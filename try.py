import pyaudio, os
import speech_recognition as sr


def listen(r):
    with sr.Microphone() as source:
        # r.lang = 'rus'
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.5
        audio = r.listen(source)
    return audio


def open(name):
    if name == 'стим' or name == 'steam':
        os.system("start steam.exe")


def action(user):
    user = [i.lower() for i in user.split()]
    if len(user) > 0 and user[0] == "младший":
        if len(user) > 2 and user[1] == 'открой':
            open(user[2])



def main():
    r = sr.Recognizer()
    while True:
        audio = listen(r)
        try:
            user = r.recognize_google(audio, language="ru_RU")
            print(user)
            action(user)
        except Exception:
            pass


recog = sr.Recognizer()
mic = sr.Microphone()

with mic as audio_file:
    print("Speak Please")

    recog.adjust_for_ambient_noise(audio_file)
    audio = recog.listen(audio_file)

    print("Converting Speech to Text...")

    try:
        print("You said: " + recog.recognize_google(audio, language="ru_RU"))
    except Exception as e:
        print("Error: " + str(e))