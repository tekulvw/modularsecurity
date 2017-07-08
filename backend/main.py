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
from flask import Flask
from flask_login import LoginManager

import os
import logging

from models import User
from resources.user import AuthorizeUser, AuthorizedUser, UserInfo, Login
from resources.user import Logout
from resources.home import Home

from auth import google, initialize_tokengetter

app = Flask(__name__)

app.config['GOOGLE_ID'] = os.environ.get("GOOGLE_CLIENT_ID")
app.config['GOOGLE_SECRET'] = os.environ.get("GOOGLE_SECRET")
app.secret_key = os.environ.get("APP_SECRET_KEY")

login_manager = LoginManager(app)
app.config["LOGIN_MGR"] = login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.from_oauth_id(user_id)

# app.add_url_rule('/', view_func=Home.as_view("home"))
app.add_url_rule('/api/authorize/', view_func=AuthorizeUser.as_view("authorize"))
app.add_url_rule('/api/authorize/complete', view_func=AuthorizedUser.as_view("authorized"))
app.add_url_rule('/api/user/info', view_func=UserInfo.as_view('user.info'))
app.add_url_rule('/api/login', view_func=Login.as_view('login'))
app.add_url_rule('/api/logout', view_func=Logout.as_view('logout'))

auth = google.initialize(app)
initialize_tokengetter(auth)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
