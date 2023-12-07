import flask
from index import Index

from map import Map
from apod import Apod

app = flask.Flask(__name__)       # our Flask app

# Main landing page
app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])


# Show map of entries
app.add_url_rule('/map',
                 view_func=Map.as_view('map'),
                 methods=['GET'])

# Show map of entries
app.add_url_rule('/apod',
                 view_func=Apod.as_view('apod'),
                 methods=['GET'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
