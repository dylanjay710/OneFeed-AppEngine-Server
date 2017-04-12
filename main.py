# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



""" Welcome everyone! This is the google app engine backend for an android app that connects and organizes social networks """
import webapp2
import os
import jinja2
import re
import random
import pickle
import string
import json
import logging
import random
from google.appengine.ext import ndb
import sys
import dj_test_handler

print sys.path

template_dir = os.path.join(os.path.dirname(__file__), 'jinja_templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

""" Still using Steve Huffmans Mainhandler class """
class MainHandler(webapp2.RequestHandler):

    def write(self, *args, **kwargs):
        self.response.out.write(*args, **kwargs)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kwargs):
        self.write(self.render_str(template, **kwargs))

""" Google Cloud Datastore """

# Facebook User Database
class FacebookUser(ndb.Expando):

    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    middle_name = ndb.StringProperty()
    name = ndb.StringProperty()
    picture_uri = ndb.StringProperty()
    link_uri = ndb.StringProperty()

    date_created = ndb.DateTimeProperty(auto_now_add=True)
    social_networks = ndb.StringProperty(repeated=True)

    @classmethod 
    def user_exists(cls, fid):
        user = cls.get_by_id(fid) # accesses the id
        return user != None

    @classmethod
    def store_user(cls, fid, middle_name, name, first_name, picture_uri, link_uri, last_name):

        new_facebook_user = FacebookUser(
            middle_name=middle_name,
            name=name,
            first_name=first_name,
            picture_uri=picture_uri,
            link_uri=link_uri,
            last_name=last_name,
            social_networks=[]
        )
        new_facebook_user.key = ndb.Key('FacebookUser', fid)
        key = new_facebook_user.put()
        return new_facebook_user, key

    @classmethod
    def update_facebook_profile(cls, fid, middle_name, name, first_name, picture_uri, link_uri, last_name):
        user = cls.get_by_id(fid)
        user.middle_name = middle_name
        user.name = name
        user.first_name = first_name
        user.picture_uri = picture_uri
        user.link_uri = link_uri
        user.last_name = last_name

        user.put()

