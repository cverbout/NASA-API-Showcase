from flask import render_template
from flask.views import MethodView

class Index(MethodView):
    def get(self):
        """
        Renders index.html page
        """
        return render_template('index.html')

