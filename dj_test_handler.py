import logging
class TestHandler(object):

	def __init__(self, db_handler):
		self.db_handler = db_handler

	def test_db(self):

		logging.info("getting all users from db")
		users = self.db_handler.get_all_entities()
		logging.info("number of onefeed users in datastore: " + str(len(users)))
		logging.info("Iterating over users in google cloud. Passwords will be hashed soon lol. Don't ask")
		for user in users:
			logging.info(user.username)
			logging.info(user)
			logging.info(user.userid)
			logging.info(user.email)
			logging.info(user.social_network_feeds)

