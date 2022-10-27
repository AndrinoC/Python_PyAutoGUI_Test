'''
Author: Andrino Machado Cauduro
Date: 2022-10-25
Version: 0.5
About: Annoy your friends
'''

from pygame import mixer as mx ##Sound effects
import PySimpleGUI as sg ##UI
import pyautogui as auto ##Automation
import pyperclip as pc ##To deal with special characters
import time ##Sleep

##PySimpleGUI basic definition
sg.theme('DarkAmber')
layout = [[sg.Text('Target:'), sg.Input(key='target')],[sg.Text('Message:', size=9), sg.Multiline(size=(50,8), key='text', no_scrollbar=True)], [sg.Button('Clear', button_color='red')], [sg.Button('Send', button_color='blue')]]
window = sg.Window('Discord bot', layout, finalize = True, element_justification='c')
window['target'].bind("<Return>", "_Advance") ##Enter will return _Advance event on "target" (does not affect it's value)
window['text'].bind("<Shift-Tab>", "_Return")

img = ["home.png", "home2.png", "friends.png"] ##Images used for automation 

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
        pc.copy(values['text']) ##Copying text to be sent, that way it will work with special characters
        mx.init() ##Starting pygame mixer
        mx.music.load(".\\resources\\sfx\\go.wav")
        mx.music.play()
        auto.press('win')
        auto.write('discord') ##Opening discord
        auto.press('enter')
        coord = None
        while coord == None:
            for i in range(len(img)): ##Search for images in the array in order to get to the friends tab
                coord = auto.locateCenterOnScreen(".\\resources\\image_detection\\"+img[i])
                auto.moveTo(coord)
                auto.click()
        auto.write(values['target']) ##Searching target on friendlist
        time.sleep(1)
        auto.press('tab') ##Opening target's chat
        auto.press('enter')
        time.sleep(1)
        auto.hotkey("ctrl", "v") ##Pasting text
        auto.press('enter')
        time.sleep(1)
        pc.copy('') ##Clearing clipboard
        quit()