# Google User Database
class GoogleUser(ndb.Expando):

    email = ndb.StringProperty()
    display_name = ndb.StringProperty()
    given_name = ndb.StringProperty()
    family_name = ndb.StringProperty()
    social_networks = ndb.StringProperty(repeated=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def store_user(cls, em, dn, gn, fn, gid):
        
        new_google_user = GoogleUser(
            email=em, 
            display_name=dn,
            given_name=gn,
            family_name=fn,
            social_networks=[]
        )
        new_google_user.key = ndb.Key('GoogleUser', gid)
        key = new_google_user.put()
        return new_google_user, key

    @classmethod
    def user_exists(cls, gid):
        user = cls.get_by_id(gid) # accesses the userid
        return user != None

# database for users who sign in with email and password
class CustomUser(ndb.Expando):

    username = ndb.StringProperty()
    password = ndb.StringProperty()
    email = ndb.StringProperty()
    social_networks = ndb.StringProperty(repeated=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def store_user(cls, username, password, email):
        key = cls.create_user_key()
        user = cls(
            id=key,
            username=username,
            password=password,
            email=email,
            social_networks=[])
        k = user.put()
        return (user, k)

    @classmethod
    def check_login_credentials(cls, username, password):
        user = cls.query(cls.username == username and cls.password == password)
        u = user.get()
        return u != None

    @classmethod
    def get_all_entities(cls):
        return cls.query().fetch()

    @classmethod
    def user_exists(cls, user_id_key):
        user = cls.get_by_id(user_id_key)
        return user != None

    @classmethod
    def username_exists(cls, username):
        user = cls.query(cls.username == username)
        return user.get() != None

    @classmethod
    def create_user_key(cls):
        user_key = cls.create_random_key()
        while (cls.userid_exists(user_key)):
            user_key = cls.create_random_key()
        return user_key

    @classmethod
    def random_letter(cls, string):
        return string[random.randint(0, len(string)-1)]

    @classmethod
    def create_random_key(cls):
        random_letters = string.lowercase + string.digits + string.uppercase + string.digits
        user_id_args = [ cls.random_letter(random_letters) for i in range(15) ]
        random_key = "".join(user_id_args)
        return "key:%s" % random_key

    @classmethod
    def log_users_on_server(cls):
        each(cls.query(), log)

    @classmethod
    def delete_all(cls):
        log("deleting all Custom Users")


class DBTester(MainHandler):

    def get(self):
        db_tester = dj_test_handler.TestHandler(GoogleUser, FacebookUser, CustomUser)
        db_tester.test_db()

    def post(self):
        pass

   
class CustomLoginHandler(MainHandler):

    def get(self):
        pass

    def post(self):
        try:

            submit_way = self.request.get("login_type")

            if submit_way == "signup":

                username = self.request.get("username")
                password = self.request.get("password")
                email = self.request.get("email")

                if validForm(username, password, email)[0] == True:
                    if CustomUser.username_exists(username):

                        log("[+] username %s exists" % username)
                        self.write("username_exists,true")

                    else:

                        new_user, key = CustomUser.store_user(username, password, email)
                        log("[+] New user stored using custom login ")
                        self.write("username_exists,false")

            elif submit_way == "login":

                username = self.request.get("username")
                password = self.request.get("password")

                credentialsValid = CustomUser.check_login_credentials(username, password)

                if credentialsValid:
                    self.write("login,true")
                else:
                    self.write("login,false")

        except Exception as e:
            self.write("Exception ENcountered %s" % str(e))

 
class GoogleLoginHandler(MainHandler):
    def get(self):
        pass

    def post(self):

        try:
            google_id = self.request.get("google_id")
            display_name = self.request.get("display_name")
            email = self.request.get("email")
            family_name = self.request.get("family_name")
            given_name = self.request.get("given_name")

            # Respond with a boolean indicating whether or not this is the users first time signing in, true if so

            if GoogleUser.user_exists(google_id):
                self.write("true")
            else:
                user, key = GoogleUser.store_user(email, display_name, given_name, family_name, google_id)
                self.write("false")
            
        except Exception as e:
            log(str(e))
            self.write("error")

class FacebookLoginHandler(MainHandler):
    def get(self):
        pass

    def post(self):
        try:
            facebook_id = self.request.get("facebook_id")
            middle_name = self.request.get("middle_name")
            name = self.request.get("name")
            first_name = self.request.get("first_name")
            picture_uri = self.request.get("picture_uri")
            link_uri = self.request.get("link_uri")
            last_name = self.request.get("last_name")

            if FacebookUser.user_exists(facebook_id):
                FacebookUser.update_facebook_profile(facebook_id, middle_name, name, first_name, picture_uri, link_uri, last_name)
                self.write("true")
            else:
                new_facebook_user, key = FacebookUser.store_user(facebook_id, middle_name, name, first_name, picture_uri, link_uri, last_name)
                self.write("false")

        except Exception as e:
            log("Exception encountered %s" % str(e))

class HomePage(MainHandler):

    def get(self):
        self.render("index.html")

    def post(self):
        pass
        
def validForm(username, password, confirm_password, email, confirm_email):
    return (True, None)

# def emails_match(email, confirm_email):
#     return validEmail(email) and validEmail(confirm_email) and email == confirm_email:

def validEmail(email):
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match != None:
        return True
    return False

def log(msg):
    logging.info(msg)

def log_args(args):
    for arg in args:
        log(arg)

def each(args, f):
    for arg in args:
        f(arg)

app = webapp2.WSGIApplication([

    ('/', HomePage),
    ('/handle_custom_login', CustomLoginHandler),
    ('/test_db', DBTester),
    ('/handle_google_login', GoogleLoginHandler),
    ('/handle_facebook_login', FacebookLoginHandler),


], debug=True)
