import speech_recognition as sr
from PIL import ImageGrab
import subprocess
import requests
import geocoder
import datetime
import pyttsx3
from tkinter import *
import psutil
import webbrowser
import GPUtil
import time
import vlc
import os
import time

APPID = 'bf2b8514d932c9a8d1a63ede6a186442'
# Инициализируем библиотеки
listener = sr.Recognizer()
engine = pyttsx3.init()
# создаем экземпляр плеера
instance = vlc.Instance()
playlist = instance.media_list_new()
player = vlc.MediaPlayer()
mp3_files = []

def get_gpu_load():
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        speak(f"GPU{gpu.id}: {gpu.load*100}%")

# Функция для запуска таймера
def timer(duration):
    speak(f"Таймер запущен на {duration} секунд.")
    time.sleep(duration)
    speak("Время вышло!")

# Инициализация движка синтеза речи
engine = pyttsx3.init()

# Установка языка и скорости речи
engine.setProperty('voice', 'ru')
engine.setProperty('rate', 250)

# Функция для произношения текста
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Инициализация распознавателя речи
r = sr.Recognizer()

# Функция для распознавания речи
def recognize_speech():
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='ru-RU')
            print(text)
            return text
        except:
            return ""

# Функция для обработки нажатия кнопки "Говорить"
def on_speak_button_click():
    while True:
        text = recognize_speech()
        input_text.set(text)
        response = process_text(text)
        speak(response)
        if response == "До свидания!":
            break
        time.sleep(0)

for root, dirs, files in os.walk("."):  # сканирование текущей директории и всех поддиректорий
    for file in files:
        if file.endswith(".mp3"):
            mp3_files.append(os.path.join(root, file))  # добавление пути к файлу в массив
for file in mp3_files:
    media = instance.media_new_path(file)
    playlist.add_media(media)
    player.set_media(media)
file = open('steam_path.txt', 'r')
steam_path = file.read()
file.close()
# Функция для обработки текста и генерации ответа
def process_text(text):
    if text == "Привет":
        return "Привет!"

    elif text == "Как дела":
        return "У меня все хорошо, спасибо! А у тебя?"

    elif text.lower() == "пока":
        return "До свидания!"

    elif text.lower() =="открой youtube":
        webbrowser.open('www.youtube.com')
        return "Открываю"

    # пока не работает
    elif text == "инфа о":
        search_term = text.lower().replace("инфа о", "")
        url = "https://www.google.com/search?q={}".format(search_term)
        webbrowser.open(url)
        return "Ищу"

    elif text.lower() == "открой переводчик":
        webbrowser.open('https://translate.google.com/')
        return "Открываю"

    elif text.lower() == "открой steam":
        os.startfile(steam_path, "open")
        return "Открываю"

    elif text.lower() ==('открой гонки' or 'открой forza' or 'открой форзу'):
        app_command = f"steam://run/{1293830}"
        os.startfile(steam_path, "open")
        os.startfile(app_command)
        return "Открываю"

    elif text.lower() == 'открой шутер':
        app_command = f"steam://run/{730}"
        os.startfile(steam_path, "open")
        os.startfile(app_command)
        return "Открываю"

    else:
        return "Извините, я не понял."

# Создание главного окна приложения
root = Tk()
root.title("Голосовой помощник Андрей")

# Создание метки и поля ввода для отображения распознанного текста
Label(root, text="Распознанный текст:").pack()
input_text = StringVar()
Entry(root, textvariable=input_text).pack()

# Создание кнопки "Говорить"
Button(root, text="Говорить", command=on_speak_button_click).pack()

# Запуск главного цикла приложения
root.mainloop()