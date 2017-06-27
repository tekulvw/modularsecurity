from flask.views import MethodView
from flask_login import current_user, login_required


class Home(MethodView):
    def get(self):
        if current_user.is_authenticated:
            return "Hello {} {}!".format(current_user.fname, current_user.lname)
        else:
            return "Hello!"
