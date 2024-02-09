import spacy
import datetime
import webbrowser
import speech_recognition as sr

class VoiceAssistant:
    def __init__(self):
        self.nlp = spacy.load("ru_core_news_md")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def process_command(self):
        with self.microphone as source:
            print("Скажи команду:")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            command = self.recognizer.recognize_google(audio, language="ru-RU")
            print("Вы сказали:", command)
            return self.analyze_command(command)
        except sr.UnknownValueError:
            return "Голос не распознан"
        except sr.RequestError as e:
            return f"Ошибка при запросе к сервису распознавания голоса: {e}"

    def analyze_command(self, command):
        doc = self.nlp(command.lower())

        print("Токены в команде:")
        for token in doc:
            print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)

        best_keyword = None
        max_similarity = 0

        for token in doc:
            for keyword in ['время', 'браузер']:
                similarity = self.nlp(token.lemma_).similarity(self.nlp(keyword))
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_keyword = keyword

        if max_similarity > 0.8:  # Порог близости слов
            return self.execute_command(best_keyword)
        else:
            return "Команда не распознана"

    def execute_command(self, keyword):
        if keyword == 'время':
            return self.get_time()
        elif keyword == 'браузер':
            return self.open_browser()
        return "Команда не распознана"

    def get_time(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        return f"Текущее время: {current_time}"

    def open_browser(self):
        webbrowser.open("https://www.google.com")
        return "Браузер открыт"

# Пример использования
assistant = VoiceAssistant()
response = assistant.process_command()
print(response)
