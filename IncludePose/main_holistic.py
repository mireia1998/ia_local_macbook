import math
import sys
import mediapipe as mp
import cv2
import numpy as np
import PySimpleGUI as sg

handConnectionPose=[(14,16)]
handConnectionHandFlexext=[(0,17)]
isZero=0

def setFrameSize(capp):
    cv = capp
    cv.set(3, 1280)
    cv.set(4, 650)
    return cv

def getFrameSize(capp):

    width = capp.get(3)  # float `width`
    height = capp.get(4)  # float `height`

    return width, height

#Funcion bucle principal
def main():
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    mp_holistic=mp.solutions.holistic
    cap = cv2.VideoCapture(0)  # para capturar video desde cámara
    cap = setFrameSize(cap)
    width, height = getFrameSize(cap)
    createguimenu(mp_drawing,mp_hands,cap,mp_holistic, width,height)


def createguimenu(mp_drawing,mp_hands,cap,mp_holistic,width,height):
    # Crear layout
    layout = [[sg.Text("¿Que te gustaría medir?")], [sg.Button("Flexión Dorsal y Palmar")],
              [sg.Button("Desviación radial/cubital")], [sg.Button("Prono/Supinación de muñeca")]]
    # Crear la ventana
    window = sg.Window("App de IA traumatología", layout, margins=(100, 50), element_justification='c')
    while True:
        event, values = window.read()
        if event == "OK" or event == sg.WIN_CLOSED:
            break
        elif event == "Flexión Dorsal y Palmar":
            armBodyDetect(mp_holistic,cap,mp_drawing,0,0,width,height)
        elif event == "Desviación radial/cubital":
            armBodyDetect(mp_holistic,cap,mp_drawing,1,0,width,height)
        elif event == "Prono/Supinación de muñeca":
            pass
    window.close()

def setFrameSize(capp):
    cv=capp
    cv.set(3, 1280)
    cv.set(4, 650)
    return cv

