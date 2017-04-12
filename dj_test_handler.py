import logging

class TestHandler(object):

	def __init__(self, google_user_db, facebook_user_db, custom_user_db):
		self.google_userdb = google_user_db
		self.facebook_userdb = facebook_user_db
		self.custom_userdb = custom_user_db

	def test_db(self):

		self.show_google_users()
		self.show_facebook_users()
		self.show_custom_users()

	def show_google_users(self):

		logging.info("[+] Getting google users from db")
		google_users = self.google_userdb.query().fetch()
		logging.info("[+] Number of google users in OneFeed datastore: " + str(len(google_users)))

		for user in google_users:

			logging.info(check_value("key_name", user))
			logging.info(check_value("id", user))
			logging.info(check_value("display_name", user))
			logging.info(check_value("family_name", user))
			logging.info(check_value("given_name", user))
			logging.info(check_value("email", user))
			logging.info(check_value("social_networks", user))

	def show_facebook_users(self):
		
		logging.info("[+] Getting facebook users from db")
		facebook_users = self.facebook_userdb.query().fetch()
		logging.info("[+] Number of facebook users in OneFeed datastore: " + str(len(facebook_users)))
	
		for user in facebook_users:
			logging.info(check_value("key_name", user))
			logging.info(check_value("id", user))
			logging.info(check_value("middle_name", user))
			logging.info(check_value("name", user))
			logging.info(check_value("first_name", user))
			logging.info(check_value("picture_uri", user))
			logging.info(check_value("link_uri", user))
			logging.info(check_value("last_name", user))
			logging.info(check_value("social_networks", user))

	def show_custom_users(self):
		logging.info("[+] Getting Custom users from db")
		custom_users = self.custom_userdb.query().fetch()
		logging.info("[+] Number of Custom users in OneFeed datastore: " + str(len(custom_users)))

def check_value(param, user):
	if param in user._properties:
		return user[param]
	else:
		return "User has no property %s" % param

def log(msg):
	logging.info(msg)