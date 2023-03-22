

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from OnlyHands import countdown


def initialize():
    cred = credentials.Certificate('key.json')
    firebase_admin.initialize_app(cred,{
        'databaseURL': 'https://ia-trauma-tfm-default-rtdb.europe-west1.firebasedatabase.app/'
    })


def getlogindata():
    login_ref=db.reference("/Login/")
    uid_ref=login_ref.child(countdown.GlobalVars.uid)
    login_data=uid_ref.get()
    countdown.GlobalVars.nombre=login_data['nombre']
    createnewflexion()

def createnewflexion():
    flexion_ref=db.reference("/Flexion/")
    new_flexion_ref= flexion_ref.push({
    'dorsal': 0,
    'fecha': countdown.GlobalVars.date,
    'paciente': countdown.GlobalVars.uid,
    'palmar':0,
    'tutorial':1
    })
    new_session_uid = new_flexion_ref.key
    countdown.GlobalVars.uid_session=str(new_session_uid)

def updateflexiondata(palmdor):
    flexions_ref = db.reference("/Flexion/")
    flexion_ref=flexions_ref.child(countdown.GlobalVars.uid_session)
    if(palmdor=='palmar'):
        flexion_ref.child('palmar').set(countdown.GlobalVars.palmar)
    else:
        flexion_ref.child('dorsal').set(countdown.GlobalVars.dorsal)
    print('value successfully updated in fb')


