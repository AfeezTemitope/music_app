from flask import Blueprint

from views import get_google_client_id, login

badify = Blueprint('badify', __name__)


@badify.get('/google_client_id')
def google_client_id():
    return get_google_client_id()


@badify.post('/google_sign_in')
def google_sign_in():
    return login()
