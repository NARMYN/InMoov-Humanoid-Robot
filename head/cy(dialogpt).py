# Import all the necessary modules
import re
import os
import cv2
import sys
import time
import torch
import pyttsx3
import datetime
import argparse
import wolframalpha
import pandas as pd
import speech_recognition as sr
from features import loc
from features import date_time
from features import weather
from features import wikipedia
from features import news
from features import google_search
from features import lab_automation
from threading import Thread
from transformers import AutoModelForCausalLM, AutoTokenizer


# Define the Assistant class
class Assistant:
    def __init__(self, name: str):
        """
        Constructor for the Assistant class
        """
        self.name = name
        # ----- Conversational AI model -----
        model_name = "microsoft/DialoGPT-small"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        # ----- Text to speech engine -----
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voices', voices[0].id)
        self.engine.setProperty('rate', 175)
        # ----- Facial recognition -----
        # Load member details
        if os.path.isfile("data/facial_recognition/member_details.csv"):
            self.enable_facial_recognition = True
            self.members = pd.read_csv("data/facial_recognition/member_details.csv")
            # Load the face recognizer
            self.recognizer = cv2.face_LBPHFaceRecognizer.create()
            self.recognizer.read("data/facial_recognition/model.yml")
            # Load the cascade classifier
            self.face_detector = cv2.CascadeClassifier("data/facial_recognition/haarcascade_frontalface_default.xml")
            # To capture video from camera
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                print("There was an issue while opening the camera")
                exit(1)
            self.cap.set(3, 640)  # set video width
            self.cap.set(4, 480)  # set video height
            self.detected_faces = []
        else:
            self.enable_facial_recognition = False
        # ----- Startup routine -----
        self.startup()

    def startup(self):
        """
        Startup routine for the assistant
        """
        self.speak("Initializing and starting all core systems...", info=True)
        self.speak("Checking all drivers...", info=True)
        self.speak("All systems up and running", info=True)
        self.speak("State is normal", info=True)

        hour = int(datetime.datetime.now().hour)
        if 0 <= hour <= 12:
            self.speak("Good morning sir!", info=True)
        elif 12 < hour < 18:
            self.speak("Good afternoon sir!", info=True)
        else:
            self.speak("Good evening sir!", info=True)

        current_time = self.tell_time()
        self.speak(f"Currently it is {current_time}", info=True)
        self.speak("I am " + self.name + " online and ready sir", info=True)

    def listen(self):
        """
        Fetch input from mic and convert it to text using Google Speech Recognition Service
        return: user's voice input as text if true, false if fail
        """
        try:
            recognizer = sr.Recognizer()
            # r.pause_threshold = 1
            # r.adjust_for_ambient_noise(source, duration=1)
            with sr.Microphone() as source:
                print("Listening....")
                recognizer.energy_threshold = 4000
                audio = recognizer.listen(source)
            try:
                print("Recognizing...")
                cmd = recognizer.recognize_google(audio, language='en-in').lower()
                print(f'You: {cmd}')
            except sr.UnknownValueError:
                print("Sorry, I did not get that")
                cmd = self.listen()
            except sr.RequestError as e:
                print("Could not request results from Google speech recognition service; {0}".format(e))
                cmd = self.listen()
            return cmd
        except Exception as e:
            print(e)
            return False

    def speak(self, text: str, info=False):
        """
        Convert any text to speech using pyttsx3
        :param text: text(String)
        :param info: whether the given string is a message
        """
        if info:
            print(text)
        else:
            print(self.name, " --> ", text)

        # Pronunciation fix for Cy object
        text = text.replace("Cy", "Sai")

        self.engine.say(text)
        self.engine.runAndWait()
        self.engine.setProperty('rate', 175)

    def facial_recognition(self, conf_thresh=30):
        """
        Performs facial recognition of NUST RAI members
        :param conf_thresh: confidence threshold
        """

        def diff(lst1: list, lst2: list):
            """
            Performs difference of two lists
            :param lst1: first list
            :param lst2: second list
            """
            list_dif = [i for i in lst1 + lst2 if i not in lst1 or i not in lst2]
            return list_dif

        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voices', voices[0].id)
        engine.setProperty('rate', 175)

        while self.cap.isOpened():
            # Read the frame
            ret, image = self.cap.read()
            if ret:
                # Min window size to be recognized as a face
                min_w = 0.1 * self.cap.get(3)
                min_h = 0.1 * self.cap.get(4)

                # Flips the original frame about y-axis
                image = cv2.flip(image, 1)

                # Convert to grayscale
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Detect the faces
                faces = self.face_detector.detectMultiScale(gray, 1.2, 5, minSize=(int(min_w), int(min_h)),
                                                            flags=cv2.CASCADE_SCALE_IMAGE)

                for (x, y, w, h) in faces:
                    cms_id, conf = self.recognizer.predict(gray[y:y + h, x:x + w])
                    if conf < 100 and (100 - conf) > conf_thresh:
                        name = self.members.loc[self.members['CMS ID'] == cms_id]['Name'].values
                        name = ' '.join(name)
                        if name not in self.detected_faces:
                            engine.say("Welcome " + name + " sir!")
                            self.detected_faces.append(name)

                if not self.enable_facial_recognition:
                    break
            else:
                break
        # When everything done, release the video capture object
        self.cap.release()
        # Stop tts engine
        engine.stop()
        # Destroy all the windows if they were created
        cv2.destroyAllWindows()

    @staticmethod
    def tell_date():
        """
        Return date
        :return: current date
        """
        return date_time.date()

    @staticmethod
    def tell_time():
        """
        Return time
        :return: current time
        """
        return date_time.time()

    @staticmethod
    def weather(city: str):
        """
        Return weather
        :param city: Any city of this world
        :return: weather info as string if True, or False
        """
        try:
            result = weather.fetch_weather(city)
        except Exception as e:
            print(e)
            result = False
        return result

    @staticmethod
    def tell_me(topic: str):
        """
        Tells about anything from wikipedia
        :param topic: any string is valid options
        :return: First 500 character from wikipedia if True, False if fail
        """
        return wikipedia.tell_me_about(topic)

    @staticmethod
    def location(location: str):
        current_loc, target_loc, distance = loc.loc(location)
        return current_loc, target_loc, distance

    @staticmethod
    def google(command: str):
        google_search.google_search(command)

    @staticmethod
    def lab_automation(command: str):
        """
        Fetch top news of the day from google news
        :return: news list of string if True, False if fail
        """
        lab_automation.switch(cmd=command)

    @staticmethod
    def my_location():
        city, state, country = loc.my_location()
        return city, state, country

    @staticmethod
    def news():
        """
        Fetch top news of the day from google news
        :return: news list of string if True, False if fail
        """
        return news.get_news()


