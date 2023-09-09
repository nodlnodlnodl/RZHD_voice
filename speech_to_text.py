import pyaudio
import vosk
import json
from text_to_speech import greetings, answering_question
import time

def bot_activation():
    WAITING_FOR_ACTIVATION = True
    BOT_NAME = 'бот'

    model_path = "models_stt/vosk-model-small-ru-0.22" # vosk-model-small-ru-0.22 или vosk-model-ru-0.42
    model = vosk.Model(model_path)
    rec = vosk.KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio() # начинаем слушать микрофон
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    print("Ожидание обращения или нажатия на кнопку")
    last_time_heard = 0
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get('text')
            print(text)

            if WAITING_FOR_ACTIVATION == True and BOT_NAME in text:
                greetings()
                WAITING_FOR_ACTIVATION = False
                last_time_heard = time.time()

            elif WAITING_FOR_ACTIVATION == False and text != '':
                answering_question(text)
                print('типа ответил на вопрос')
                last_time_heard = time.time()

        if WAITING_FOR_ACTIVATION == False and time.time() - last_time_heard > 5:
            WAITING_FOR_ACTIVATION = True
            print('переход в режим ожидания')
