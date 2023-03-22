

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
    'dorsalR': 0,
    'dorsalL': 0,
    'palmarR': 0,
    'palmarL': 0,
    'fecha': countdown.GlobalVars.date,
    'paciente': countdown.GlobalVars.uid,
    'tutorial':1
    })
    new_session_uid = new_flexion_ref.key
    countdown.GlobalVars.uid_session=str(new_session_uid)

def createnewdesviacion():
    flexion_ref=db.reference("/Desviacion/")
    new_flexion_ref= flexion_ref.push({
    'cubitalR': 0,
    'cubitalL': 0,
    'radialR': 0,
    'radialL': 0,
    'fecha': countdown.GlobalVars.date,
    'paciente': countdown.GlobalVars.uid,
    'tutorial':1
    })
    new_session_uid = new_flexion_ref.key
    countdown.GlobalVars.uid_session=str(new_session_uid)

def updateflexiondata(palmdor,value):
    flexions_ref = db.reference("/Flexion/")
    flexion_ref=flexions_ref.child(countdown.GlobalVars.uid_session)
    if(palmdor=='palmarL'):
        flexion_ref.child('palmarL').set(value)
    elif(palmdor=='palmarR'):
        flexion_ref.child('palmarR').set(value)
    elif (palmdor == 'dorsalL'):
        flexion_ref.child('dorsalL').set(value)
    elif (palmdor == 'dorsalR'):
        flexion_ref.child('dorsalR').set(value)
    else:
        flexion_ref.child('dorsalR').set(value)
    print('flexion successfully updated in fb...'+ countdown.GlobalVars.uid_session)

def updatedesviaciondata(cubirad,value):
    desviaciones_ref = db.reference("/Desviacion/")
    desviacion_ref=desviaciones_ref.child(countdown.GlobalVars.uid_session)
    desviacion_ref.child(cubirad).set(value)
    print('desviacion successfully updated in fb...'+ countdown.GlobalVars.uid_session)
