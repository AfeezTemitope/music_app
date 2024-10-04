import os

import firebase_admin
from firebase_admin import credentials
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from urls import badify


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
cred = credentials.Certificate('securityAccountKey.json')
firebase_admin.initialize_app(cred)
app.register_blueprint(badify)

if __name__ == '__main__':
    app.run()
