import speech_recognition as sr

def text_from_speech():
    r = sr.Recognizer()
    mic = sr.Microphone()

    sr.LANGUAGE = 'ru-RU'

    with mic as source:
        r.adjust_for_ambient_noise(source)
        print('Сей самфинг')
        audio = r.listen(source)

    text = r.recognize_google(audio, language='ru-RU')
    print(f'ты высрал: {text}')