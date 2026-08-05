import os
import time

import requests
import serial
from dotenv import load_dotenv

load_dotenv()

SERIAL_PORT = os.getenv("SERIAL_PORT", "COM3")
SERIAL_BAUD = int(os.getenv("SERIAL_BAUD", "9600"))
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
KIOSK_LIEU = os.getenv("KIOSK_LIEU") or None

VALID_MOODS = {"content", "neutre", "pas_content"}


def send_vote(mood):
    response = requests.post(
        f"{BACKEND_URL}/api/votes",
        json={"humeur": mood, "source": "iot", "lieu": KIOSK_LIEU},
        timeout=5,
    )
    response.raise_for_status()


def handle_line(line):
    line = line.strip()
    if not line.startswith("VOTE:"):
        return

    mood = line.removeprefix("VOTE:").strip()
    if mood not in VALID_MOODS:
        print(f"Ligne série ignorée (humeur inconnue) : {line!r}")
        return

    try:
        send_vote(mood)
        print(f"Vote transmis : {mood}")
    except requests.RequestException as error:
        print(f"Échec d'envoi du vote '{mood}' au backend : {error}")


def run():
    print(f"Écoute du port série {SERIAL_PORT} @ {SERIAL_BAUD} bauds, backend {BACKEND_URL}")

    while True:
        try:
            with serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=1) as ser:
                print("Port série connecté.")
                while True:
                    raw_line = ser.readline().decode("utf-8", errors="ignore")
                    if raw_line:
                        handle_line(raw_line)
        except serial.SerialException as error:
            print(f"Port série indisponible ({error}), nouvelle tentative dans 3s...")
            time.sleep(3)


if __name__ == "__main__":
    run()
