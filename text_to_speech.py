import os
import torch
import sounddevice as sd


def text_to_speech():
    device = torch.device('cpu')
    torch.set_num_threads(4)
    local_file = 'models/model.pt'

    if not os.path.isfile(local_file):
        torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v4_ru.pt',
                                       local_file)

    model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
    model.to(device)

    example_text = 'Даниэль приветствую! Я результат синтеза... Надеюсь у тебя получится развернуть сервер с гитлабом.'
    sample_rate = 48000
    speaker='aidar' # aidar, baya, kseniya, xenia, eugene, random
    # audio_paths = model.save_wav(text=example_text,
    #                              speaker=speaker,
    #                              sample_rate=sample_rate)

    def speaker_silero(text1):
        audio = model.apply_tts(text=text1,
                                    speaker=speaker,
                                    sample_rate=sample_rate)

        sd.play(audio, blocking=False)

    while True:
        print('Text please')
        speaker_silero(input())