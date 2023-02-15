'''
Author: Andrino Machado Cauduro
Date: 2022-10-25
Version: 0.7
About: Automation to send message to a discord friend
'''

import time ##Sleep
import sys
import os
import socket
import threading
from pygame import mixer as mx ##Sound effects
import PySimpleGUI as sg ##UI
import pyautogui as auto ##Automation
import pyperclip as pc ##To deal with special characters
from tcp_latency import measure_latency

# Getting IP
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

class Tela:
    '''Class Tela, main class.'''
    def __init__(self):
        ##PySimpleGUI basic definition
        sg.theme('DarkAmber')
        layout = [
            [sg.Text(size=(12,1), justification='left', key='Latencia')],
            [sg.HorizontalSeparator()],
            [sg.Text('Alvo:'), sg.Input(size=48, key='target')],
            [sg.HorizontalSeparator()],
            [sg.Text('Texto:'), sg.Multiline(size=(50,8), key='text', no_scrollbar=True)],
            [sg.HorizontalSeparator()],
            [sg.CBox('Sounds', key='fx', default=True),
            sg.Button('Clear', button_color='red'),
            sg.Button('Send', button_color='blue')]
            ]

        window = sg.Window('Discord bot', layout,
        margins=(25,15),
        finalize = True)

        ##Enter will return _Advance event on "target" (does not affect it's value)
        window['target'].bind("<Return>", "_Advance")
        window['text'].bind("<Shift-Tab>", "_Return")

        ##Images used for automation
        img = ["taskbar.png", "home.png", "friends.png", "search.png"]

        ##Points to the .py current location, resources folder must be in the same directory
        filepath = os.path.dirname(os.path.realpath(__file__))

        #self.event = window.read(timeout = 1)
        self.latency_thread(window)

        ##Main loop
        while True:
            events, values = window.read()
            if events == "target"+"_Advance":
                window.Element('text').SetFocus()
            if events == "text"+"_Return":
                window.Element('target').SetFocus()
            if events == 'Clear':
                window['target'].Update('')
                window['text'].Update('')
                window.Element('target').SetFocus()
            if events == sg.WINDOW_CLOSED:
                quit()
            if events == 'Send':
                if values['fx']:
                    mx.init() ##Starting pygame mixer
                    mx.music.load(filepath+"\\resources\\sounds\\go.wav")
                    mx.music.play()
                coord = None
                auto.press('win')
                time.sleep(1)
                auto.write('discord')
                auto.press('enter')
                ##Search for images in the array in order to get to the friends tab
                for i in range(4):
                    coord = auto.locateCenterOnScreen(filepath+"\\resources\\images\\"+img[i],
                    grayscale=True,
                    confidence=0.8)
                    print("Image: " + img[i] + " Located.")
                    auto.moveTo(coord)
                    auto.click()
                ##Copying target to be sent, that way it will work with special characters
                pc.copy(values['target'])
                auto.hotkey("ctrl", "v")
                auto.press('enter')
                for i in range(3):
                    auto.press('tab')
                auto.press('enter')
                time.sleep(1)
                pc.copy(values['text'])
                auto.hotkey("ctrl", "v")
                auto.press('enter')
                time.sleep(1)
                pc.copy('') ##Clearing clipboard
                quit()
    # Latency Update Method
    def late_update(self, window):
        '''Late update'''
        while True:
            ping = (float(measure_latency(host="brazil6726.discord.gg")[0]))
            window['Latencia'].update("Latência: %.2f" %ping)

    def latency_thread(self, window):
        '''Latency Thread'''
    # Multithreading Latency method
        try:
            threading.Thread(target=self.late_update, args=(window,),daemon=True).start()
        except SystemExit:
            sys.exit()
tela = Tela()
