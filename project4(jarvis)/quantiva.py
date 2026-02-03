import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import pyjokes
import time
import os


def sptext():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            data = recognizer.recognize_google(audio)
            return data.lower()
        except sr.UnknownValueError:
            print("Quantiva could not understand the audio")
            return ""
        except sr.RequestError:
            print("Speech service is unavailable")
            return ""


def speechtx(x):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 150)
    engine.say(x)
    engine.runAndWait()


speechtx("I am Quantiva. How can I help you?")


if __name__ == "__main__":
    while True:
        data1 = sptext()

        if not data1:
            speechtx("I am sorry, I didn't catch that. Could you please repeat?")
            continue

        if "your name" in data1:
            speechtx("My name is Quantiva")

        elif "how old are you" in data1:
            speechtx("I am a computer program. I do not have an age like humans.")

        elif "time" in data1:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speechtx("The current time is " + current_time)

        elif "youtube" in data1:
            speechtx("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "earn with saboor" in data1:
            speechtx("Opening earn with saboor")
            webbrowser.open("https://www.youtube.com/@earn_with_saboor")

        elif "joke" in data1:
            joke = pyjokes.get_joke(language="en", category="all")
            speechtx(joke)
            print(joke)

        elif "exit" in data1 or "quit" in data1:
            speechtx("Thank you for using me. Goodbye!")
            break

        else:
            speechtx("Sorry, I don't know how to help with that yet.")

        time.sleep(2)
