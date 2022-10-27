'''
Author: Andrino Machado Cauduro
Date: 2022-10-25
Version: 0.7
About: Automation to send message to a discord friend
'''

from pygame import mixer as mx ##Sound effects
import PySimpleGUI as sg ##UI
import pyautogui as auto ##Automation
import pyperclip as pc ##To deal with special characters
import time ##Sleep
import os

##PySimpleGUI basic definition
sg.theme('DarkAmber')
layout = [
    [sg.HorizontalSeparator()],
    [sg.Text('Target:'), sg.Input(size=48, key='target')],
    [sg.HorizontalSeparator()],
    [sg.Text('Text:'), sg.Multiline(size=(50,8), key='text', no_scrollbar=True)],
    [sg.HorizontalSeparator()],
    [sg.CBox('Sounds', key='fx', default=True), sg.Button('Clear', button_color='red'), sg.Button('Send', button_color='blue')]
    ]
window = sg.Window('Discord bot', layout, margins=(25,15), finalize = True, element_justification='c')
window['target'].bind("<Return>", "_Advance") ##Enter will return _Advance event on "target" (does not affect it's value)
window['text'].bind("<Shift-Tab>", "_Return")

img = ["taskbar.png", "home.png", "home2.png", "friends.png"] ##Images used for automation 
filepath = os.path.dirname(os.path.realpath(__file__)) ##Points to the .py current location, resources folder must be in the same directory

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
        while coord == None:
            for i in range(len(img)): ##Search for images in the array in order to get to the friends tab
                coord = auto.locateCenterOnScreen(filepath+"\\resources\\images\\"+img[i])
                auto.moveTo(coord)
                auto.click()
        pc.copy(values['target']) ##Copying target to be sent, that way it will work with special characters
        auto.hotkey("ctrl", "v") 
        time.sleep(1)
        auto.press('tab') ##Opening target's chat
        auto.press('enter')
        time.sleep(1)
        pc.copy(values['text']) 
        auto.hotkey("ctrl", "v") 
        auto.press('enter')
        time.sleep(1)
        pc.copy('') ##Clearing clipboard
        quit()