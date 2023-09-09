import pyaudio
import vosk
import json

model_path = "models_stt/vosk-model-small-ru-0.22" # vosk-model-small-ru-0.22 или vosk-model-ru-0.42
model = vosk.Model(model_path)
rec = vosk.KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio() # начинаем слушать микрофон
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

print("Слушаю...")

while True:
    data = stream.read(4000, exception_on_overflow=False)
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        text = result.get('text')
        print(text)
        if "привет" in text:
            print("Да, я здесь!")