from playsound import playsound
from gtts import gTTS
from transliterate import translit
import pyaudio
import speech_recognition as sr
import os


def say(words):
    trans = translit(words, "ru", reversed=True)
    if os.path.exists(f'audios\\{trans}.mp3'):
        playsound(f'audios\\{trans}.mp3')
    myobj = gTTS(text=words, lang='ru', slow=False)
    try:
        myobj.save(f'audios\\{trans}.mp3')
        playsound(f'audios\\{trans}.mp3')
    except Exception as e:
        print(e)


class Interaction:
    def __init__(self):
        self.recog = sr.Recognizer()
        self.mic = sr.Microphone()

    def recognise_words(self):
        with self.mic as audio_file:
            print("Speak Please")

            self.recog.adjust_for_ambient_noise(audio_file)
            audio = self.recog.listen(audio_file)

            print("Converting Speech to Text...")

            try:
                ans = self.recog.recognize_google(audio, language="ru_RU")
                print("You said: " + ans)
                return ans
            except Exception as e:
                print("Error: " + str(e))
                return False
    
    def question(self):  # returns what was said
        said = self.recognise_words()
        if not(said):
            said = self.recognise_words()
            if not(said):
                return False
        said = [i for i in said.split()]
        return said
