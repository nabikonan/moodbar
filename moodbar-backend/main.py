import os
from typing import Literal, Optional

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from db import get_connection

app = FastAPI(title="Moodbar API")


class Vote(BaseModel):
    humeur: Literal["content", "neutre", "pas_content"]
    source: Literal["web", "iot"]
    lieu: Optional[str] = None


@app.post("/api/votes", status_code=201)
def create_vote(vote: Vote):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO votes (humeur, source, lieu) VALUES (%s, %s, %s)",
        (vote.humeur, vote.source, vote.lieu),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"status": "ok"}


@app.get("/api/votes")
def list_votes(limit: int = 100):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, humeur, horodatage, source, lieu FROM votes ORDER BY horodatage DESC LIMIT %s",
        (limit,),
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


# sert le frontend statique (index.html/kiosk.html) depuis la même app, pour rester sur une seule origine (pas de CORS, un seul service à déployer)
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "moodbar-frontend")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
