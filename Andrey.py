from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from ctypes import wintypes
from PIL import ImageGrab
from tkinter import *
import speech_recognition as sr
import subprocess
import webbrowser
import threading
import requests
import datetime
import pyttsx3
import psutil
import GPUtil
import random
import ctypes
import json
import nltk
import time
import os

global player
# Инициализация библиотеки user32.dll
user32 = ctypes.WinDLL('user32')
# Определение типов данных WPARAM и LPARAM
WPARAM = wintypes.WPARAM
LPARAM = wintypes.LPARAM
# Определение констант для сообщений о громкости звука
WM_APPCOMMAND = 0x319
APPCOMMAND_VOLUME_UP = 0x0a
APPCOMMAND_VOLUME_DOWN = 0x09
APPCOMMAND_VOLUME_MUTE = 0x08
# Загрузка стоп-слов для русского и английского языков
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words(['russian', 'english']))
# Инициализируем библиотеки
listener = sr.Recognizer()
engine = pyttsx3.init()
# Установка скорости речи
engine.setProperty('rate', 200)
# Инициализация распознавателя речи
r = sr.Recognizer()

# Функция для увеличения громкости звука
def volume_up():
    user32.PostMessageW(WPARAM(-1), WM_APPCOMMAND, 0, APPCOMMAND_VOLUME_UP * 0x10000)

# Функция для уменьшения громкости звука
def volume_down():
    user32.PostMessageW(WPARAM(-1), WM_APPCOMMAND, 0, APPCOMMAND_VOLUME_DOWN * 0x10000)

# Функция для отключения звука
def volume_mute():
    user32.PostMessageW(WPARAM(-1), WM_APPCOMMAND, 0, APPCOMMAND_VOLUME_MUTE * 0x10000)

# Функция для запуска таймера на указанное количество секунд
def start_timer(seconds):
    time.sleep(seconds)
    speak(f"Таймер на {seconds} секунд завершен.", 'ru-RU')

# Функция для запуска секундомера
def start_stopwatch():
    global stopwatch_start_time
    stopwatch_start_time = time.time()

# Функция для остановки секундомера и вывода затраченного времени
def stop_stopwatch():
    global stopwatch_start_time
    elapsed_time = time.time() - stopwatch_start_time
    speak(f"Секундомер остановлен. Затраченное время: {elapsed_time:.2f} секунд.", 'ru-RU')

# Функция для поиска информации в Google по указанному запросу
def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    for g in soup.find_all('div', class_='g'):
        title = g.find('h3').text
        link = g.find('a')['href']
        snippet = g.find('span', class_='st').text
        results.append({'title': title, 'link': link, 'snippet': snippet})
    return results

# Функция для запуска таймера
def timer(duration):
    return f"Таймер запущен на {duration} секунд."
    time.sleep(duration)
    return "Время вышло!"

# Функция для произношения текста
def speak(text, language):
    # Установка языка речи
    if language == 'ru-RU':
        engine.setProperty('voice', 'ru')
    else:
        engine.setProperty('voice', 'en')
    engine.say(text)
    engine.runAndWait()

# Функция для получения информации о погоде в указанном городе
def get_weather(city):
    # Замените YOUR_API_KEY на ваш ключ API с сайта openweathermap.org
    api_key = "bf2b8514d932c9a8d1a63ede6a186442"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        return f"В городе {city} сейчас {temp} градусов по Цельсию и {description}."
    else:
        return f"Извините, я не смог получить информацию о погоде в городе {city}."

# Функция для распознавания речи
def recognize_speech():
    with sr.Microphone() as source:
        audio = r.listen(source)
        # Попытка распознать речь на русском языке
        try:
            text = r.recognize_google(audio, language='ru-RU')
            print(text)
            return text, 'ru-RU'
        except:
            pass
        # Попытка распознать речь на английском языке
        try:
            text = r.recognize_google(audio, language='en-US')
            print(text)
            return text, 'en-US'
        except:
            return "Извините, я не понял.", 'ru-RU'

# Функция для обработки нажатия кнопки "Говорить"
def on_speak_button_click():
    while True:
        text, language = recognize_speech()
        input_text.set(text)
        response = process_text(text, language)
        speak(response, language)
        if response == "До свидания!" or response == "Goodbye!":
            break

