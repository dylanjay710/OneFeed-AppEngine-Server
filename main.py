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

class User(ndb.Model):
    # uid = ndb.StringProperty(required
    pass

class OneFeedUser(ndb.Expando):

    userid = ndb.StringProperty(required=True)
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    social_network_feeds = ndb.StringProperty(repeated=True)

    @classmethod
    def store_user(cls, username, password, email, social_networks):
        key = cls.create_user_key()
        user = cls(
            key_name=key,
            userid=key,
            username=username,
            password=password,
            email=email,
            social_network_feeds=social_networks)
        user.put()
        return user

    @classmethod
    def get_all_entities(cls):
        return cls.query()

    @classmethod
    def userid_exists(cls, user_id_key):
        user = cls.get_by_id(user_id_key)
        return user != None

    @classmethod
    def username_exists(cls, username):
        user = cls.query(cls.username == username)
        return user != None

    @classmethod
    def create_user_key(cls):
        user_id_key = cls.create_random_key()
        while (cls.userid_exists(user_id_key)):
            user_id_key = cls.create_random_key()
        return user_id_key

    @classmethod
    def random_letter(cls, string):
        return string[random.randint(0, len(string)-1)]

    @classmethod
    def create_random_key(cls):
        random_letters = string.lowercase + string.digits + string.uppercase + string.digits
        user_id_args = [ cls.random_letter(random_letters) for i in range(15) ]
        return "".join(user_id_args)

    @classmethod
    def log_users_on_server(cls):
        each(cls.query(), log)

    @classmethod
    def delete_all(cls):
        log("deleting all users")

class DBHandler(MainHandler):
    def get(self):
        action = self.request.get("action")
        if action == "log_users_on_server":
            OneFeedUser.log_users_on_server()
        elif action == "delete_all":
            OneFeedUser.delete_all();
        
class CreateAccountHandler(MainHandler):
    
    def test_functions(self):
        pass

    def get(self):
        self.test_functions()
        self.write("<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js'></script>")

    def post(self):
        try:
            username = self.request.get("username")
            password = self.request.get("password")
            confirm_password = self.request.get("confirm_password")
            email = self.request.get("email")
            confirm_email = self.request.get("confirm_email")

            if validForm(username, password, confirm_password, email, confirm_email)[0] == True:
                if OneFeedUser.username_exists(username):
                    log("%s exists, displaying error msg" % username)
                    self.write("username exists %s" % username)
                else:
                    new_user = OneFeedUser.store_user(username, password, email, [])
                    log("user stored with properties")
                    log(new_user._properties)
                    self.write("ok working bitch")

        except Exception as e:
            self.write("Exception ENcountered %s" % str(e))

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
    ('/create_account', CreateAccountHandler),

], debug=True)
