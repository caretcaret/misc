# Petbot
# an interactive modular reddit bot
# original author: Jeffrey Zhang

import queue
import configparser
import argparse
import sys
import datetime
import time
import threading
import requests
import importlib
import random

class Data:
	def __init__(self, json, tags=None):
		for item in json:
			setattr(self, k, v)
		self.tags = tags or []

class MessageData(Data):
	def __init__(self, json, tags=None):
		super().__init__(self, json, tags)
		self.tags.append('message')


class Action:
	def __init__(self, api_url, api_args=None, api_method='GET', tags=None):
		"""Represents an action to be done using the reddit api.
		`api_url` specifies the url to send the request to.
		`api_args` specifies the arguments in a POST/GET request
		`api_method` specifies either `'GET'` or `'POST'`
		`tags` specifies any information to be attached to the Data object,
		which must be a list."""
		self.api_url = api_url
		self.api_args = api_args or {}
		self.api_method = api_method
		self.tags = tags or []

	def extract_data(self, json):
		"""Receives a json dict and returns a `Data` object"""
		return Data()

class PollCommentsAction(Action):
	def __init__(self, subreddits, tags=None):
		super().__init__('https://reddit.com/r/' + '+'.join(subreddits) + '/comments/.json', tags=tags)

class PollMessagesAction(Action):
	def __init__(self, tags=None):
		super().__init__('https://reddit.com/message/unread/.json', tags=tags)

	def extract_data(self, json):
		messages = json['data']['children']
		if len(messages) == 0:
			return None
		datas = []
		for thing in messages:
			datas.append(thing['data'])
		return datas


class Petbot:
	def __init__(self, settings, plugins):
		for k, v in settings.items():
			setattr(self, k, v)
		self.plugins = plugins
		self.require_comments = any([plugin.require_comments for plugin in plugins])
		self.require_messages = any([plugin.require_messages for plugin in plugins])
		self.headers = {'User-Agent': "Petbot by /u/" + self.owner_name }
		self.pq_action = queue.PriorityQueue()
		self.pq_data = queue.PriorityQueue()
		self.running = False

	def login(self):
		# check that credentials exist
		if any([len(x) == 0 for x in [self.owner_name, self.bot_name, self.bot_password]]):
			print("Error: missing owner name, bot name, or bot password")
			sys.exit()
		try:
			# send request
			payload = {
				'user': self.bot_name,
				'passwd': self.bot_password,
				'api_type': 'json',
			}
			r = requests.post('https://ssl.reddit.com/api/login', params=payload, headers=self.headers)
			data = r.json()
			# check for errors
			if len(data['json']['errors']) != 0:
				print("Error logging into reddit:")
				print('\n'.join(data['json']['errors']))
				sys.exit()
			# get and store data
			self.modhash = data['json']['data']['modhash']
			self.headers['Cookie'] = 'reddit_session=' + data['json']['data']['cookie']
			self.last_api_call = datetime.datetime.utcnow()
			self.verbose and print(datetime.datetime.utcnow(),
				"Logged in as", self.bot_name,
				"with cookie", self.headers['Cookie'],
				"and modhash", self.modhash)
		except requests.exceptions.RequestException as e:
			print("Error logging into reddit:")
			print(e)
			sys.exit()

	def submit(self, action):
		"""Submits an Action object through json and returns the corresponding Data associated with it"""
		method = action.api_method.upper()
		if method == 'GET':
			r = requests.get(action.api_url, params=action.api_args, headers=self.headers)
			data = r.json()
			return action.extract_data(data)
		elif method == 'POST':
			action.api_args['uh'] = self.modhash
			r = requests.post(action.api_url, params=action.api_args, headers=self.headers)
			data = r.json()
			return action.extract_data(data)

	def run(self):
		# After credentials are acquired, spawn a thread
		# that controls polling the api and its frequency.
		api_thread = threading.Thread(target=self.api_thread)
		api_thread.start()
		self.running = True
		try:
			while self.running:
				# Wait until incoming data is received
				data = self.pq_data.get()
				# Data passes through plugin matching
				best = []
				best_score = 0
				actions = []
				for plugin in self.plugins:
					bid = plugin.expose(self, data)
					# if bid is negative, discard plugin for this data
					if bid < 0:
						continue
					# if bid is 0, add to the list of plugins to generate action
					elif bid == 0:
						actions.append(plugin)
					# if bid is positive, compare with other bids
					else:
						if bid > best_score:
							best = [plugin]
							best_score = bid
						elif bid == best_score:
							best.append(plugin)
				# Select the best plugin
				if len(best) > 0:
					actions.append(random.choice(best))
				# Generate actions and submit to api queue
				for plugin in actions:
					action = plugin.invoke(self, data)
					self.pq_action.put((1, action))
		# User wants to stop the bot with ^C
		except KeyboardInterrupt:
			self.running = False
			self.verbose and print(datetime.datetime.utcnow(), "Stopped running.")

	def api_thread(self):
		self.verbose and print(datetime.datetime.utcnow(), "API thread started.")
		last_comments_poll = datetime.datetime.utcnow() - self.comments_delay
		last_messages_poll = datetime.datetime.utcnow() - self.messages_delay
		last_api_call = datetime.datetime.utcnow()
		while self.running:
			# Uses a simple model of First In First Out for scheduling, except when
			# checking for comments/messages, which is prioritized.
			# TODO: priority of polling should be a function of how much
			# new information is acquired.
			# Add a request for polling comments if it has been comments_delay long since last poll
			if self.require_comments:
				if last_comments_poll + self.comments_delay < datetime.datetime.utcnow():
					self.verbose and print(datetime.datetime.utcnow(), "Adding request to poll comments")
					self.pq_action.put((0, PollCommentsAction(self.subreddits)))
					last_comments_poll = datetime.datetime.utcnow()
					last_api_call = datetime.datetime.utcnow()
			# Same for polling private messages
			if self.require_messages:
				if last_messages_poll + self.messages_delay < datetime.datetime.utcnow():
					self.pq_action.put((0, PollMessagesAction()))
					last_messages_poll = datetime.datetime.utcnow()
					last_api_call = datetime.datetime.utcnow()
			# There are api actions waiting to be done
			if not self.pq_action.empty():
				if last_api_call + self.api_delay < datetime.datetime.utcnow():
					# Dequeue to get api action
					action = self.pq_action.get()
					# Submit action and get data from it
					data = self.submit(action)
					# Enqueue action
					# TODO: detect if there is any meaningful data
					self.pq_data.put(data)
		self.verbose and print(datetime.datetime.utcnow(), "API thread stopped.")


