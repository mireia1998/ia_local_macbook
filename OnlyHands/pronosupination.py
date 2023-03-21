import cv2
from math import atan2, cos, sin, sqrt, pi
import numpy as np
import PySimpleGUI as sg
import angle
import countdown

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
def main2():

    cap = cv2.VideoCapture(0)  # para capturar video desde cámara
    cap=setFrameSize(cap)

    createguimenu(cap)

def createguimenu(cap):
    # Crear layout
    layout = [[sg.Text("¿Que boligrafo vas a usar?")], [sg.Button("Azul")], [sg.Button("Rosa")], [sg.Button("Amarillo")] ]
    # Crear la ventana
    window = sg.Window("App de IA traumatología", layout, margins=(100, 50), element_justification='c')
    while True:
        event, values = window.read()
        if event == "OK" or event == sg.WIN_CLOSED:
            break
        elif event == "Azul":
            lower_bound = np.array([80, 150, 100])
            upper_bound = np.array([120, 255, 255])
            bucle(cap,upper_bound,lower_bound)
        elif event == "Rosa":
            lower_bound = np.array([140, 150, 100])
            upper_bound = np.array([175, 255, 255])
            bucle(cap,upper_bound,lower_bound)
        elif event == "Amarillo":
            lower_bound = np.array([15, 120, 100])
            upper_bound = np.array([35, 255, 255])
            bucle(cap,upper_bound,lower_bound)
    window.close()

def setFrameSize(capp):
    cv=capp
    cv.set(3, 1280)
    cv.set(4, 650)
    return cv

def drawAxis(img, p_, q_, color, scale):
    p = list(p_)
    q = list(q_)

    ## [visualization1]
    angle = atan2(p[1] - q[1], p[0] - q[0])  # angle in radians
    hypotenuse = sqrt((p[1] - q[1]) * (p[1] - q[1]) + (p[0] - q[0]) * (p[0] - q[0]))

    # Here we lengthen the arrow by a factor of scale
    q[0] = p[0] - scale * hypotenuse * cos(angle)
    q[1] = p[1] - scale * hypotenuse * sin(angle)
    cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)

    # create the arrow hooks
    p[0] = q[0] + 9 * cos(angle + pi / 4)
    p[1] = q[1] + 9 * sin(angle + pi / 4)
    cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)

    p[0] = q[0] + 9 * cos(angle - pi / 4)
    p[1] = q[1] + 9 * sin(angle - pi / 4)
    cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)
    ## [visualization1]


def getOrientation(pts, img):
    ## [pca]
    # Construct a buffer used by the pca analysis
    sz = len(pts)
    data_pts = np.empty((sz, 2), dtype=np.float64)
    for i in range(data_pts.shape[0]):
        data_pts[i, 0] = pts[i, 0, 0]
        data_pts[i, 1] = pts[i, 0, 1]

    # Perform PCA analysis
    mean = np.empty((0))
    mean, eigenvectors, eigenvalues = cv2.PCACompute2(data_pts, mean)

    # guardamos el centro del objeto
    cntr = (int(mean[0, 0]), int(mean[0, 1]))

    cv2.circle(img, cntr, 3, (255, 0, 255), 2)
    p1 = (
    cntr[0] + 0.02 * eigenvectors[0, 0] * eigenvalues[0, 0], cntr[1] + 0.02 * eigenvectors[0, 1] * eigenvalues[0, 0])
    p2 = (
    cntr[0] - 0.02 * eigenvectors[1, 0] * eigenvalues[1, 0], cntr[1] - 0.02 * eigenvectors[1, 1] * eigenvalues[1, 0])
    drawAxis(img, cntr, p1, (255, 255, 0), 1)
    drawAxis(img, cntr, p2, (0, 0, 255), 5)

    angle = atan2(eigenvectors[0, 1], eigenvectors[0, 0])  # orientation in radians
    countdown.GlobalVars.measType = 4

    # Ponemos la etiqueta
    #label = "  Rotacion: " + str(-int(np.rad2deg(angle)) - 90) + " grados"
    #textbox = cv2.rectangle(img, (cntr[0], cntr[1] - 25), (cntr[0] + 250, cntr[1] + 10), (255, 255, 255), -1)
    #cv2.putText(img, label, (cntr[0], cntr[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    angok=(-int(np.rad2deg(angle)) - 90)

    angleprocess(img, angok, cntr)


    return angle

