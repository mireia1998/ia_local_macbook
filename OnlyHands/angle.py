import numpy as np
import cv2
import countdown
import tkinter as tk
import PySimpleGUI as sg

def angulosdedos(image, results, joint_list,handtype, width, height):
    countdown.GlobalVars.lr = results.multi_handedness[0].classification[0].label
    for hand in results.multi_hand_landmarks:

        for joint in joint_list:
            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])
            b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y])
            radians=np.arctan2((hand.landmark[joint[1]].y - hand.landmark[joint[0]].y), (hand.landmark[joint[1]].x - hand.landmark[joint[0]].x))
            angle=np.abs(radians*180.0/np.pi)

            if(countdown.GlobalVars.lr=='Right'):
                angle=abs(180-angle)


            if(hand.landmark[joint[0]].y < hand.landmark[joint[1]].y):
                if(handtype==0):
                    countdown.GlobalVars.measType = 0
                else:
                    countdown.GlobalVars.measType = 2

            else:
                if(handtype==0):
                    countdown.GlobalVars.measType = 1
                else:
                    countdown.GlobalVars.measType = 3

            #Pasar puntos de formato mediapipe a OpenCV y crear el horizonte
            puntoa1=tuple(np.multiply(a, [width, height]).astype(int))
            puntob1=tuple(np.multiply(b, [width, height]).astype(int))

            ##Horizonte
            horizon = tuple(np.multiply(a, [0, height]).astype(int))
            ##Horizonte invertido
            horizoninv = tuple(np.multiply(a, [1, height]).astype(int))
            horizoninvlist=list(horizoninv)
            horizoninvlist[0]=1600
            horizoninv=tuple(horizoninvlist)
            cv2.line(image, puntoa1, horizoninv, (0, 255, 0), thickness=2, lineType=8)

            #ploteo de la linea eje x horizontal
            cv2.line(image, puntoa1, horizon, (0,255,0), thickness=2, lineType=8)
            #ploteo de la linea que une los markers
            cv2.line(image, puntoa1, puntob1, (0, 255, 0), thickness=2, lineType=8)

            image=angleprocess(image,angle,width, height, a, b)

    return image

def angleprocess(image, angle, width,height,a,b):
    if not countdown.GlobalVars.event.is_set() and countdown.GlobalVars.registered == False:  # aun no es cero

        if (round(angle) < 5):
            cv2.putText(image, "ready, wait...", tuple(np.multiply(b, [width, height]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
            if not countdown.GlobalVars.stop_event.is_set():
                countdown.hiloconteo(3)
            else:
                countdown.GlobalVars.stop_event.clear()
        else:
            countdown.GlobalVars.stop_event.set()
            cv2.putText(image, "please move to 0 deg", tuple(np.multiply(a, [1000, 650]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (240, 29, 0), 2, cv2.LINE_AA)

    elif countdown.GlobalVars.registered == False:  # ya es cero

        if (round(angle) < 3):
            cv2.putText(image, "mueve tu mano...", tuple(np.multiply(b, [width, height]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            cv2.putText(image, str(round(angle)) + " degree",
                        tuple(np.multiply(a, [1000, 650]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (240, 29, 0), 2, cv2.LINE_AA)
            # aqui programamos la lógica de almacenamiento de ángulo
            countdown.processnumber(angle)
    else:
        if countdown.GlobalVars.ready == 0:
            countdown.GlobalVars.ready = 1
            countdown.mostrarresultado(angle, 0)
            countdown.GlobalVars.event.clear()
            countdown.GlobalVars.registered = False

    return image