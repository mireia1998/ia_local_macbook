import requests
import json
import PySimpleGUI as sg
from OnlyHands import countdown

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from OnlyHands.firebase import fb_rtdb


class FirebaseUtils:

    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    api_key="AIzaSyDwPXa83bc7WMxQHYa256H-2TUYwS62_Pg"
    realtime_url="https://ia-trauma-tfm-default-rtdb.europe-west1.firebasedatabase.app/"


def extractUIDfromHTTPResponse(response):
    response_body = response.content.decode('utf-8')
    response_json = json.loads(response_body)
    local_id = response_json['localId']
    countdown.GlobalVars.uid=str(local_id)


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



def authenticate(user,password):
    ok=0
    token = sign_in_with_email_and_password(user,password)
    print(str(token.json()))
    if token.status_code == 200:
        # Authentication successful
        print("User authenticated")
        ok=1
        fb_rtdb.initialize()
        extractUIDfromHTTPResponse(token)
        fb_rtdb.getlogindata()
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
