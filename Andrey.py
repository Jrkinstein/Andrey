from PIL import ImageGrab
import speech_recognition as sr
import subprocess
import requests
import geocoder
import datetime
import pyttsx3
import psutil
import webbrowser
import GPUtil
import time
import vlc
import os

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

# Функция для распознавания речи
# Убрать конфликт русского и английского языков 
# Сделать так, чтобы откликался только на слово Андрей 
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Слушаю...')
        r.adjust_for_ambient_noise(source)  # Подстройка к фоновому шуму
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language="ru-RU").lower()
        if 'Андрей' in command:
            command = command.replace('Андрей', '')
            print(command)
    except sr.UnknownValueError:
        command = ""
    return command

# Функция для ответа текстом
def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

active_mode = False
location = ""

for root, dirs, files in os.walk("."):  # сканирование текущей директории и всех поддиректорий
    for file in files:
        if file.endswith(".mp3"):
            mp3_files.append(os.path.join(root, file))  # добавление пути к файлу в массив
for file in mp3_files:
    media = instance.media_new_path(file)
    playlist.add_media(media)
player.set_media(media)
if __name__ == "__main__":
    speak("Привет! Я Андрей.")
    file = open('prov.txt', 'r')
    prov = int(file.read())
    file.close()
    if prov == 0:
        steam_path = input('укажите путь к Steam: ')
        prov = 1
        file = open('steam_path.txt', 'w')
        file.write(steam_path)
        file.close()
        file = open('prov.txt', 'w')
        file.write(str(prov))
        file.close()
    else:
        file = open('steam_path.txt', 'r')
        steam_path = file.read()
        file.close()
    while True:
        if not active_mode:
            command = listen()
        else:
            command = input()

        if 'до свидания' in command:
            speak('До свидания!')
            break

        if 'привет' in command:
            speak('Здравствуйте!')

        elif 'реши пример' in command:
            print('* умножить; '
                  '/ разделить; '
                  '+ сложить; '
                  '- вычесть; '
                  '// корень; '
                  '** степень; '
                  '% остаток')
