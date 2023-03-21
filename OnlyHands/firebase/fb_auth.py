import requests
import json
import PySimpleGUI as sg


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class FirebaseUtils:

    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    api_key="AIzaSyDwPXa83bc7WMxQHYa256H-2TUYwS62_Pg"




def sign_in_with_email_and_password(email: str, password: str, return_secure_token: bool = True):
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": return_secure_token
    })

    r = requests.post(FirebaseUtils.rest_api_url,
                      params={"key": FirebaseUtils.api_key},
                      data=payload)

    return r
def initialize():
    cred = credentials.Certificate('key.json')
    firebase_admin.initialize_app(cred)


def getlogindata():
    login_ref=db.reference('Login')
    login_data=login_ref.get()
    user_ref=login_ref.child('pu9nTg5XP4WdGzFkLRXlp6emETQ2')
    print(str(user_ref))
def authenticate(user,password):
    ok=0
    token = sign_in_with_email_and_password(user,password)
    if token.status_code == 200:
        # Authentication successful
        print("User authenticated")
        ok=1
        initialize()
        sg.popup_ok('Autenticación correcta')
    else:
        # Authentication failed
        error_message = token.json()["error"]["message"]
        if error_message == "INVALID_PASSWORD":
            sg.popup_ok('Contraseña incorrecta')

        elif error_message == "EMAIL_NOT_FOUND":
            sg.popup_ok('El usuario no existe')
        else:
            print("Authentication failed for unknown reason")
            sg.popup_ok('Autenticación fallida')

    return ok
