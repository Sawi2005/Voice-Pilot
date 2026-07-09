"""
Command interpreter for Voice Pilot.

Add or edit entries in APP_ALIASES to match the apps installed on your
own machine. Paths differ across Windows / macOS / Linux, so this module
detects the OS and launches apps accordingly.
"""

import os
import platform
import subprocess
import webbrowser
from datetime import datetime

NOTES_FILE = os.path.join(os.path.dirname(__file__), "notes.txt")

# Map spoken app names -> how to launch them per OS.
# Edit these to match what's actually installed on your machine.
APP_ALIASES = {
    "chrome": {
        "windows": "start chrome",
        "darwin": "open -a 'Google Chrome'",
        "linux": "google-chrome",
    },
    "notepad": {
        "windows": "notepad",
        "darwin": "open -a 'TextEdit'",
        "linux": "gedit",
    },
    "calculator": {
        "windows": "calc",
        "darwin": "open -a 'Calculator'",
        "linux": "gnome-calculator",
    },
    "vscode": {
        "windows": "code",
        "darwin": "open -a 'Visual Studio Code'",
        "linux": "code",
    },
    "terminal": {
        "windows": "start cmd",
        "darwin": "open -a 'Terminal'",
        "linux": "gnome-terminal",
    },
    "spotify": {
        "windows": "start spotify",
        "darwin": "open -a 'Spotify'",
        "linux": "spotify",
    },
}


def _current_os() -> str:
    system = platform.system().lower()
    if system.startswith("win"):
        return "windows"
    if system == "darwin":
        return "darwin"
    return "linux"


def open_app(app_name: str) -> str:
    app_name = app_name.strip().lower()
    entry = APP_ALIASES.get(app_name)

    if not entry:
        return f"I don't have {app_name} configured yet. Add it to APP_ALIASES in commands.py."

    cmd = entry.get(_current_os())
    if not cmd:
        return f"No launch command set for {app_name} on this OS."

    try:
        subprocess.Popen(cmd, shell=True)
        return f"Opening {app_name}."
    except Exception as e:
        return f"Couldn't open {app_name}: {e}"


def search_web(query: str) -> str:
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Searching the web for {query}."


def tell_time() -> str:
    now = datetime.now().strftime("%I:%M %p")
    return f"It's currently {now}."


def take_note(note_text: str) -> str:
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"[{timestamp}] {note_text}\n")
    return "Got it, I've saved that note."


def execute_command(heard: str) -> str:
    """
    Very simple rule-based intent matching. Swap this out for an NLP model
    or an LLM call later if you want smarter parsing.
    """
    heard = heard.lower().strip()

    if heard.startswith("open "):
        app_name = heard.replace("open ", "", 1)
        return open_app(app_name)

    if heard.startswith("search for ") or heard.startswith("search "):
        query = heard.replace("search for ", "").replace("search ", "", 1)
        return search_web(query)

    if "what time is it" in heard or "current time" in heard:
        return tell_time()

    if heard.startswith("note ") or heard.startswith("take a note "):
        note_text = heard.replace("take a note ", "").replace("note ", "", 1)
        return take_note(note_text)

    return "Sorry, I didn't understand that command."
