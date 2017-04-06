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

template_dir = os.path.join(os.path.dirname(__file__), 'jinja_templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class MainHandler(webapp2.RequestHandler):

    def write(self, *args, **kwargs):
        self.response.out.write(*args, **kwargs)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kwargs):
        self.write(self.render_str(template, **kwargs))

class FacebookUser(ndb.Expando):
    pass

class GoogleUser(ndb.Expando):

    email = ndb.StringProperty()
    display_name = ndb.StringProperty()
    given_name = ndb.StringProperty()
    family_name = ndb.StringProperty()
    social_networks = ndb.StringProperty(repeated=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def store_google_user(cls, em, dn, gn, fn, gid):
        user_key = "key:" + gid
        new_google_user = GoogleUser(
            key_name=user_key,
            email=em, 
            display_name=dn,
            given_name=gn,
            family_name=fn,
            social_networks=[]
        )
        key = new_google_user.put()
        log("[+] New Google User stored")
        log(key)
        return new_google_user, key

    @classmethod
    def user_exists(cls, gid):
        return cls.get_by_id(gid) != None

class CustomUser(ndb.Expando):

    username = ndb.StringProperty()
    password = ndb.StringProperty()
    email = ndb.StringProperty()
    social_network_feeds = ndb.StringProperty(repeated=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def store_user(cls, username, password, email, social_networks):
        key = "key:" + cls.create_user_key()
        user = cls(
            key_name=key,
            userid=key,
            username=username,
            password=password,
            email=email,
            social_network_feeds=social_networks)
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
    def userid_exists(cls, user_id_key):
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
        db_tester = dj_test_handler.TestHandler(GoogleUser, FacebookUser)
        db_tester.test_db()

    def post(self):
        pass

   
class CustomLoginHandler(MainHandler):

    def get(self):
        self.write("<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js'></script>")

    def post(self):
        try:

            submit_way = self.request.get("login_type")

            if submit_way == "signup":

                username = self.request.get("username")
                password = self.request.get("password")
                confirm_password = self.request.get("confirm_password")
                email = self.request.get("email")
                confirm_email = self.request.get("confirm_email")

                if validForm(username, password, confirm_password, email, confirm_email)[0] == True:
                    if OneFeedUser.username_exists(username):

                        log("[+] %s exists" % username)
                        self.write("username_exists,true")

                    else:

                        new_user, key = OneFeedUser.store_user(username, password, email, [])
                        log("[+] New user stored using custom login ")
                        self.write("username_exists,false")

            elif submit_way == "login":

                username = self.request.get("username")
                password = self.request.get("password")

                credentialsValid = OneFeedUser.check_login_credentials(username, password)

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

        google_id = self.request.get("google_id")
        display_name = self.request.get("display_name")
        email = self.request.get("email")
        family_name = self.request.get("family_name")
        given_name = self.request.get("given_name")

        # Respond with a boolean indicating whether or not this is the users first time signing in, true if so
        if GoogleUser.user_exists(google_id):
            return self.write("true") 
        else:
            user, key = GoogleUser.store_user(email, display_name, given_name, family_name, google_id)
            return self.write("false")
        

class FacebookLoginHandler(MainHandler):
    def get(self):
        pass

    def post(self):
        pass

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
