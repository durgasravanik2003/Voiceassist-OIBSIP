import speech_recognition as sr
import pyttsx3
from datetime import datetime
import pyowm
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import webbrowser
import os


recognizer = sr.Recognizer()
engine = pyttsx3.init()

API_KEY = '730cfab73fa047320ddc6ad3e76f1057'
CITY = 'Nellore'  


EMAIL_ADDRESS = 'korchpatidurgasravani@gmail.com'  
EMAIL_PASSWORD = 'mpea kuxa ftiy nzww'  

owm = pyowm.OWM(API_KEY)  

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return None
        except sr.RequestError:
            speak("Sorry, I'm having trouble connecting to the speech recognition service.")
            return None
        except sr.WaitTimeoutError:
            speak("Listening timed out.")
            return None

def get_weather(city):
    try:
        observation = owm.weather_manager().weather_at_place(city)
        weather = observation.weather
        temp = weather.temperature('celsius')['temp']
        description = weather.detailed_status
        return f"The weather in {city} is currently {description} with a temperature of {temp} degrees Celsius."
    except pyowm.commons.exceptions.NotFoundError:
        return "Sorry, I couldn't find weather information for that location."
    except pyowm.commons.exceptions.PyowmError as e:
        return f"An error occurred: {e}"

def send_email(recipient, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(EMAIL_ADDRESS, recipient, text)
            speak("Email sent successfully.Let's check it out")
            
            gmail_url = f"https://mail.google.com/"
            webbrowser.open(gmail_url)
            
    except Exception as e:
        speak(f"An error occurred while sending the email: {e}")

def main():
    while True:
        command = listen()
        if command:
            if "hello" in command:
                speak("Hello! How can I assist you today?")
            elif "time" in command:
                now = datetime.now()
                speak(f"The current time is {now.strftime('%H:%M:%S')}")
            elif "date" in command:
                now = datetime.now()
                speak(f"Today's date is {now.strftime('%Y-%m-%d')}")
            elif "search" in command:
                search_query = command.replace("search", "").strip()
                speak(f"Searching for {search_query}...")
            elif "how is the weather today" in command:
                weather_info = get_weather(CITY)
                speak(weather_info)
            elif "send email" in command:
                speak("Please enter details:")
                recipient = input("Recipient's email address: ")
                subject = input("Subject: ")
                body = input("Body: ")
                send_email(recipient, subject, body)
            elif "open google" in command:
                speak("Opening Google.")
                webbrowser.open("https://www.google.com")
            elif "open spotify" in command:
                speak("Opening Spotify.")
                os.startfile("C:\\Users\\YourUsername\\AppData\\Roaming\\Spotify\\Spotify.exe")
            elif "bye" in command:
                speak("Goodbye!")
                break
            else:
                speak("Sorry, I didn't understand that.")
        else:
            continue

if __name__ == "__main__":
    main()