def main(speech: bool):
    # Define the assistant object
    cy = Assistant(name="Cy")

    def computational_intelligence(question: str):
        try:
            client = wolframalpha.Client("39W8AT-4697HQXJK6")
            answer = client.query(question)
            answer = next(answer.results).text
            print(answer)
            return answer
        except:
            cy.speak("Sorry sir I couldn't fetch your question's answer. Please try again ")
            return None

    def cmd_handler(cmd: str):

        if re.search('date', cmd):
            date_today = cy.tell_date()
            cy.speak(date_today)

        elif "time" in cmd:
            time_now = cy.tell_time()
            cy.speak(time_now)

        elif 'lights' in cmd or 'fans' in cmd:
            cy.lab_automation(cmd)

        elif re.search('weather', cmd):
            city = cmd.split(' ')[-1]
            weather_result = cy.weather(city=city)
            cy.speak(weather_result)

        elif re.search('tell me about', cmd):
            topic = cmd.split(' ')[-1]
            if topic:
                wiki_result = cy.tell_me(topic)
                cy.speak(wiki_result)
            else:
                cy.speak("Sorry sir. I couldn't load your query from my database. Please try again")

        elif "news" in cmd or "headlines" in cmd:
            news_result = cy.news()
            cy.speak("Today's headlines are..")
            for index, articles in enumerate(news_result):
                cy.speak(articles['title'])
                if index == len(news_result) - 2:
                    break
            cy.speak('These were the top headlines, Have a nice day sir!')

        elif 'google ' in cmd:
            cy.google(cmd)

        elif "calculate" in cmd:
            answer = computational_intelligence(cmd)
            cy.speak(answer)

        elif "what is" in cmd or "who is" in cmd:
            answer = computational_intelligence(cmd)
            cy.speak(answer)

        elif "where is" in cmd:
            place = cmd.split('where is ', 1)[1]
            current_loc, target_loc, distance = cy.location(place)
            city = target_loc.get('city', '')
            state = target_loc.get('state', '')
            country = target_loc.get('country', '')
            time.sleep(1)
            try:
                if city:
                    result = f"{place} is in {state} state and country {country}. It is {distance} km away from your " \
                             f"current location "
                    cy.speak(result)
                else:
                    result = f"{state} is a state in {country}. It is {distance} km away from your current location"
                    cy.speak(result)
            except:
                result = "Sorry sir, I couldn't get the co-ordinates of the location you requested. Please try again"
                cy.speak(result)
        elif "where i am" in cmd or "current location" in cmd or "where am i" in cmd:
            try:
                city, state, country = cy.my_location()
                print(city, state, country)
                cy.speak(
                    f"You are currently in {city} city which is in {state} state and country {country}")
            except Exception as e:
                cy.speak(
                    "Sorry sir, I coundn't fetch your current location. Please try again")
        elif "exit" in cmd:
            cy.enable_facial_recognition = False
            cy.engine.stop()
            cy.speak("Alright sir, going offline. It was nice working with you")
            sys.exit()
        else:
            return True

    if cy.enable_facial_recognition:
        # Intialize the thread that will be used for facial recognition
        facial_recognition_thread = Thread(target=cy.facial_recognition, daemon=True)
        # Start the thread
        facial_recognition_thread.start()

    conv_exchange = 0

    if speech:
        while True:
            cmd = cy.listen()
            if cmd_handler(cmd=cmd):
                if conv_exchange == 30: conv_exchange = 0
                # Encode the input and add end of string token
                input_ids = cy.tokenizer.encode(cmd + cy.tokenizer.eos_token, return_tensors="pt")
                # concatenate new user input with chat history (if there is)
                bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if conv_exchange > 0 else input_ids
                # generate a bot response
                chat_history_ids = cy.model.generate(
                    bot_input_ids,
                    max_length=1000,
                    do_sample=True,
                    top_k=100,
                    temperature=0.75,
                    pad_token_id=cy.tokenizer.eos_token_id
                )
                # print the output
                cy.text = cy.tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0],
                                              skip_special_tokens=True)
                cy.speak(cy.text)
                conv_exchange += 1

    if not speech:
        while True:
            cmd = input('You --> ')
            if not cmd_handler(cmd=cmd):
                if conv_exchange == 30: conv_exchange = 0
                # Encode the input and add end of string token
                input_ids = cy.tokenizer.encode(cmd + cy.tokenizer.eos_token, return_tensors="pt")
                # Concatenate new user input with chat history (if there is)
                bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if conv_exchange > 0 else input_ids
                # Generate a bot response
                chat_history_ids = cy.model.generate(
                    bot_input_ids,
                    max_length=1000,
                    do_sample=True,
                    top_k=100,
                    temperature=0.75,
                    pad_token_id=cy.tokenizer.eos_token_id
                )
                # Print the output
                cy.text = cy.tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0],
                                              skip_special_tokens=True)
                print(cy.name, " --> ", cy.text)
                conv_exchange += 1


if __name__ == "__main__":
    # Define the parser object
    parser = argparse.ArgumentParser()
    # Define the arguments
    parser.add_argument('--speech', action='store_false')
    # Parse all the arguments
    opt = parser.parse_args()
    # Run the main function
    main(speech=opt.speech)
