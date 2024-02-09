import datetime
import webbrowser as wb
import random
import os
import keyboard
import time
import smtplib
import pyautogui as pag
import threading
import glob
import subprocess

from plyer import notification
import BotConfig
import speech_recognition as sr
import pyttsx3
import win32gui
import win32.lib.win32con as win32con
import schedule
import psutil
import spacy

nlp = spacy.load("ru_core_news_sm")

def speak(text):
    engine = pyttsx3.init()
    engine
    engine.say(text)
    engine.runAndWait()

def Recognition():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Say something")
        audio = r.listen(source)

    try:
        print("Google Speech Recognition thinks you said " +
              r.recognize_google(audio, language="ru-RU"))
        return r.recognize_google(audio, language="ru-RU")
    except sr.UnknownValueError:
        speak("i am dont uderstand, please repeat")
    except sr.RequestError as e:
        speak("no have internet connection")

def analyze_intent(text):
    """
    Анализ интента команды пользователя с использованием SpaCy.

    :param text: текст команды пользователя
    :return: интент команды
    """
    doc = nlp(text)
    print(text)
    intent = None
    for token in doc:
        print(token)
        # Пример простого анализа интента на основе глаголов в предложении
        if token.pos_ == "VERB":
            intent = token.lemma_
            break
    return intent

def HelloWord(Username):
    """
    { function_description }

    :param      Username:  The username
    :type       Username:  { username eneterd from keyboard }
    """
    time = int(datetime.datetime.now().hour)

    if(time >= 12 and time < 18):
        speak(f"Good day {Username}")

    elif(time >= 5 and time < 12):
        speak(f"Good morning {Username}")

    else:
        speak(f"Good night {Username}")

def GetCommand(RecognitionData, UserName, command_name: str, *args: list):
    """
    Gets the command.

    :param      RecognitionData:  The recognition data
    :type       RecognitionData:  { Parse recognition voice }
    :param      UserName:         The user name
    :type       UserName:         { username eneterd from keyboard }
    :param      command_name:     The command name
    :type       command_name:     str
    :param      args:             The arguments
    :type       args:             list
    """
    intent = analyze_intent(command_name)
    print(intent)

    if intent:
        # Пример обработки интента "открыть браузер"
        if intent == "открыть":
            Bot.OpenBrowser()

        # Пример обработки интента "напомнить"
        elif intent == "напомнить":
            Bot.reminder()

        # Добавьте другие интенты и их обработку здесь
        else:
            speak("Я не понимаю эту команду")
    else:
        speak("Я не могу понять ваш запрос")

def OpenBrowser(*args: tuple):

    phrases = [
        "Open browser",
        "wait, i opening browser",
        "please, wait, i opening browser",
        ]
    speak(random.choice(phrases))

    if not args[0]:
        return

    search_term = " ".join(args[0])
    wb.open_new_tab(f"https://google.com/search?q={search_term}")

def AssistantOff(*args: tuple):
    """
    { Off assistant }

    :param      args:  The arguments
    :type       args:  tuple
    """
    phrases = [
        'goodbye',
        'byebye',
        "see you"
     ]
    speak(random.choice(phrases))
    os.abort()

def ComputerOff(*args: tuple):
    """
    { Off your device }

    :param      args:  The arguments
    :type       args:  tuple
    """
    phrases = [
        "Shutdown",
        "i am shutdown your pc"
     ]
    speak(random.choice(phrases))

    os.system("shutdown -s -t 10")

def sendMail(*args: tuple):
    """
    Sends a mail.

    :param      args:  The arguments
    :type       args:  tuple
    """

    phrases = [
        "preparing a letter to send",
        "will send soon",
        "Visage is already carrying your letter"
    ]
    if not args[0]:
        return

    Get = BotConfig.EmailForm()
    Info = Get.InputEmail()
    sender, password = Info[0], Info[1]

    if '@gmail.' in sender:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

    elif '@yandex.' in sender:
        server = smtplib.SMTP_SSL('smtp.yandex.com', 465)

    elif '@mail.' in sender:
        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        # mail.ru pass xDfEuWPtwsyfHzJS1vXs
        # mail.ru logi vdvachevsky@mail.ru

    else:
        speak("Unknown mail")
        return

    valueString = ''
    
    for key in BotConfig.email_recipient.keys():
        if args[0][0] in key:
            valueString = BotConfig.email_recipient[key]
    try:
        speak(random.choice(phrases))

        server.login(sender, password)

        message = args[0][1:]
        recipient = valueString

        server.sendmail(sender, recipient, ' '.join(
            message).encode('utf-8'))

        speak("mail succesfuly sent")
        server.quit()

    except Exception as ext:
        print(ext)

def ColorPicker(*args: tuple):

    """
    { get color on your screen }

    :param      args:  The arguments
    :type       args:  tuple
    """

    phrases = [
        'get color',
        'wait, i get color from your screen'
    ]
    speak(random.choice(phrases))

    notification.notify(
        title="Visage-VA",
        message="color will be displayed in 2 seconds",
        app_name="Visage VA",
        timeout=1
    )

    time.sleep(2)
    x, y = pag.position()

    rgb = pag.pixel(x,y)
    colorNameClass = BotConfig.rgbname()

    notification.notify(
        title="Visage-VA",
        message=f"Color on screen: {colorNameClass.convert_rgb_to_names(rgb)}",
        app_name="Visage VA",
        timeout=10
    )

def reminder(*args: tuple):

    phrases = [
        "reminder ready",
        "remind you when the time comes",
        "I won't forget"
    ]

    Get = BotConfig.GetInfo()
    Info = Get.remind()

    remindText, remindLocalTime = Info[0], Info[1]

    speak(random.choice(phrases))

    def run_continuously(interval=1):
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    schedule.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run

    def background_job():
        notification.notify(
            title="Visage-VA notification",
            message=remindText,
            app_name="Visage VA",
            timeout=1
            )
        return schedule.CancelJob

    schedule.every().day.at(remindLocalTime).do(background_job)

    stop_run_continuously = run_continuously()

def FindFile(*args: tuple):

    phrases = [
        "already looking",
        "I'll find. it soon",
        "wait, the search for the file has begun"
    ]

    Get = BotConfig.GetInfo()
    Info = Get.Finder()

    disk = psutil.disk_partitions()
    file_name = Info

    b = 0
    lenResponse = 0
    speak(random.choice(phrases))
    while b < len(disk):
        folders = disk[b][0]

        resp = glob.glob(f"{folders}**/{file_name}", recursive=True)
        while lenResponse < len(resp):
            File = resp[lenResponse].replace(file_name, "")
            os.system(f"explorer.exe {File}")
            
            lenResponse +=1
        b += 1

def TelegramSend(*args: tuple):
    pass
if __name__ == '__main__':
    # the_program_to_hide = win32gui.GetForegroundWindow()
    # win32gui.ShowWindow(the_program_to_hide , win32con.SW_HIDE)
    Username = BotConfig.GetUserName()
    HelloWord(Username)

    while True:
        keyboard.wait("Ctrl + Shift")
        # call function
        ParseVoice = Recognition().lower().split()
        command = ParseVoice[0]
        commandOptions = [str(input_part)
                            for input_part in ParseVoice[1:len(ParseVoice)]]
        GetCommand(ParseVoice, Username, command, commandOptions)
    while True:
        schedule.run_pending()