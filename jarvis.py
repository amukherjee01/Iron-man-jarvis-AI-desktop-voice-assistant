import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import smtplib
import json

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
print(voices[0].id)
engine.setProperty("voice", voices[0].id)

with open("config.json") as f:
    params = json.load(f)["params"]


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

    speak("I am Jarvis sir. Please tell me how may i help you")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said {query}\n")

    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query


def sendEmail(to, content):
    sever = smtplib.SMTP("smtp.gmail.com", 587)
    sever.ehlo()
    sever.starttls()
    sever.login(params["useremail"], params["password"])
    sever.sendmail(params["useremail"], to, content)
    sever.close()


if __name__ == "__main__":
    # speak("Aditya is good boy")
    wishme()
    while True:
        query = takecommand().lower()

        # Logic for executing task based on query
        if "wikipedia" in query:
            speak("Searching wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia...")
            print(results)
            speak(results)

        elif "open youtube" in query:
            webbrowser.open("Youtube.com")

        elif "open google" in query:
            webbrowser.open("google.com")

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif "quit" in query:
            speak("Ok.. Quitting")
            exit()

        elif "send email to aditya" in query:
            try:
                speak("What should i say?")
                content = takecommand()
                to = params["useremail"]
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                print("Sorry i am not able to send email at this moment")
