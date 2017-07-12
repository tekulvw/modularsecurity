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

import logging
import uuid
import os

from models.user import User as UserModel

from resources.user import AuthorizeUser, AuthorizedUser, UserInfo, Login, User
from resources.user import Logout
from resources.device import DeviceCollectionResource, DeviceResource
from resources.system import System
from resources.system import KillSwitch

from auth import google, initialize_tokengetter, read_client_keys

app = Flask(__name__)

client_id, client_secret = read_client_keys()

app.config['GOOGLE_ID'] = client_id
app.config['GOOGLE_SECRET'] = client_secret
app.secret_key = str(uuid.uuid4())

login_manager = LoginManager(app)
app.config["LOGIN_MGR"] = login_manager

if os.environ.get("TESTING"):
    app.config["SERVER_NAME"] = 'localhost'


@login_manager.user_loader
def load_user(user_id):
    return UserModel.from_oauth_id(user_id)

# app.add_url_rule('/', view_func=Home.as_view("home"))
app.add_url_rule('/api/authorize/', view_func=AuthorizeUser.as_view("authorize"))
app.add_url_rule('/api/authorize/complete', view_func=AuthorizedUser.as_view("authorized"))
app.add_url_rule('/api/user/', view_func=User.as_view('user'))
app.add_url_rule('/api/user/info', view_func=UserInfo.as_view('user.info'))
app.add_url_rule('/api/login', view_func=Login.as_view('login'))
app.add_url_rule('/api/logout', view_func=Logout.as_view('logout'))

app.add_url_rule('/api/device', view_func=DeviceCollectionResource.as_view('device'),
                 methods=["POST"])

single_dev_view = DeviceResource.as_view('device.single')
app.add_url_rule('/api/device/data', view_func=single_dev_view,
                 methods=["POST"])

system_view = System.as_view('system')
app.add_url_rule('/api/system', methods=["POST", ], view_func=system_view)
app.add_url_rule('/api/system/<int:system_id>',
                 methods=["GET","PUT"],
                 view_func=system_view)

killswitch_view = KillSwitch.as_view('killswitch')
app.add_url_rule('/api/system/<int:system_id>/killswitch', view_func=killswitch_view,
                 methods=["PUT"])

auth = google.initialize(app)
initialize_tokengetter(auth)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
