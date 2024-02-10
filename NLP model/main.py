import spacy
import datetime
import webbrowser
import speech_recognition as sr
import json
import pymorphy2
from speech_generator import SpeechGenerator

class VoiceAssistant:
    def __init__(self, config_path):
        self.nlp = spacy.load("ru_core_news_md")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.config_path = config_path
        self.morph = pymorphy2.MorphAnalyzer()
        self.speech_generator = SpeechGenerator(config_path)

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

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

        # Поиск синонимов в конфиге
        for keyword, synonyms in self.config["синонимы"].items():
            if any(token.lemma_ in synonyms for token in doc):
                return self.execute_command(keyword, doc)

        # Если синоним не найден, использовать обычный анализ команды

        # Найти наиболее близкое ключевое слово
        best_keyword = None
        max_similarity = 0

        for token in doc:
            for keyword in self.config["синонимы"].keys():
                similarity = self.nlp(token.lemma_).similarity(self.nlp(keyword))
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_keyword = keyword

        if max_similarity > 0.8:  # Порог близости слов
            return self.execute_command(best_keyword, doc)
        else:
            return "Команда не распознана"

    def execute_command(self, keyword, doc):
        if keyword == 'время':
            return self.get_time()
        elif keyword == 'браузер':
            search_query = self.extract_search_query(doc)
            if search_query:
                return self.search_in_browser(search_query)
            else:
                return "Не удалось извлечь запрос из команды"
        return "Команда не распознана"

    def get_time(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        self.speech_generator.speak(self.speech_generator.generate_response("время").format(current_time=current_time))
        return 0

    def search_in_browser(self, query):
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        self.speech_generator.speak(self.speech_generator.generate_response("браузер"))
        return 0

    def extract_search_query(self, doc):
        query = ''
        verb_encountered = False

        for token in doc:
            if token.pos_ == 'VERB':
                verb_encountered = True
            elif verb_encountered and token.pos_ not in ['PUNCT', 'CCONJ']:
                query += token.text + ' '

        return query.strip()

    def analyze_context(self, target_word, sentence):
        analyzer = ContextAnalyzer(sentence)
        return analyzer.analyze_context(target_word)

    def get_plural_form(self, word):
        parsed_word = self.morph.parse(word)[0]
        if 'sing' in parsed_word.tag:
            return parsed_word.inflect({'plur'}).word
        return word

class ContextAnalyzer:
    def __init__(self, sentence):
        self.nlp = spacy.load("ru_core_news_md")
        self.doc = self.nlp(sentence.lower())

    def analyze_context(self, target_word):
        for token in self.doc:
            if token.text == target_word:
                context = {
                    "word": token.text,
                    "lemma": token.lemma_,
                    "pos": token.pos_,
                    "tag": token.tag_,
                    "dep": token.dep_,
                    "left_context": [t.text for t in token.lefts],
                    "right_context": [t.text for t in token.rights]
                }
                return context

# Пример использования
assistant = VoiceAssistant("config.json")
response = assistant.process_command()
print(response)
