import olama_test as ot
import pyttsx3
from RealtimeSTT import AudioToTextRecorder

def process_text(text):
    engine = pyttsx3.init()
    print(text)

    text = ot.Talk(text)

    engine.say(text)
    engine.runAndWait()



if __name__ == "__main__":
    recorder = AudioToTextRecorder(language="de")

    while True:

        text = recorder.text()

        if text == "auto":
            break

        if not text:
            continue

        process_text(text)
