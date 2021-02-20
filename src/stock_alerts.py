# -*- coding: utf-8 -*-
import helpers
import tweepy


class PS5StockAlerts:
	def __init__(self, user='PS5StockAlerts', limit=1, verbose=True):
		self.credentials = helpers.read_json('ps_alert.json')

		self.api = tweepy.API(self.authenticate())

		self.user = user
		self.limit = limit

		self.verbose = verbose

	def authenticate(self):
		"""This function authenticates into twitter.

		Returns
		-------
		auth : tweepy.auth.OAuthHandler
			Twitter authentication access.

		"""
		auth = tweepy.OAuthHandler(**self.credentials.get('consumer'))
		auth.set_access_token(**self.credentials.get('application'))

		return auth

	def retrieve_tweets(self):
		"""This function retrieves the - latest - tweets from a given user.

		Returns
		-------
		response : tweepy.models.Status.
			Latest tweet.

		"""
		return self.api.user_timeline(
			screen_name=self.user,
			count=self.limit,
			tweet_mode='extended'
		)[0]

	@staticmethod
	def seek_and_destroy(tweet, verbose):
		"""This function seeks for "Playstation 5 In Stock NOW"

		Parameters
		----------
		tweet : tweepy.models.Status.
			Latest tweet.
		verbose : bool
			Not found verbose.

		Returns
		-------
		url : str
			Tweet url.

		"""
		if 'playstation 5 in stock now' in tweet.full_text.lower():
			return 'https://twitter.com/twitter/statuses/{}'.format(tweet.id)
		if verbose:
			return 'Impossible, perhaps the archives are incomplete!'

	def __call__(self, *args, **kwargs):
		return self.seek_and_destroy(self.retrieve_tweets(), self.verbose)


def add_me(message):
	"""This function adds user/chat id into a database.

	Parameters
	----------
	message : telebot.types.Message
		The message object.

	Returns
	-------
	msg : str
		User/Chat alert list addition/removal.

	"""
	helpers.set_path()
	helpers.start_connection().query("""
		INSERT INTO
			`mooncake-304003.misc.ps5-stock`
		VALUES 
			({})
	""".format(message.chat.id))

	return 'User/chat added to PS5 alert list!'


def drop_me(message):
	"""This function removes user/chat id into a database.

	Parameters
	----------
	message : telebot.types.Message
		The message object.

	Returns
	-------
	msg : str
		User/Chat alert list addition/removal.

	"""
	helpers.set_path()
	helpers.start_connection().query("""
		DELETE FROM
			`mooncake-304003.misc.ps5-stock`
		WHERE
			CHAT_ID = {}
	""".format(message.chat.id))

	return 'User/chat removed from PS5 alert list!'
