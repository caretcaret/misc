__module_name__ = "caretbot"
__module_version__ = "1.0"
__module_description__ = "caretbot"

print __module_name__ + ' ' + __module_version__

import xchat
import re

username = 'caretbot'
servername = 'irc.rizon.net'
channel = '#lelandcs'

responses = [['nyaa', 'nyaa~'],
			 ['big', "That's what she said!"],
			 ['huge', "That's what she said!"],
			 ['long', "That's what she said!"],
			 ['hard', "That's what she said!"],
			 ['lost', "the game"],
			 ['okay', '.jpg']]

def on_message(word, word_eol, userdata):
	user = word[0]
	message = word[1].strip().lower()

	for trigger, response in responses:
		if message.find(trigger) != -1:
			if response[0] == '*':
				xchat.get_context().command('me ' + response[1:])
			else:
				xchat.get_context().command('say ' + response)
			return xchat.EAT_XCHAT

	return xchat.EAT_XCHAT

def on_address(word, word_eol, userdata):
	user = word[0]
	message = word[1].strip()
	pattern = r'^' + username + r"[^A-Za-z0-9]*<(.+)><(.+)>$"

	m = re.match(pattern, message)
	if m:
		responses.append([m.group(1), m.group(2)])
		xchat.get_context().command('say ' + '^_^')
		return xchat.EAT_ALL
	else:
		on_message(word, word_eol, userdata)
	xchat.get_context().command('say ' + 'nya?')

	return xchat.EAT_ALL

xchat.hook_print('Channel Message', on_message)
xchat.hook_print('Channel Msg Hilight', on_address)