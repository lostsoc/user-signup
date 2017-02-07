#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import webapp2
import re


form = """
    <h2>Signup</h2>
    <form method='post'>
    <label>Username:<input type='text' name='username' value="%(username)s" required><span style="color: red"> %(username_error)s </span></label><br>
    <label>Password:<input type = 'password' name='password' required></label><br>
    <label>Verify Password:<input type = 'password' name='verify' required><span style = "color: red"> %(verify_error)s </span></label><br>
    <label>Email (optional):<input type='text' name='email' value='%(email)s'><span style = "color: red"> %(email_error)s </span></label><br>
    <input type='submit' value='Submit'>
    </form>"""

def valid_username(username):
    pattern = r'^[a-zA-Z0-9_-]{3,20}$'
    if re.search(pattern, username):
        return username

def valid_password(password):
    pattern = r'^.{3,20}$'
    if re.search(pattern, password):
        return password


def valid_verify(verify, password):
    if verify == password:
        return verify

def valid_email(email):
    pattern = r'^[\S]+@[\S]+.[\S]+$'
    if re.search(pattern,email):
        return email
    elif email == "":
        email ="none"
        return email


class MainHandler(webapp2.RequestHandler):
    def write_form(self, username_error= "", verify_error="", email_error="", username="", email=""):
        self.response.write(form % {"username_error": username_error,  "verify_error": verify_error, "email_error": email_error, "username": username, "email": email})

    def get(self):
        self.write_form()

    def post(self):
        input_username = self.request.get("username")
        input_email = self.request.get("email")

        username = valid_username(input_username)
        password = valid_password(self.request.get("password"))
        verify = valid_verify((self.request.get("verify")),(self.request.get("password")))
        email = valid_email(input_email)

        if (username and password and verify and email):
            self.response.write("Welcome, " + username +"!")
        elif not (verify):
            self.write_form("","Passwords entered do not match.", "", input_username, input_email)
        elif not (username):
            self.write_form("The username you entered contains an invalid character.","","", input_username, input_email)
        elif not (email):
            self.write_form("","","The email entered is not properly formatted.", input_username, input_email)


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
