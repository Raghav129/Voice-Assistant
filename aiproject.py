import datetime
import os
import smtplib
import sys
import time
import webbrowser
import speech_recognition as sr
import cv2
import pyaudio
import instaloader
import pyautogui
import pyttsx3
import pywhatkit as kit
import requests
import wikipedia
from requests import get

engine = pyttsx3.init('sapi5')
voice = engine.getProperty('voices')
#print(voice)
engine.setProperty('voice', voice[1].id)


# Text to Speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# Taking input from user
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=1, phrase_time_limit=5)

    try:
        print("recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said:{query}")

    except Exception as e:
        speak("can you say that again please...")
        return "none"
    return query


# Wishes
def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")

    if hour > 0 and hour < 12:
        speak(f"Good Morning Sir, its {tt}")

    elif hour > 12 and hour < 17:
        speak(f"Good Afternoon Sir, its {tt}")
    else:
        speak(f"Good Evening sir, its {tt}")
    speak("I am Luna, how can i help you?")


# Sending an email
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('margamraghavendra2112@gmail.com', 'RaGHAvenDrAmaRgAmnANi@2112')
    server.sendmail('margamraghavendra2112@gmail.com', to, content)
    server.close()

def TaskExecution():
    wish()
    while True:
        # if 1:

        query = takecommand().lower()

        # Building Logic for Tasks

        if "open notepad" in query:
            npath = "C:\\Program Files\\WindowsApps\\Microsoft.WindowsNotepad_11.2302.16.0_x64__8wekyb3d8bbwe\\Notepad\\Notepad.exe"
            os.startfile(npath)

        elif "open adobe acrobat" in query:
            npath = "C:\\Program Files\\Adobe\\Acrobat DC\\Acrobat\\Acrobat.exe"
            os.startfile(npath)

        elif "open command prompt" in query:
            os.system("start cmd")

        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('Webcam', img)
                k = cv2.waitKey(50)
                if k == 27:
                    break;
            cap.release()
            cap.destroyAllWindows()

        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            speak(f"your ip address is {ip}")

        elif "wikipedia" in query:
            speak("searching wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia,")
            speak(results)

        elif "open youtube" in query:
            webbrowser.open("www.youtube.com")

        elif "open google" in query:
            speak("Sir, What should is search for?")
            cm = takecommand().lower()
            webbrowser.open(f"{cm}")

        elif "send message" in query:
            kit.sendwhatmsg("+916301720551", "this is a test message for you through my assistant", 20, 47)

        elif "play my favourite song" in query:
            speak("Playing Am I Dreaming")

            kit.playonyt("Metro Boomin, A$AP Rocky, Roisee - Am I Dreaming (Visualizer)")

        elif "send email to my friend" in query:
            try:
                speak("what should i say?")
                content = takecommand().lower()
                to = "gajulasathwik54@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent to sathwik, sir.")

            except Exception as e:
                print(e)
                speak("Sorry sir, im not able to send this email")

        elif "you can sleep" in query:
            speak("Thank you for using me sir, have a great day.")
            hour = int(datetime.datetime.now().hour)
            if hour > 22 and hour < 4:
                speak("Good Night sir, its {tt}, Sleep tight")
            else:
                pass
            sys.exit()
    

# Closing notepad

        elif "close notepad" in query:
            speak("Okay sir, closing it")
            os.system("taskkill /f /im notepad.exe")

# Switching windows
        elif "switch windows" in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("Alt")

        elif "where am i" in query or "where are we" in query:
            speak("wait sir, let me check")
            try:
                ipAdd = requests.get("https://api.ipify.org").text
                print(ipAdd)
                url = 'https://get.geojs.io/v1/ip/geo/' +ipAdd+'.json'
                geo_requests = requests.get(url)
                geo_data = geo_requests.json()
                # print(geo_data)
                city = geo_data['city']
                region = geo_data['state']
                # country = geo_data['country']
                speak(f"sir im not sure, but i think we are in {city} of {region} ")
            except Exception as e:
                speak("sorry sir, due to network issue im not able to find where we are.")
                pass
        
        # Check instagram profile

        elif "check instagram profile" in query:
            speak("okay sir, please enter the username")
            name = input("Enter username here: ")
            webbrowser.open(f"www.instagram.com/{name}")
            speak(f"sir, here is the profile of {name}")
            time.sleep(5)
            speak(f"sir, would you like to download {name}'s profile picture?")
            conditon = takecommand().lower()
            if "yes" in conditon:
                mod = instaloader.Instaloader()
                mod.download_profile(name, profile_pic_only=True)
                speak("download is done sir. profile picture is saved in our main folder. im ready for the next command")
            else:
                pass

        # Taking a screenshot

        elif "take a screenshot" in query:
            speak("sir, what should i name this screenshot file?")
            name = takecommand().lower()
            speak("hold the screen for a moment sir, i am taking screenshot")
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("screenshot is taken and saved in the main folder sir, i am ready for the next task")

        elif "thank you" in query:
            speak("pleasure is mine sir")
        
        elif "hello" in query or "hey" in query:
            speak("hello sir, may i help you with something?")

        elif "how are you" in query:
            speak("im fine sir, how about you?")

        elif "im good" in query or "im fine" in query or "im great" in query:
            speak("that's great to hear from you")
        
        elif "sleep now" in query:
            speak("okay sir, im sleeping now. you can call me anytime!")
            break


if __name__ == "__main__":
    while True:
        permission = takecommand()
        if "wake up" in permission:
            TaskExecution()
        elif "good bye" in permission:
            speak("y")
            sys.exit()
