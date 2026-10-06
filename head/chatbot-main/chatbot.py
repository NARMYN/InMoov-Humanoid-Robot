# Import all the necessary packages
import os
import argparse
import pyttsx3
import pandas as pd
import speech_recognition as sr
from simpletransformers.conv_ai import ConvAIModel, ConvAIArgs


# Define the chatbot class
class ChatBot:
    def __init__(self, name: str):
        self.name = name
        self.text = ''
        self.bot_persona = [
            "My name is Dobby.",
            "I protect Harry Potter and his friends."
            "I am a loyal servant.",
            "I am brave and quirky.",
            "My power is magic.",
            "I am a free elf."
        ]
        self.history = []
        self.student_info = ''
        model_args = ConvAIArgs()
        model_args.max_history = 50
        self.model = ConvAIModel(model_type="gpt", model_name="gpt_personachat_cache", args=model_args)
        print('--- ', name, ' is awake! ---')

    def generate_student_info(self, cms_id: int):
        qalam_csv = pd.read_csv('qalam.csv')
        qalam_csv = qalam_csv.set_index('CMS ID').T.to_dict('dict')
        info = qalam_csv[cms_id]
        self.student_info = "Your name is " + info['Name'] + ". Your father name is " + info['Father Name'] + ". Your roll number is " + info['Roll no'] + ". You live in  " + info['Address'] + ". And your CGPA is " + str(info['CGPA'])

    def speech_to_text(self):
        """
        Convert audio to text using Google Speech Recognition Service
        """
        recognizer = sr.Recognizer()
        with sr.Microphone(0) as mic:
            print("listening...")
            recognizer.adjust_for_ambient_noise(mic)
            audio = recognizer.listen(mic)
        try:
            self.text = recognizer.recognize_google(audio)
            print("me --> ", self.text)
        except sr.UnknownValueError:
            print("me -->  Sorry, I did not get that")
        except sr.RequestError as e:
            print("Could not request results from Google speech recognition service; {0}".format(e))

    def text_to_speech(self, text:str):
        """
        Convert text to audio using pyttsx3
        """
        print(self.name, " --> ", text)
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop()


# Run the bot
if __name__ == "__main__":

    # Define the parser object
    parser = argparse.ArgumentParser()
    # Define the arguments
    parser.add_argument('--speech', action='store_true')

    # Parse all the arguments
    opt = parser.parse_args()

    # Define the chatbot object
    bot = ChatBot(name="Dobby")

    # Ask for CMS ID
    cms_id = int(input('Please input your CMS ID: '))

    # Get student info
    bot.generate_student_info(cms_id=cms_id)

    while True:
        if opt.speech:
            bot.speech_to_text()
            if 'exit' in bot.text:
                bot.text = "Bye!"
                bot.text_to_speech(bot.text)
                break
            elif bot.text == 'who am i' or bot.text == 'Who am i' or bot.text == 'who am i?' or bot.text == 'Who am i?' or bot.text == 'who am I':
                bot.text = bot.student_info
                bot.text_to_speech(bot.text)
            else:
                bot.text, bot.history = bot.model.interact_single(
                    bot.text,
                    bot.history,
                    bot.bot_persona
                )
                bot.text_to_speech(bot.text)
        else:
            bot.text = input('me --> ')
            if 'exit' in bot.text:
                print(bot.name + " --> Bye!")
                break
            elif bot.text == 'who am i' or bot.text == 'Who am i' or bot.text == 'who am i?' or bot.text == 'Who am i?':
                bot.text = bot.student_info
                print(bot.name, " --> ", bot.text)
            else:
                bot.text, bot.history = bot.model.interact_single(
                    bot.text,
                    bot.history,
                    bot.bot_persona
                )
                print(bot.name, " --> ", bot.text)
