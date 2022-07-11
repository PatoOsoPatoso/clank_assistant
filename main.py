#!/usr/bin/python3

import os
import vlc
import json
import argparse
import queue
import sounddevice as sd
import vosk
import getpass
from time import sleep
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import load_dotenv

# Similar sounds
names = ["clan gsm", "clan", "clac", "asistente"]

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

ibm_authenticator = os.environ.get("IBM_AUTH")
service_url = os.environ.get("SERVICE_URL")

program_paths = []

if os.name == 'nt':
    program_paths.append(rf"C:\Users\{getpass.getuser()}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs")
    program_paths.append(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs")
else:
    # Implement Linux part...
    pass

def clank(text):
    posible = [n for n in names if n in text.lower()]
    if not posible:
        return None

    # The first return parameter is just for testing
    _, command, target = extractParameters(text, posible[0])

    if command in commands["abrir"]:
        abrir(target)
    elif command in commands["apagar"]:
        apagar()
    elif command in commands["parar"]:
        pauseSound()
    elif command in commands["seguir"]:
        unpauseSound()
    elif command in commands["detener"]:
        stopSound()
    elif command in commands["repetir"]:
        repeat(target)
    else:
        playSound("no_command")


def repeat(target):
    if not target:
        playSound("no_repeat")
        return

    synthesizeSound(target)
    playSound("sound")


def abrir(target):
    result_target = [k for k, v in targets.items() if target in v]

    results = {}

    print(target)
    print(result_target)

    if not result_target:
        result_target = [target]
    
    for program_path in program_paths:
        for dirpath, dirnames, files in os.walk(program_path):
            for name in files:
                matches = len([x for x in name.lower().split() if x in result_target[0].split()])
                if matches > 0: results[os.path.normpath(dirpath + "/" + name)] = matches

    if not results:
        playSound("no_target")
        return
    
    result = sorted(results.items(), key=lambda x: x[1], reverse=True)
    os.startfile(result[0][0])


def apagar():
    playSound("closing")
    sleep(2)
    exit()


def playSound(f):
    stopSound()
    media = instance.media_new(f"audio/{f}.wav")
    player.set_media(media)
    player.play()


def pauseSound():
    player.pause()


def unpauseSound():
    player.play()


def stopSound():
    player.stop()


def synthesizeSound(text):
    authenticator = IAMAuthenticator(ibm_authenticator)
    text_to_speech = TextToSpeechV1(authenticator=authenticator)

    text_to_speech.set_service_url(service_url)

    with open('audio/sound.wav', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(text,
                                      voice='es-ES_EnriqueV3Voice',
                                      accept='audio/wav').get_result().content)


def extractParameters(text, name):
    sentence = text.lower().split(name, 1)[1].strip()
    command = sentence.split()[0] if sentence else ""
    target = " ".join(sentence.split()[1:]) if sentence else ""

    # sentence is just for testing
    return sentence, command, target


instance = vlc.Instance()
player = instance.media_player_new()

# List of commands and possible spanish matches
commands = {
    "abrir": ["abre", "enciende", "enchufa"],
    "apagar":
    ["ciérrate", "apágate", "apaga", "apagate", "cierrate", "cierra"],
    "parar": ["para"],
    "seguir": ["sigue"],
    "detener": ["detente", "cállate"],
    "repetir": ["repite"]
}

# List of targets and possible spanish targets
targets = {
    "directo.pyw": ["directo", "el directo"],
    "lol": ["el lol", "league of legends", "league", "lol"],
    "discord": ["discord", "el discord"],
    "minecraft": ["minecraft", "el minecraft"],
    "brave": ["navegador", "el navegador", "brave"],
    "whatsapp": ["whatsapp"],
    "whatsappweb.url": ["whatsapp web"],
    "youtube.url": ["youtube"],
    "blitz": ["blitz"],
    "twitch.url": ["twitch"],
    "twitter.url": ["twitter"],
    "blender": ["blender"],
    "unity": ["unity", "unity hub"],
    "code": ["visual studio code", "visual studio", "code", "vscode"],
    "streamlabs": ["stream", "streamlabs", "stream labs", "obs"],
    "torrent": ["torrent", "qbitorrent", "bittorrent"],
    "spotify": ["spotify"],
    "spotifyweb.url": ["spotify web"],
    "steam": ["steam"],
    "epic": ["epic games", "epic"],
    "teams": ["microsoft teams", "teams"],
    "plutonium": ["plutonium", "call of duty", "black ops 2"],
    "ubisoft connect": ["ubisoft connect", "visor conecto", "un visor conector"]
}


def startEngine():
    q = queue.Queue()
    vosk.SetLogLevel(-1)

    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    parser = argparse.ArgumentParser()
    args, remaining = parser.parse_known_args()

    parser.add_argument('-d', '--device', type=int)
    args = parser.parse_args(remaining)

    try:
        device_info = sd.query_devices(args.device, 'input')
        args.samplerate = int(device_info['default_samplerate'])

        model = vosk.Model("model")

        with sd.RawInputStream(samplerate=args.samplerate,
                               blocksize=8000,
                               device=args.device,
                               dtype='int16',
                               channels=1,
                               callback=callback):
            rec = vosk.KaldiRecognizer(model, args.samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    clank(json.loads(rec.Result())["text"])

    except KeyboardInterrupt:
        parser.exit(0)
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))


if __name__ == "__main__":
    startEngine()
