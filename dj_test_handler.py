import logging
class TestHandler(object):

	def __init__(self, db_handler):
		self.db_handler = db_handler

	def test_db(self):

		username = "test_username"
		id = "idonenigga"

		logging.info("getting all users from db")
		users = self.db_handler.get_all_entities()
		logging.info(len(users))
		
		logging.info("checking user %s exists" % username)
		username_exists_boolean = self.db_handler.username_exists(username)
		logging.info("username exists: %s" % username_exists_boolean)


		logging.info("check id %s exists" % id)
		id_exists = self.db_handler.userid_exists(id)
		logging.info("user id exists: %s" % id_exists)

		logging.info("testing creating user_key")
		new_user_key = self.db_handler.create_user_key()
		logging.info("created user key: %s" % new_user_key)

		logging.info("testing random key function")
		random_key = self.db_handler.create_random_key()
		logging.info("random key: %s" % random_key)

		logging.info("checking login credentials with login username password")
		user_login_correct = self.db_handler.check_login_credentials("username", "password")
		logging.info("user login valid: %s" % user_login_correct)