# изменить на голосовой ввод
            expr = input("Введите арифметическое выражение: ")
            result = eval(expr)
            print("Результат:", result)

        elif 'открой видео' in command:
            speak('открываю')
            webbrowser.open('www.youtube.com')

        elif "инфа о" in command.lower():
            search_term = command.lower().replace("инфа о", "")
            url = "https://www.google.com/search?q={}".format(search_term)
            webbrowser.open(url)

        elif 'переведи' in command:
            webbrowser.open('https://translate.google.com/')

        elif 'сменить путь' in command:
            steam_path = input('укажите путь к Steam: ')
            file = open('steam_path.txt', 'w')
            file.write(steam_path)
            file.close()

        elif 'открой платформу для игр' in command:
            os.startfile(steam_path, "open")

        elif 'открой гонки' in command:
            app_command = f"steam://run/{1293830}"
            os.startfile(steam_path, "open")
            os.startfile(app_command)

        elif 'открой шутер' in command:
            app_command = f"steam://run/{730}"
            os.startfile(steam_path, "open")
            os.startfile(app_command)

        elif 'спасибо' in command:
            speak('Пожалуйста')

        elif command in ['сменить режим','Сменить режим']:
            if active_mode == True:
                speak('Перехожу в голосовой режим')
                active_mode = False
            else:
                speak('Перехожу в текстовый режим')
                active_mode = True

        elif 'включи музыку' in command:
            speak("Включаю музыку.")
            player = instance.media_list_player_new()
            player.set_media_list(playlist)
            player.play()

        elif 'выключи музыку' in command:
            player.stop()

        elif 'открой апокалипсис 1' in command:
            app_command = f"steam://run/{286690}"
            os.startfile(steam_path, "open")
            os.startfile(app_command)

        elif 'открой вконтакте' in command:
            webbrowser.open('https://vk.com/')

        elif 'открой апокалипсис 2' in command:
            app_command = f"steam://run/{287390}"
            os.startfile(steam_path, "open")
            os.startfile(app_command)

        elif 'открой апокалипсис 3' in command:
            app_command = f"steam://run/{412020}"
            os.startfile(steam_path, "open")
            os.startfile(app_command)

        elif 'открой бомбу' in command:
            app_command = f"steam://run/{341800}"
            os.startfile(steam_path, "open")
            os.startfile(app_command)

        elif 'открой производство' in command:
            app_command = f"steam://run/{526870}"
            os.startfile(steam_path, "open")
            os.startfile(app_command)

        elif 'открой фуру' in command:
            app_command = f"steam://run/{227300}"
            os.startfile(steam_path, "open")
            os.startfile(app_command)

        elif 'открой выживалку' in command:
            app_command = f"steam://run/{242760}"
            os.startfile(steam_path, "open")
            os.startfile(app_command)

        elif 'открой симулятор' in command:
            app_command = f"steam://run/{4000}"
            os.startfile(steam_path, "open")
            os.startfile(app_command)

        elif 'сколько времени' in command:
            now = datetime.datetime.now()
            speak(f"Текущее время: {now.strftime('%H:%M:%S')}")

        elif 'какой сегодня день' in command:
            now = datetime.datetime.now()
            speak(f"Сегодня {now.strftime('%A %d %B %Y')}")

        elif 'изменить местоположение' in command:
            location = input("Введите местоположение: ")

        elif command in ['открой блокнот', 'блокнот']:
            subprocess.Popen('notepad.exe')

        elif 'открой браузер' in command:
            webbrowser.open('www.google.com') # сделать для разных браузеров 

        elif 'кто ты' in command:
            speak('Я Андрей')

        elif 'следующий трек' in command:
            player.next()

        elif 'предыдущий трек' in command:
            playlist.player_prev()

        elif 'открой сайт мгкцт' in command:
            webbrowser.open('https://mgkct.minskedu.gov.by/') 

        elif 'выключи компьютер' in command:
            os.system("shutdown /s /t 1")

        elif 'перезагрузи компьютер' in command:
            os.system("shutdown /r /t 1")

        elif 'режим гибернации' in command:
            os.system("shutdown /h")

        elif 'сделай скриншот' in command:
            ImageGrab.grab().save('Screenshots\screenshot.png') # сделать рандомную генерацию названия

        elif 'нагрузка на процессор' in command:
            cpu_percent = psutil.cpu_percent()
            speak(f"Нагрузка на ЦП: {cpu_percent}%")

        elif 'нагрузка на видеокарту' in command:
            get_gpu_load()

        elif 'нагрузка на оперативку' in command:
            mem_percent = psutil.virtual_memory().percent
            speak(f"Нагрузка на ОЗУ: {mem_percent}%")

        elif 'открой боль' in command:
            app_command = f"steam://run/{570}"
            os.startfile(steam_path, "open")
            os.startfile(app_command)

        elif command in ['погода', 'погода сейчас']:
            try:
                if not location:
                    speak("В каком городе вы хотите узнать погоду?")
                    location = input("Введите местоположение: ")
                g = geocoder.osm(location)
                lat, lon = g.latlng
                url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={APPID}&units=metric'
            except:
                pass
            try:
                response = requests.get(url)
                data = response.json()
                if 'weather' in data:
                    description = data['weather'][0]['description']
                    temp = data['main']['temp']
                    speak(f"Сейчас в {location} {description}, температура {temp} градусов по Цельсию.")
                    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={APPID}&units=metric'
                    response = requests.get(url)
                    data = response.json()
                else:
                    speak("Не удалось получить информацию о погоде.")
            except:
                speak("Не удалось получить информацию о погоде.")

        elif command in ['погода на следующие 24 часа', 'погода на 24 часа']:
            try:
                if not location:
                    speak("В каком городе вы хотите узнать погоду?")
                    location = input("Введите местоположение: ")
# изменить на голосовой ввод 
                g = geocoder.osm(location)
                lat, lon = g.latlng
                url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={APPID}&units=metric'
            except:
                pass
            try:
                response = requests.get(url)
                data = response.json()
                if 'weather' in data:
                    description = data['weather'][0]['description']
                    temp = data['main']['temp']
                    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={APPID}&units=metric'
                    response = requests.get(url)
                    data = response.json()
                    if 'list' in data:
                        speak("Прогноз на следующие 24 часа:")
                        for item in data['list'][:8]:
                            date_time_str = item['dt_txt']
                            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
                            date = date_time_obj.strftime('%d.%m.%Y')
                            time = date_time_obj.strftime('%H:%M')
                            temp = item['main']['temp']
                            description = item['weather'][0]['description']
                            speak(f"{date} в {time} {description}, температура {temp} градусов по Цельсию.")
                else:
                    speak("Не удалось получить информацию о погоде.")
            except:
                speak("Не удалось получить информацию о погоде.")

        elif 'таймер' in command:
            try:
                seconds = int(input("Введите количество секунд: "))
# изменить на голосовой ввод 
                timer(seconds)
            except:
                speak('Не удалось запустить таймер: некорректный ввод.')

        elif 'секундомер' in command:
            start_time = time.time()
            input("Нажмите Enter, чтобы остановить секундомер.")
            end_time = time.time()
            elapsed_time = round(end_time - start_time, 2)
            print(f"Прошло {elapsed_time} секунд(ы).")

        else:
            print('?')
