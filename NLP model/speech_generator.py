import os
import tempfile
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import json
import random

class SpeechGenerator:
    def __init__(self, config_path):
        self.config_path = config_path
        self.load_phrases()

    def load_phrases(self):
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

    def generate_response(self, keyword):
        if keyword in self.config["фразы"]:
            phrases = self.config["фразы"][keyword]
            response = random.choice(phrases)
            return response
        else:
            return "Произошла ошибка. Фразы для данной команды не найдены."

    def speak(self, text):
        tts = gTTS(text=text, lang='ru')
        temp_filename = os.path.join(tempfile.gettempdir(), "output.mp3")
        tts.save(temp_filename)
        sound = AudioSegment.from_mp3(temp_filename)
        sound = sound.speedup(playback_speed=1.3)
        play(sound)
        os.remove(temp_filename)