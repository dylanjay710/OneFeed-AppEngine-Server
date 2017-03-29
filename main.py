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

class CreateAccountHandler(MainHandler):

    def get(self):
        self.write("get request received")

    def post(self):
        try:
            username = self.request.get("username")
            password = self.request.get("password")
            confirm_password = self.request.get("confirm_password")
            email = self.request.get("email")
            confirm_email = self.request.get("confirm_email")
            data = [username, password, confirm_password, email, confirm_email]
            
            log_args(data)

            # account_check_response = analyze_form(username, password, confirm_password, email, confirm_email):
            # if account_check_response[0] == True:
            #     self.write("user with username %s" % username + " stored successfully")
            #     log("user stored sanity check")

            # elif account_check_response[0] == False:
            #     self.write("Form Error: %s" % account_check_response[1])

        except Exception as e:
            self.write("Exception Encountered while validating form: %s" % str(e))

# def analyze_form(username, password, confirm_password, email, confirm_email):
#     error_msg = None
#     if len(username) >= 2:
#         if len(password) >=5:
#             if validEmail(email):
#                 if passwords_match(password, confirm_password)
#                     if emails_match(email, confirm_email):
#                         // add exists method here
#                         try:
#                             OneFeedUser.store_user(username, password, confirm_password, email, confirm_email)
#                             return (True, error_msg)

#                         except  Exception as e:
#                             log("Exception Encountered: %s" % str(e))
#                     else:
#                         error_msg = "emails do not match"
#                 else:
#                     error_msg = "passwords do not match"
#             else:
#                 error_msg = "invalid email"
#         else:
#             error_msg = "password must be at least 5 characters long"
#     else:
#         error_msg = "username must be at least 2 characters long"

#     return (False, error_msg)

def emails_match(email, confirm_email):
    return validEmail(email) and validEmail(confirm_email) and email == confirm_email

def validEmail(email):
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match != None:
        return True

def log(msg):
    logging.info(msg)

def log_args(args):
    for arg in args:
        log(arg)

app = webapp2.WSGIApplication([
    ('/create_account', CreateAccountHandler),

], debug=True)
