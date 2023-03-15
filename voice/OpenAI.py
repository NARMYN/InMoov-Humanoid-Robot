import os
#import library

import speech_recognition as sr

# Initialize recognizer class (for recognizing the speech)

r = sr.Recognizer()
# Reading Microphone as source
# listening the speech and store in audio_text variable
while True:
    with sr.Microphone() as source:
        print("Talk")
        r.energy_threshold = 4000
        audio_text = r.listen(source)
        print("Time over, thanks")
        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
	
    try:
        # using google speech recognition
        print("Text: "+r.recognize_google(audio_text))
        prompt = r.recognize_google(audio_text)
    except:
        print("Sorry, I did not get that")
         
    import openai

    # Replace YOUR_API_KEY with your OpenAI API key
    openai.api_key = os.environ["OPENAI_API_KEY"]  # set your key in the environment

    model_engine = "text-davinci-003"
    #prompt = "write a short note on NUST"

    # Set the maximum number of tokens to generate in the response


    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=500,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

    # Print the response
    mytext = completion.choices[0].text

    import pyttsx3
    engine = pyttsx3.init() # object creation

    """ RATE"""
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    print (rate)                        #printing current voice rate
    engine.setProperty('rate', 125)     # setting up new voice rate


    """VOLUME"""
    volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    print (volume)                          #printing current volume level
    engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

    """VOICE"""
    voices = engine.getProperty('voices')       #getting details of current voice
    #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
    engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
    print(mytext)
    #engine.say("Hello World!")
    engine.say(mytext)
    engine.runAndWait()
    engine.stop()
