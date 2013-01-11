# Petbot
# an interactive modular reddit bot
# original author: Jeffrey Zhang

import queue
import configparser
import argparse
import sys
import datetime
import threading
import requests

class Petbot:
	def __init__(self, settings):
		for k, v in settings.items():
			setattr(self, k, v)
		self.headers = {'User-Agent': "Petbot by /u/" + settings['owner_name']}

	def run(self):
		pass

	def login(self):
		try:
			payload = {
				'user': self.bot_name,
				'passwd': self.bot_password,
				'api_type': 'json',
			}
			r = requests.post('https://ssl.reddit.com/api/login', params=payload, headers=self.headers)
			data = r.json()
			if len(data['json']['errors']) != 0:
				print("Error logging into reddit:")
				print('\n'.join(data['json']['errors']))
				sys.exit()
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
		arguments['behavior'] = {'verbose': ns.verbose }
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
			config.read_dict(DEFAULT_SETTINGS)
			config.read_file(config_file)
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
