import logging
class TestHandler(object):

	def __init__(self, google_user_db, facebook_user_db):
		self.google_userdb = google_user_db
		self.facebook_userdb = facebook_user_db

	def test_db(self):

		self.show_google_users()
		self.show_facebook_users()

	def show_google_users(self):

		logging.info("getting google users from db")
		google_users = self.google_userdb.query().fetch()
		logging.info("[+] Number of google users in OneFeed datastore: " + str(len(google_users)))

		for user in google_users:
			
			if "given_name" in user._properties:
		
			logging.info(user.key_name)
			logging.info(user.display_name)
			logging.info(user.family_name)
			logging.info(user.display_name)
			logging.info(user.email)
			logging.info(user.social_networks)

	def show_facebook_users(self):
		
		logging.info("getting facebook users from db")
		facebook_users = self.facebook_userdb.query().fetch()
		logging.info("[+] Number of facebook users in OneFeed datastore: " + str(len(facebook_users)))
	
		for user in facebook_users:
			logging.info(user)



