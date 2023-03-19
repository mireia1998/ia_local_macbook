
import numpy as np
import cv2
import countdown

def angulosdedos(image, results, joint_list,handtype, width, height):
    for hand in results.multi_hand_landmarks:

        for joint in joint_list:
            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])
            b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y])
            radians=np.arctan2((hand.landmark[joint[1]].y - hand.landmark[joint[0]].y), (hand.landmark[joint[1]].x - hand.landmark[joint[0]].x))
            angle=np.abs(radians*180.0/np.pi)
            if handtype ==0: # si es flex/ext lo que se mide
                if angle>90:
                    angle=abs(angle-180)
            elif handtype ==1:
                angle= abs(90-angle)
            elif handtype ==2:
                angle= abs(90-angle)

            #Pasar puntos de formato mediapipe a OpenCV y crear el horizonte
            puntoa1=tuple(np.multiply(a, [width, height]).astype(int))
            puntob1=tuple(np.multiply(b, [width, height]).astype(int))
            if handtype==0:# Midiendo flexoextension,
                ##Horizonte
                horizon = tuple(np.multiply(a, [0, height]).astype(int))
                ##Horizonte invertido
                horizoninv = tuple(np.multiply(a, [1, height]).astype(int))
                horizoninvlist=list(horizoninv)
                horizoninvlist[0]=1600
                horizoninv=tuple(horizoninvlist)
                cv2.line(image, puntoa1, horizoninv, (0, 255, 0), thickness=2, lineType=8)
            else:
                ##Solo necesitamos horizonte normal
                horizon = tuple(np.multiply(a, [width, 0]).astype(int))

            #ploteo de la linea eje x horizontal
            cv2.line(image, puntoa1, horizon, (0,255,0), thickness=2, lineType=8)
            #ploteo de la linea que une los markers
            cv2.line(image, puntoa1, puntob1, (0, 255, 0), thickness=2, lineType=8)

            if not countdown.GlobalVars.event.is_set() and countdown.GlobalVars.registered==False: # aun no es cero
                if (round(angle) < 3) :
                    countdown.GlobalVars.stopFlag == 0
                    cv2.putText(image, "ready, angle is 0deg", tuple(np.multiply(b, [width, height]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
                    if(countdown.GlobalVars.started==0):
                        countdown.hiloconteo(3)
                        countdown.GlobalVars.started=1
                else:
                    cv2.putText(image, "please move to 0 deg", tuple(np.multiply(a, [1000, 650]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (240, 29, 0), 2, cv2.LINE_AA)
                    countdown.GlobalVars.stopFlag==1
                    countdown.GlobalVars.started = 0
            elif countdown.GlobalVars.registered==False : # ya es cero

                if (round(angle) < 3):
                    cv2.putText(image, "Dorsiflexiona tu mano...", tuple(np.multiply(b, [width, height]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
                else:
                    cv2.putText(image, str(round(angle)) + " degree",
                                tuple(np.multiply(a, [1000, 650]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (240, 29, 0), 2, cv2.LINE_AA)
                    # aqui programamos la lógica de almacenamiento de ángulo
                    countdown.processnumber(angle)
            else:
                print("Flexion medida, es " + str(countdown.GlobalVars.datomedio))

    return image