def desvradcubital(image, results, joint_list,handtype,width,height):
    if(handtype==0):
        a = np.array([results.pose_landmarks.landmark[13].x, results.pose_landmarks.landmark[13].y])
        b = np.array([results.left_hand_landmarks.landmark[0].x, results.left_hand_landmarks.landmark[0].y])
        c = np.array([results.left_hand_landmarks.landmark[9].x, results.left_hand_landmarks.landmark[9].y])

        radians = np.arctan2((results.left_hand_landmarks.landmark[9].y - results.left_hand_landmarks.landmark[0].y),
                             (results.left_hand_landmarks.landmark[9].x - results.left_hand_landmarks.landmark[0].x))
        angle180 = np.abs(radians * 180.0 / np.pi)
        angle = abs(180.0 - angle180)
    else:
        a= np.array([results.pose_landmarks.landmark[14].x, results.pose_landmarks.landmark[14].y])
        b = np.array([results.right_hand_landmarks.landmark[0].x, results.right_hand_landmarks.landmark[0].y])
        c = np.array([results.right_hand_landmarks.landmark[9].x, results.right_hand_landmarks.landmark[9].y])

        radians = np.arctan2((results.right_hand_landmarks.landmark[9].y - results.right_hand_landmarks.landmark[0].y),
                             (results.right_hand_landmarks.landmark[9].x - results.right_hand_landmarks.landmark[0].x))

    horizon = tuple(np.multiply(a, [width, 0]).astype(int))
    angle = np.abs(radians * 180.0 / np.pi)
    puntoa1 = tuple(np.multiply(a, [width,height]).astype(int)) # codos
    puntob1 =tuple(np.multiply(b, [width,height]).astype(int)) # muñeca
    puntoc1 = tuple(np.multiply(c, [width,height]).astype(int)) #3er meta

    # ploteo de lineas
    cv2.line(image, puntoa1, horizon, (0, 255, 0), thickness=2, lineType=8) #del codo al horizonte
    cv2.line(image, puntoa1, puntob1, (0, 255, 0), thickness=2, lineType=8) #del codo a la muñeca
    cv2.line(image, puntob1, puntoc1, (0, 255, 0), thickness=2, lineType=8)  #de la muñeca al 3er meta

    # y aqui ponemos grados entre los markers de la mano
    cv2.putText(image, str(round(angle)) + " grados", tuple(np.multiply(a, [1000, 650]).astype(int)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (240, 29, 0), 2, cv2.LINE_AA)



def flexoextension(image, results, joint_list,handtype,width,height):
    if(handtype==0):
        a = np.array([results.pose_landmarks.landmark[13].x, results.pose_landmarks.landmark[13].y])
        horizon = tuple(np.multiply(a, [0, height]).astype(int))
        b = np.array([results.left_hand_landmarks.landmark[0].x, results.left_hand_landmarks.landmark[0].y])
        c = np.array([results.left_hand_landmarks.landmark[17].x, results.left_hand_landmarks.landmark[17].y])

        radians = np.arctan2((results.left_hand_landmarks.landmark[17].y - results.left_hand_landmarks.landmark[0].y),
                             (results.left_hand_landmarks.landmark[17].x - results.left_hand_landmarks.landmark[0].x))
        angle180 = np.abs(radians * 180.0 / np.pi)
        angle=abs(180.0 - angle180)
    else:
        a= np.array([results.pose_landmarks.landmark[14].x, results.pose_landmarks.landmark[14].y])
        horizoni = tuple(np.multiply(a, [1, height]).astype(int))
        hlist=list(horizoni)
        hlist[0]=1600
        horizon=tuple(hlist)
        b = np.array([results.right_hand_landmarks.landmark[0].x, results.right_hand_landmarks.landmark[0].y])
        c = np.array([results.right_hand_landmarks.landmark[17].x, results.right_hand_landmarks.landmark[17].y])

        radians = np.arctan2((results.right_hand_landmarks.landmark[17].y - results.right_hand_landmarks.landmark[0].y),
                             (results.right_hand_landmarks.landmark[17].x - results.right_hand_landmarks.landmark[0].x))
        angle = np.abs(radians * 180.0 / np.pi)




    # los tres puntos pasados de mp a Opencv
    puntoa1 = tuple(np.multiply(a, [width,height]).astype(int)) #epicondilo lateral
    puntob1 =tuple(np.multiply(b, [width,height]).astype(int)) #muñeca
    puntoc1 = tuple(np.multiply(c, [width,height]).astype(int)) #5to meta

    # ploteo de lineas
    print(width)
    cv2.line(image, puntoa1, horizon, (0, 255, 0), thickness=2, lineType=8) #del codo al horizonte
    cv2.line(image, puntoa1, puntob1, (0, 255, 0), thickness=2, lineType=8) #del codo a la muñeca
    cv2.line(image, puntob1, puntoc1, (0, 255, 0), thickness=2, lineType=8)  #de la muñeca al 5to meta

    if (round(angle) < 3):
        cv2.putText(image, "ready, angle is 0deg", tuple(np.multiply(b, [width, height]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
        isZero=1
    else:
        cv2.putText(image, str(round(angle)) + " grados", tuple(np.multiply(a, [1000, 650]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (240, 29, 0), 2, cv2.LINE_AA)




def armBodyDetect(mp_holistic, cap, mp_drawing,movement,mode,width,height):
    joint_list1 = [[11, 13,15]]  # estos son los marcadores de muñeca (0) y 5to meta (17)a (3r meta 9)

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            ret, frame = cap.read()
            handtype = mode
            # Pasar de BGR a RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Girar horizontalmente
            image = cv2.flip(image, 1)
            # Poner flag a False
            image.flags.writeable = False
            # Detección
            results = holistic.process(image)
            # Poner flag a True
            image.flags.writeable = True
            # Pasar de RGB a BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            # Detecciones
            # print(results)
            # Renderizar resultados
            if results.right_hand_landmarks is not None:
                mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(150, 22, 150), thickness=2,
                                                                 circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(150, 200, 250), thickness=2,
                                                                 circle_radius=2),
                                          )


            if results.left_hand_landmarks is not None:
                mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(150, 22, 150), thickness=2,
                                                                 circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(150, 200, 250), thickness=2,
                                                                 circle_radius=2),
                                                )



            if results.pose_landmarks is not None:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, handConnectionPose,
                                          mp_drawing.DrawingSpec(color=(150, 22, 150), thickness=2,
                                                                 circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(150, 200, 250), thickness=2,
                                                                 circle_radius=2),
                                          [13,14])

            if (results.pose_landmarks is not None) and (results.left_hand_landmarks is not None) and movement == 0:
                #flexoextension(image,results,joint_list1,0,width,height)
                pass

            if (results.pose_landmarks is not None) and (results.right_hand_landmarks is not None) and movement == 0:
                flexoextension(image,results,joint_list1,1,width,height)

            if (results.pose_landmarks is not None) and (results.left_hand_landmarks is not None) and movement == 1:
                #desvradcubital(image, results, joint_list1, 0,width,height)
                pass

            if (results.pose_landmarks is not None) and (results.right_hand_landmarks is not None) and movement == 1:
                desvradcubital(image, results, joint_list1, 1,width,height)



            cv2.imshow('Midiendo...', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                # Si pulsas tecla q sales del programa
                main()
    cap.release()
    cv2.destroyAllWindows()


main()