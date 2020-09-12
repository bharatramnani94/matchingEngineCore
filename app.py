#!flask/bin/python

from flask import Flask
from routes import route_defs

app = Flask(__name__)
app.register_blueprint(route_defs)

if __name__ == '__main__':
    app.run(debug=True)
