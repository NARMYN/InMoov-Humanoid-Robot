import requests
import pyttsx3
import speech_recognition as sr
import time
url1 = "https://api.thingspeak.com/update?api_key=G39NYATOHG8YCBE9&field"
url2 = "https://api.thingspeak.com/update?api_key=19C0JCSMVQUHZI0Q&field"
Dict = {"AL1":'1',"AL2":'2',"AL3":'3',"AF1":'4',
            "BL1":'1',"BL2":'2',"BF1":'3',"CL1":'4',
            "CL2":'5',"CL3":'6',"AC1":'7'}

def speech_to_text():
    """
    Convert audio to text using Google Speech Recognition Service
    """
    starttime =time.time()
    endtime = starttime
    recognizer = sr.Recognizer()
    with sr.Microphone(3) as mic:
        print("listening...")
        recognizer.adjust_for_ambient_noise(mic)
        audio = recognizer.listen(mic, timeout=8,phrase_time_limit=8)
    try:
        text = recognizer.recognize_google(audio)
        print("me --> ", text)
    except sr.UnknownValueError:
        print("me -->  Sorry, I did not get that")
    except sr.RequestError as e:
        print("Could not request results from Google speech recognition service; {0}".format(e))
    return text

url1 = "https://api.thingspeak.com/update?api_key=G39NYATOHG8YCBE9&field"
url2 = "https://api.thingspeak.com/update?api_key=19C0JCSMVQUHZI0Q&field"
Dict = {"AL1":'1',"AL2":'2',"AL3":'3',"AF1":'4',
            "BL1":'1',"BL2":'2',"BF1":'3',"CL1":'4',
            "CL2":'5',"CL3":'6',"AC1":'7'}

while(True):
    cmd = speech_to_text()
    if cmd.lower() == "sai light off":
        n = "AL3"
        m = "1"
        
    elif cmd.lower() == "SAI light on":
        n = "AL3"
        m = "0"   
    #print(n[2])
    #print(n[0])
    print(Dict[n])
    
    if n[0]=='A':
        s=url1+Dict[n]+'='+m
        print(s)
        a=requests.get(s)    
        while a.text=='0':
            a = requests.get(s)
    
    elif n[0]=='B' or n[0] == 'C'  :
        s=url2+Dict[n]+'='+m
        print(s)
        a=requests.get(s)    
        while a.text=='0':
            a = requests.get(s)
    else:
        print("Please Enter Correct Switch Name")                   