def angleprocess(image, angle,cntr):

    angle=abs(angle)
    angle=abs(180-angle)

    print(str(angle))
    if not countdown.GlobalVars.event.is_set() and countdown.GlobalVars.registered == False:  # aun no es cero

        if (round(angle) < 5):
            label = "Ready, wait..."
            textbox = cv2.rectangle(image, (cntr[0], cntr[1] - 25), (cntr[0] + 250, cntr[1] + 10), (255, 255, 255), -1)
            cv2.putText(image, label, (cntr[0], cntr[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

            if not countdown.GlobalVars.stop_event.is_set():
                countdown.hiloconteo(3)
            else:
                countdown.GlobalVars.stop_event.clear()
        else:
            countdown.GlobalVars.stop_event.set()
            label = "Please move to 0 deg"
            textbox = cv2.rectangle(image, (cntr[0], cntr[1] - 25), (cntr[0] + 250, cntr[1] + 10), (255, 255, 255), -1)
            cv2.putText(image, label, (cntr[0], cntr[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    elif countdown.GlobalVars.registered == False:  # ya es cero

        if (round(angle) < 5):
            label = "Mueve tu mano..."
            textbox = cv2.rectangle(image, (cntr[0], cntr[1] - 25), (cntr[0] + 250, cntr[1] + 10), (255, 255, 255), -1)
            cv2.putText(image, label, (cntr[0], cntr[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        else:
            label = "  Rotacion: " + str(angle) + " grados"
            textbox = cv2.rectangle(image, (cntr[0], cntr[1] - 25), (cntr[0] + 250, cntr[1] + 10), (255, 255, 255), -1)
            cv2.putText(image, label, (cntr[0], cntr[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            # aqui programamos la lógica de almacenamiento de ángulo
            countdown.processnumber(angle)
    else:
        if countdown.GlobalVars.ready == 0:
            countdown.GlobalVars.ready = 1
            countdown.mostrarresultado(angle, 0)
            countdown.GlobalVars.event.clear()
            countdown.GlobalVars.registered = False


def bucle(cap, upper_bound,lower_bound):

    while(1):
        ret,frame=cap.read()


        ##extracode
        # convertir a espacio de colores hsv
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # limites superior/inferior para color verde
        #lower_bound = np.array([80, 199, 90])
       # upper_bound = np.array([120, 255, 255])
        #lower_bound = np.array([10, 100, 20])
        #upper_bound = np.array([25, 255, 255])

        # buscar los colores en los limites
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        #####2. Quitar ruido de la máscara####

        # definir tamaño de kernel
        kernel = np.ones((7, 7), np.uint8)

        ##quitar ruido innecesario
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        #####3. Aplicar máscara a la imagen####

        # segmentar la region detectada
        segmented_img = cv2.bitwise_and(frame, frame, mask=mask)
        ##extracode

        # Find all the contours in the thresholded image
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        for i, c in enumerate(contours):

            # Calculate the area of each contour
            area = cv2.contourArea(c)

            # Ignore contours that are too small or too large
            if area < 3700 or 100000 < area:
                continue

            # Draw each contour only for visualisation purposes
            cv2.drawContours(frame, contours, i, (0, 0, 255), 2)

            # Find the orientation of each shape
            getOrientation(c, frame)

        cv2.imshow('Midiendo...', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            pass
    cap.release()
    cv2.destroyAllWindows()
