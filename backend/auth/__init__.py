from flask import session


def initialize_tokengetter(auth_obj):
    @auth_obj.tokengetter
    def tokengetter():
        auth_resp = session.get("authorization")
        if auth_resp:
            return auth_resp["access_token"], ''
        return None
