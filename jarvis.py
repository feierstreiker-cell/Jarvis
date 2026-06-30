import asyncio, edge_tts, os, datetime
from playsound import playsound
from ddgs import DDGS

def speak(text):
    print(f"Jarvis: {text}")
    async def run_tts():
        communicate = edge_tts.Communicate(text, "de-DE-KatjaNeural", rate="-4%")
        await communicate.save("temp.mp3")
    asyncio.run(run_tts())
    playsound("temp.mp3")
    os.remove("temp.mp3")

def suche_im_internet(frage):
    frage_klein = frage.lower()

    # Spezialfall Wetter - echte Daten
    if "wetter" in frage_klein:
        try:
            import requests
            ort = "Meißen"
            if " in " in frage_klein:
                ort = frage_klein.split(" in ")[-1].strip().title()
            antwort = requests.get(f"https://wttr.in/{ort}?format=3", timeout=5).text
            return antwort
        except:
            pass

    # normaler Fall
    try:
        with DDGS() as ddgs:
            ergebnisse = list(ddgs.text(frage, max_results=1, region="de-de"))
            if ergebnisse:
                return ergebnisse[0]['body']
    except:
        pass
    return ""

def ask_jarvis(frage):
    try:
        internet_wissen = ""
        if any(w in frage.lower() for w in ["heute", "aktuell", "wetter", "nachrichten", "datum", "wer ist", "was ist", "preis", "börse", "internet"]):
            internet_wissen = suche_im_internet(frage)

        if internet_wissen:
            return internet_wissen

        return "Dazu habe ich gerade keine aktuellen Infos gefunden, aber ich höre dir zu."
    except Exception as e:
        print(f"Fehler: {e}")
        return "Entschuldige, ich konnte gerade nicht nachdenken."

speak("Hallo, ich bin Jarvis. Ich bin jetzt intelligent und habe Internet.")

while True:
    befehl = input("Du: ")
    if "zeit" in befehl.lower():
        jetzt = datetime.datetime.now().strftime("%H:%M")
        speak(f"Es ist {jetzt} Uhr")
    elif "ende" in befehl.lower() or "tschüss" in befehl.lower():
        speak("Bis später")
        break
    else:
        antwort = ask_jarvis(befehl)
        speak(antwort)