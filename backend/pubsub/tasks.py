from google.appengine.api.app_identity import get_application_id
from flask import current_app

from google.cloud import pubsub


__all__ = [
    "client",
    "get_system_topic",
    "get_all_system_topic",
    "get_all_system_pushsub"
]

client = None

TOPIC_FMT = "system/{}"


def create_client(project=None):
    """
    Creates Google PubSub client.
    :param project:
    :return:
    """
    project = project or get_application_id()
    global client
    client = pubsub.Client(project)
    return client


def create_pushsub(topic, sub_name, endpoint):
    """
    Creates a push sub of topic to endpoint.
    :param sub_name: Name of subscriber
    :param topic: Topic object
    :param endpoint: URL endpoint to hit.
    :return: Subscription object
    """
    sub = topic.subscription(sub_name, push_endpoint=endpoint)
    if not sub.exists():
        sub.create()
    return sub


def get_all_system_pushsub(endpoint):
    """
    Gets a pushsub that subscribes to all data input.
    :param endpoint: URL endpoint to hit.
    :return: Subscription object
    """
    topic = get_all_system_topic()
    return create_pushsub(topic, "ALL_SYSTEM", endpoint)


def get_all_system_topic():
    """
    Returns the topic that receives all device data.
    :return:
    """
    topic_name = TOPIC_FMT.format("ALL_SYSTEMS")
    topic = client.topic(topic_name)
    if not topic.exists():
        topic.create()
    return topic


def get_system_topic(system):
    """
    Gets the topic for a given system.
    :param system: Datastore object
    :return: topic object
    """
    topic_name = TOPIC_FMT.format(system.key.integer_id())
    topic = client.topic(topic_name)
    if not topic.exists():
        topic.create()
    return topic
