import os

from firebase_admin import auth
from flask import request, jsonify
from dotenv import load_dotenv
from google.auth.transport import requests
from google.auth.transport.requests import Request
from google.oauth2 import id_token

load_dotenv()

firebase_api_key = os.getenv('FIREBASE_API_KEY')
spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
google_client_id = os.getenv('GOOGLE_CLIENT_ID')


def get_google_client_id():
    return jsonify({'google_client_id': google_client_id})


def login():
    try:
        id_token_received = request.json.get('idToken')

        id_info = id_token.verify_oauth2_token(id_token_received, requests.Request())

        if id_info['aud'] != google_client_id:
            return jsonify({'error': 'Invalid client id'}), 401

        user_email = id_info['email']

        try:
            user = auth.get_user_by_email(user_email)
        except auth.UserNotFoundError:
            user = auth.create_user(email=user_email)

        return jsonify({'message': 'Login successful', 'user_email': user_email}), 200

    except ValueError:
        return jsonify({'error': 'Invalid token'}), 400


def verify_token():
    token = request.headers.get('Authorization').split(' ')[1]
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token['uid']
    except Exception as e:
        return jsonify({'error': 'Invalid Token'}), 401
