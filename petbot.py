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

class Petbot:
	def __init__(self, settings):
		for k, v in settings.items():
			setattr(self, k, v)
		self.headers = {'User-Agent': "Petbot by /u/" + settings['owner_name']}
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
			self.verbose or print(datetime.datetime.utcnow(),
				"Logged in as", self.bot_name,
				"with cookie", self.headers['Cookie'],
				"and modhash", self.modhash)
		except requests.exceptions.RequestException as e:
			print("Error logging into reddit:")
			print(e)
			sys.exit()

	def run(self):
		# after credentials are acquired, spawn a thread
		# that controls polling the api and its frequency.
		api_thread = threading.Thread(target=self.api_thread)
		api_thread.start()
		self.running = True
		try:
			while self.running:
				pass
				# TODO: Main thread monitors incoming data
				# TODO: Data is transformed into friendly format
				# TODO: Data passes through plugin matching
				# TODO: Best plugin is selected
				# TODO: Action is submitted to api queue
				pass
		# User wants to stop the bot with ^C
		except KeyboardInterrupt:
			self.running = False
			self.verbose or print(datetime.datetime.utcnow(), "Stopped running.")

	def api_thread(self):
		# TODO: Check which data sources are required
		# TODO: Add first data checks to queue
		self.verbose or print(datetime.datetime.utcnow(), "API thread started.")
		while self.running:
			pass
			# TODO: Dequeue to get api action
			# TODO: Determine api action and use appropriate source
			# TODO: Enqueue received data if necessary
		self.verbose or print(datetime.datetime.utcnow(), "API thread stopped.")


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
			'restrict_owner': 'yes',
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
			settings['subreddits'] = [x.strip() for x in config.get('behavior', 'subreddits').split(',')]
			settings['plugins'] = [x.strip() for x in config.get('behavior', 'plugins').split(',')]
			settings['restrict_owner'] = config.getboolean('behavior', 'restrict_owner')
			option_to_timedelta = lambda option: datetime.timedelta(milliseconds=int(config.get('behavior', option)))
			settings['api_delay'] = option_to_timedelta('api_delay')
			settings['comments_delay'] = option_to_timedelta('comments_delay')
			settings['messages_delay'] = option_to_timedelta('messages_delay')
			settings['verbose'] = config.getboolean('behavior', 'verbose')
	except (IOError, configparser.Error) as e:
		print("Missing or broken config file at", config_filename)
		print(e)
		sys.exit()

	# run!
	petbot = Petbot(settings)
	petbot.login()
	petbot.run()
