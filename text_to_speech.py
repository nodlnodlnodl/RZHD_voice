import pyttsx3
#from model import using_trained_model...

def greetings():
    engine = pyttsx3.init()     # инициализация
    engine.setProperty('rate', 150)     # скорость речи
    engine.setProperty('volume', 0.9)
    engine.say('   ' + "Приветствую уважаемый, слушаю ваш вопрос!")  # запись фразы в очередь
    engine.runAndWait()

def answering_question(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    engine.say('   ' + using_trained_model(text))