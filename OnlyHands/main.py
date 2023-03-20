import sys

import mediapipe as mp
import cv2
import numpy as np
import time
import uuid
import os
import PySimpleGUI as sg
import angle
import frame as f
import pronosupination as ps


# Funcion bucle principal
def main():
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    cap = cv2.VideoCapture(0)  # para capturar video desde cámara
    cap = f.setFrameSize(cap)
    width, height = f.getFrameSize(cap)
    createLoginPage(mp_drawing, mp_hands, cap, width, height)


def iniciarSesion(usuario, nip):
    correct = 0
    if (usuario == "" or nip == ""):
        sg.popup_error('Debes rellenar los campos')
    else:
        if (usuario == "sener" and nip == "sener"):
            sg.popup_ok('Inicio de sesion correcto')
            correct = 1
        else:
            sg.popup_error('Usuario o contraseña incorrectos')
            correct = 0
    return correct


def createLoginPage(mp_drawing, mp_hands, cap, width, height):
    # sg.theme('DarkPurple1')

    # Crear layout
    layout = [
        [sg.Image(filename='sener_small-2.png')],
        [sg.Text('Usuario:', size=(100, 1))],
        [sg.InputText('', pad=((0, 0), (0, 10)), key='user')],
        [sg.Text('Contraseña:', size=(100, 1))],
        [sg.InputText('', pad=((0, 0), (0, 10)), password_char="*", key='nip')],
        [sg.Button('Iniciar Sesión', key='login'), sg.Button('Cancelar', key='close')]
    ]
    window = sg.Window("Login", layout, size=(230, 230))
    while True:
        event, values = window.read()
        if event == "close" or event == sg.WIN_CLOSED:
            break
        elif event == 'login':
            valido = iniciarSesion(values['user'], values['nip'])
            if valido == 1:
                window.close()
                createguimenu(mp_drawing, mp_hands, cap, width, height)
    window.close()


def createguimenu(mp_drawing, mp_hands, cap, width, height):
    # sg.theme('DarkPurple1')

    # Crear layout
    layout = [[sg.Button("Mi perfil")]
                , [sg.Button("Tutoriales de uso")],
              [sg.Button("Flexión Dorsal y Palmar")],
              [sg.Button("Aducción/abducción de muñeca")], [sg.Button("Prono/Supinación de muñeca")],
               [sg.Image(filename='sener_small-2.png')]
              ]
    # Crear la ventana
    window = sg.Window("Menú principal", layout, margins=(100, 50), element_justification='c')
    while True:
        event, values = window.read()
        if event == "OK" or event == sg.WIN_CLOSED:
            break
        elif event == "Flexión Dorsal y Palmar":
            f.handDetect(mp_hands, cap, mp_drawing, 0, 17, 0, width, height)
        elif event == "Aducción/abducción de muñeca":
            f.handDetect(mp_hands, cap, mp_drawing, 0, 9, 1, width, height)
        elif event == "Prono/Supinación de muñeca":
            # Aqui conectamos al otro módulo
            ps.main2()
    window.close()


main()
