import PySimpleGUI as sg

from OnlyHands import countdown


def main3():
    creategui()


def creategui():
    # Crear layout
    layout = [[sg.Text("Bienvenido/a, "+countdown.GlobalVars.nombre)],
              [sg.Text("Tu doctor/a es" + countdown.GlobalVars.docname)],
              [sg.Text("Del hospital de" + countdown.GlobalVars.hospi)],
              [sg.Button("Mis mediciones")],
              [sg.Button("Acerca de")]]
    # Crear la ventana
    window = sg.Window("Mi perfil", layout, margins=(100, 50), element_justification='c')
    while True:
        event, values = window.read()
        if event == "OK" or event == sg.WIN_CLOSED:
            break
        elif event == "Mis mediciones":
            pass
        elif event == "Acerca de":
            pass
    window.close()
