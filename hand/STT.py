#pip install SpeechRecognition
#pip install PyAudio
import speech_recognition as sr
def speechrecognition():
    recog = sr.Recognizer()
    num = int(input("Press 0 to use microphone and 1 to use an audio file"))
    if num==0:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recog.listen(source)
        try:
            #using default API KEY
            #for custom use: r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")
            my_audio = recog.recognize_google(audio)
            print("--Translating---")
            print("Result:", my_audio)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recogniton Service, {0}".format(e))
    elif num == 1:
        filename = input("Please provide file name with extension") # ext should be WAV
        with sr.AudioFile(filename) as source:
            audiofile = recog.listen(source)
            try:
                text = recog.recognize_google(audiofile)
                print(text)
            except:
                print("Check Internet connectivity")
    else:
        print("Enter the correct number. Follow instructions properly")
    return my_audio
mybool=bool(input("Do you want to use speech recognition(Y/N)?"))
if mybool==True:
    speechrecognition()