import olama_test
import pyttsx3
from RealtimeSTT import AudioToTextRecorder


def process_text(text):
    engine = pyttsx3.init()
    print(text)
    text = olama_test.Talk(text)

    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":

    recorder = AudioToTextRecorder(
        language="de"
    )

    while True:
        text = recorder.text()

        if text == "auto":
            exit()

        if not text:
            continue

        process_text(text)
