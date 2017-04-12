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

			log(user.key)
			log(user.key.get())
			log("[+] Display Name: %s" % user.display_name)
			log("[+] Family Name: %s" % user.family_name)
			log("[+] Given Name: %s" % user.given_name)
			log("[+] Email: %s" % user.email)
			log("[+] Social Networks; %s" % user.social_networks)

	def show_facebook_users(self):
		
		logging.info("[+] Getting facebook users from db")
		facebook_users = self.facebook_userdb.query().fetch()
		logging.info("[+] Number of facebook users in OneFeed datastore: " + str(len(facebook_users)))
	
		for user in facebook_users:

			log(user.key)

			log(user.key.get())
			log("[+] First Name: %s" % user.first_name)
			log("[+] Middle Name: %s" % user.middle_name)
			log("[+] Last Name: %s" % user.last_name)
			log("[+] Name: %s" % user.name)
			log("[+] Picture Uri: %s" % user.picture_uri)
			log("[+] Link Uri: %s " % user.link_uri)
			log("[+] Social Networks: %s" % user.social_networks)

	def show_custom_users(self):
		logging.info("[+] Getting Custom users from db")
		custom_users = self.custom_userdb.query().fetch()
		logging.info("[+] Number of Custom users in OneFeed datastore: " + str(len(custom_users)))

def log(msg):
	logging.info(msg)