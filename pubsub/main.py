# Copyright 2015 Google Inc. All Rights Reserved.
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

# [START app]
import base64
import json
import logging
import os

from google.cloud.datastore import Client
from flask import current_app, Flask, jsonify, request, abort
from pubsub.tasks import get_system_topic, get_all_system_topic
from monitor import data_event_handler


app = Flask(__name__)

app.config['DATASTORE_CLIENT'] = Client()

# Configure the following environment variables via app.yaml
# This is used in the push request handler to veirfy that the request came from
# pubsub and originated from a trusted source.
app.config['PUBSUB_VERIFICATION_TOKEN'] = \
    os.environ['PUBSUB_VERIFICATION_TOKEN']

all_sys_topic = get_all_system_topic()
app.config['ALL_SYSTEM_TOPIC'] = all_sys_topic

app.add_url_rule("/pubsub/push-handler", methods=["POST"],
                 endpoint="push_handler",
                 view_func=data_event_handler)

base_url = os.environ.get("BASE_URL")
all_sys_sub = all_sys_topic.subscription(
    "monitor",
    ack_deadline=10,
    push_endpoint=base_url + "/pubsub/push-handler"
)

if not all_sys_sub.exists():
    all_sys_sub.create()


# [START push]
@app.route('/pubsub/datareceived', methods=['POST'])
def pubsub_datareceived():
    if (request.args.get('token', '') !=
            current_app.config['PUBSUB_VERIFICATION_TOKEN']):
        return 'Invalid request', 400

    envelope = json.loads(request.data.decode('utf-8'))
    system_id = envelope.get('system_id')

    if system_id is None:
        return abort(400)

    to_publish = base64.b64encode(request.data)

    all_system_topic = current_app.config['ALL_SYSTEM_TOPIC']
    all_system_topic.publish(
        to_publish,
        extra=current_app.app_context
    )

    system_topic = get_system_topic(system_id)
    system_topic.publish(
        to_publish,
        extra=current_app.app_context
    )

    return jsonify({})
# [END push]


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]
