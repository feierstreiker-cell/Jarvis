from logging import fatal
import os
import olama_test as ot
import fenster_test as ft
import pyttsx3
from RealtimeSTT import AudioToTextRecorder
import threading

running = True
recorder = None

def process_text(text,ui):
    engine = pyttsx3.init()
    print(text)
    ui.set_state("thinking")
    text = ot.Talk(text)

    ui.set_state("speaking")
    engine.say(text)
    engine.runAndWait()

    ui.set_state("idle")


def assistant_loop(ui,rec):
    global running

    while running:
        ui.set_state("listening")

        text = rec.text()

        if not text:
            continue

        process_text(text, ui)

def onexit():
    global running, recorder
    running = False
    try:
        if recorder:
            try:
                recorder.stop()
            except:
                pass
            try:
                recorder.shutdown()
            except:
                pass
            try:
                recorder.close()
            except:
                pass
    except:
        pass

    try:
        ui.root.destroy()
    except:
        pass

if __name__ == "__main__":
    ui = ft.AssistantUI()

    recorder = AudioToTextRecorder(language="de")

    # run assistant in background thread
    threading.Thread(target=assistant_loop, args=(ui,recorder), daemon=True).start()

    # IMPORTANT: tkinter runs in main thread
    ui.root.protocol("WM_DELETE_WINDOW",onexit)
    ui.root.mainloop()
