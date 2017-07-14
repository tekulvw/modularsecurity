from flask import current_app, request


def data_event_handler():
    data = request.get_json()
    print(request)
    return '', 204