if __name__ == '__main__':
	DEFAULT_SETTINGS = {
		'user': {
			'owner_name': '',
			'bot_name': '',
			'bot_password': '',
		},
		'behavior': {
			'subreddits': '',
			'plugins': '',
			'api_delay': '2000',
			'comments_delay': '10000',
			'messages_delay': '10000',
			'verbose': 'yes',
		}
	}
	# parse args
	arguments = {}
	parser = argparse.ArgumentParser(description="Interactive modular reddit bot.")
	parser.add_argument('-f', action='store', dest='config_filename', default='config.ini',
		help="Non-default config filename.")
	parser.add_argument('-v', action='store_true', dest='verbose', default=False, help="Verbose printout.")
	try:
		ns = parser.parse_args()
		arguments['behavior'] = { 'verbose': ns.verbose }
		config_filename = ns.config_filename
	except IOError as e:
		print("Error parsing arguments.")
		print(e)
		sys.exit()

	# parse config
	settings = {}
	try:
		with open(config_filename, 'r') as config_file:
			config = configparser.ConfigParser()
			# fallback settings
			config.read_dict(DEFAULT_SETTINGS)
			# load settings from file
			config.read_file(config_file)
			# overwrite settings from arguments
			config.read_dict(arguments)
			settings['owner_name'] = config.get('user', 'owner_name')
			settings['bot_name'] = config.get('user', 'bot_name')
			settings['bot_password'] = config.get('user', 'bot_password')
			settings['subreddits'] = [x.strip() for x in config.get('behavior', 'subreddits').split(',') if x.strip() != '']
			settings['plugins_str'] = [x.strip() for x in config.get('behavior', 'plugins').split(',') if x.strip() != '']
			option_to_timedelta = lambda option: datetime.timedelta(milliseconds=int(config.get('behavior', option)))
			settings['api_delay'] = option_to_timedelta('api_delay')
			settings['comments_delay'] = option_to_timedelta('comments_delay')
			settings['messages_delay'] = option_to_timedelta('messages_delay')
			settings['verbose'] = config.getboolean('behavior', 'verbose')
	except (IOError, configparser.Error) as e:
		print("Missing or broken config file at", config_filename)
		print(e)
		sys.exit()

	# Import plugins specified by the settings
	plugins = []
	try:
		for plugin in settings['plugins_str']:
			module = importlib.import_module('plugins.' + plugin)
			# Get the plugin classes from the module
			for name in dir(module):
				obj = getattr(module, name)
				# check if obj is a class and if it is in the plugin list
				if isinstance(obj, type) and name in settings['plugins_str']:
					# add an instance of the class so we can get its attributes
					plugins.append(obj())
					settings['verbose'] and print(datetime.datetime.utcnow(), "Loading plugin", name)
	except ImportError as e:
		print("Missing or broken plugin")
		print(e)
		sys.exit()

	if len(plugins) == 0:
		print("No plugins! Quitting")
		sys.exit()

	# run!
	petbot = Petbot(settings, plugins)
	petbot.login()
	petbot.run()
