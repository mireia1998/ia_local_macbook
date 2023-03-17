

import cv2
import angle

def setFrameSize(capp):
    cv = capp
    cv.set(3, 1280)
    cv.set(4, 650)
    return cv

def getFrameSize(capp):

    width = capp.get(3)  # float `width`
    height = capp.get(4)  # float `height`

    return width, height


def handDetect(mp_hands, cap, mp_drawing,joint1,joint2,mode, width, height):
    joint_list1 = [[joint1, joint2]]  # estos son los marcadores de muñeca (0) y 5to meta (17)a (3r meta 9)

    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
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
            results = hands.process(image)
            # Poner flag a True
            image.flags.writeable = True
            # Pasar de RGB a BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            # Detecciones
            # print(results)
            # Renderizar resultados
            if results.multi_hand_landmarks:
                for num, hand in enumerate(results.multi_hand_landmarks):
                    mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(150, 22, 150), thickness=2,
                                                                     circle_radius=4),
                                              mp_drawing.DrawingSpec(color=(150, 200, 250), thickness=2,
                                                                     circle_radius=2),
                                              )
                angle.angulosdedos(image, results, joint_list1, handtype, width, height)

            cv2.imshow('Midiendo...', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                pass
                #main.main()
    cap.release()
    cv2.destroyAllWindows()