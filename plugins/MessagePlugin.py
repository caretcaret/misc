from BasePlugin import BasePlugin

class MessagePlugin(BasePlugin):
	def __init__(self):
		"""Defines the base template of a plugin."""
		self.require_comments = False  # Does plugin require data from new comments feed?
		self.require_messages = True  # Does plugin require data from private messages?
		self.subreddits = None  # None if no restriction to subreddits, or a list of subreddits to allow
		# The plugin will only be invoked if a subreddit is in both config and self.subreddits

	def expose(self, petbot, data):
		"""When the bot receives data, the `expose` function is called iff the data is required
		by the plugin. The plugin processes the data (e.g. stores in database) and returns a value `bid`.
		If `bid` is negative, the plugin's behavior will not be invoked.
		If `bid` is 0, the plugin's behavior will always be invoked.
		If `bid` is positive, the single plugin with the highest positive bid will have its behavior invoked.
		If two or more plugins tie, a random choice is made."""
		return -1

	def invoke(self, petbot, data):
		"""The `invoke` function defines the plugin's behavior. This function is called when the bot
		decides to act according to its behavior after `expose` is called for every plugin.
		Returns a value `action`, a prioritized tuple that dictates the type of behavior for the bot
		to take, which is enqueued in the action queue."""
		return None