steam_path = 'C:\Program Files (x86)\Steam\Steam.exe'
# Функция для обработки текста и генерации ответа
def process_text(text, language):
    # Токенизация текста и удаление стоп-слов
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalpha()]
    words = [word for word in words if word not in stop_words]

    # Проверка наличия ключевых слов в тексте
    if 'открой' in words or 'open' in words or 'запусти' in words:
        if 'steam' in words:
            os.startfile(steam_path, "open")
            return "Открываю"

        elif 'youtube' in words:
            webbrowser.open("https://www.youtube.com")
            return "Открываю YouTube." if language == 'ru-RU' else "Opening YouTube."

        elif 'переводчик' in words:
            webbrowser.open('https://translate.google.com/')
            return "Открываю"

        elif 'бомбу' in words or 'talking' in words or 'nobody' in words:
            app_command = f"steam://run/{341800}"
            os.startfile(steam_path, "open")
            os.startfile(app_command)
            return "Открываю"

        elif 'производство' in words or 'satisfactory' in words:
            app_command = f"steam://run/{526870}"
            os.startfile(steam_path, "open")
            os.startfile(app_command)
            return "Открываю"

        elif 'фуру' in words or'етс' in words or 'ets' in words:
            app_command = f"steam://run/{227300}"
            os.startfile(steam_path, "open")
            os.startfile(app_command)
            return "Открываю"

        elif 'forest' in words or 'выживалку' in words:
            app_command = f"steam://run/{242760}"
            os.startfile(steam_path, "open")
            os.startfile(app_command)
            return "Открываю"

        elif 'mod' in words or 'мод' in words:
            app_command = f"steam://run/{4000}"
            os.startfile(steam_path, "open")
            os.startfile(app_command)
            return "Открываю"

        elif 'vk' in words or 'вк' in words or 'вконтакте' in words:
            webbrowser.open('https://vk.com/')
            return "Открываю"

        elif 'гонки' in words or 'forza' in words or 'форзу' in words:
            app_command = f"steam://run/{1293830}"
            os.startfile(steam_path, "open")
            os.startfile(app_command)
            return "Открываю"

        elif 'ks' in words or 'кс' in words or 'шутер' in words:
            app_command = f"steam://run/{730}"
            os.startfile(steam_path, "open")
            os.startfile(app_command)
            return "Открываю"

        elif 'блокнот' in words:
            subprocess.Popen('notepad.exe')
            return "Открываю"

        elif 'браузер' in words:
            webbrowser.open('www.google.com')
            return "Открываю"

        elif 'мгк' in words or 'мгкцт' in words or 'колледжа' in words:
            webbrowser.open('https://mgkct.minskedu.gov.by/')
            return "Открываю"

        elif 'доту' in words or 'dota' in words or 'боль' in words:
            app_command = f"steam://run/{570}"
            os.startfile(steam_path, "open")
            os.startfile(app_command)
            return "Открываю"

        elif 'metro' in words or 'метро' in words:
            if '2033' in words:
                app_command = f"steam://run/{286690}"
                os.startfile(steam_path, "open")
                os.startfile(app_command)
                return "Открываю"

            elif 'last' in words or 'light' in words or 'луч' in words or 'надежды' in words:
                app_command = f"steam://run/{287390}"
                os.startfile(steam_path, "open")
                os.startfile(app_command)
                return "Открываю"

            elif 'exodus' in words or 'исход' in words:
                app_command = f"steam://run/{412020}"
                os.startfile(steam_path, "open")
                os.startfile(app_command)
                return "Открываю"

    elif 'погода' in words or 'weather' in words:
        city_index = words.index('погода') + 1 if 'погода' in words else words.index('weather') + 1
        if city_index < len(words):
            city = words[city_index]
            return get_weather(city)

    elif ('найди' in words or 'find' in words) and ('google' in words or 'гугл' in words):
        query_index = words.index('найди') + 1 if 'найди' in words else words.index('find') + 1
        query_words = words[query_index:]
        query = ' '.join(query_words)
        results = search_google(query)
        if results:
            response = f"Вот что я нашел в Google по запросу '{query}':\n"
            for result in results:
                response += f"{result['title']} - {result['link']}\n"
            return response
        else:
            return f"Извините, я ничего не нашел в Google по запросу '{query}'."

    elif 'таймер' in words:
        seconds_index = words.index('таймер') + 1
        if seconds_index < len(words):
            try:
                seconds = int(words[seconds_index])
                threading.Thread(target=start_timer, args=(seconds,)).start()
                return f"Таймер на {seconds} секунд запущен."
            except ValueError:
                pass

    if 'секундомер' in words:
        if 'старт' in words:
            start_stopwatch()
            return "Секундомер запущен."

        elif 'стоп' in words:
            stop_stopwatch()

    if language == 'ru-RU':
        if 'привет' in words:
            return "Привет! Как дела?"

        elif 'дела' in words:
            return "У меня все хорошо, спасибо! А у тебя?"

        elif 'пока' in words:
            return "До свидания!"

        elif 'кто' in words and 'ты' in words:
            return 'Я Андрей'

        elif 'сколько' in words and 'времени' in words:
            now = datetime.datetime.now()
            return f"Текущее время: {now.strftime('%H:%M:%S')}"

        elif 'какой' in words and 'сегодня' in words:
            now = datetime.datetime.now()
            return f"Сегодня {now.strftime('%A %d %B %Y')}"

        elif 'компьютер' in words:
            if 'выключи' in words:
                os.system("shutdown /s /t 1")

            elif 'перезагрузи' in words:
                os.system("shutdown /r /t 1")

        elif 'режим' in words and 'гибернации' in words:
            os.system("shutdown /h")

        elif 'сделай' in words and 'скриншот' in words:
            rand = random.randint(0,99999999999)
            ImageGrab.grab().save(f'Screenshots\{rand}.png')
            return 'делаю'


        elif 'нагрузка' in words:
            if 'процессор' in words:
                cpu_percent = psutil.cpu_percent()
                return f"Нагрузка на ЦП: {cpu_percent}%"

            elif 'видеокарту' in words:
                gpus = GPUtil.getGPUs()
                for gpu in gpus:
                    return f"GPU{gpu.id}: {gpu.load * 100}%"

            elif 'оперативку' in words:
                mem_percent = psutil.virtual_memory().percent
                return (f"Нагрузка на ОЗУ: {mem_percent}%")

        elif 'громкость' in words:
            if 'увеличь' in words:
                volume_up()
                return 'есть'

            elif 'уменьши' in words:
                volume_down()
                return 'есть'

        elif 'выключи' in words and 'звук' in words:
            volume_mute()
            return 'есть'

        else:
            return "Извините, я не понял."

    else:
        if 'hello' in words:
            return "Hello! How are you?"

        elif 'how' in words and 'you' in words:
            return "I'm fine, thank you! And you?"

        elif 'goodbye' in words:
            return "Goodbye!"

        else:
            return "Sorry, I didn't understand."

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