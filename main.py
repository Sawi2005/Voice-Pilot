"""
Voice Pilot - A simple Python voice assistant
Listens for a wake phrase, then executes voice commands like opening apps,
searching the web, telling the time, or taking quick notes.
"""

import sys
import speech_recognition as sr
import pyttsx3

from commands import execute_command


def build_speech_engine():
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)
    return engine


def speak(engine, text: str):
    print(f"[assistant] {text}")
    engine.say(text)
    engine.runAndWait()


def listen(recognizer: sr.Recognizer, mic: sr.Microphone, timeout: int = 5) -> str:
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("[listening...]")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            return ""

    try:
        text = recognizer.recognize_google(audio)
        print(f"[heard] {text}")
        return text.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"[error] Speech service unavailable: {e}")
        return ""


def main():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    engine = build_speech_engine()

    speak(engine, "Voice Pilot is online. Say a command whenever you're ready.")

    try:
        while True:
            heard = listen(recognizer, mic)
            if not heard:
                continue

            if "exit" in heard or "shut down" in heard or "quit" in heard:
                speak(engine, "Shutting down. Goodbye.")
                break

            response = execute_command(heard)
            if response:
                speak(engine, response)

    except KeyboardInterrupt:
        speak(engine, "Interrupted. Goodbye.")
        sys.exit(0)


if __name__ == "__main__":
    main()
