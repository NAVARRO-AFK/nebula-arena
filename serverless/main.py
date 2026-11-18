import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB = "/data/scores.db"

def conectar():
    c = sqlite3.connect(DB)
    c.execute("CREATE TABLE IF NOT EXISTS scores (jugador TEXT PRIMARY KEY, puntos INTEGER NOT NULL DEFAULT 0)")
    c.commit()
    return c

@app.post("/score")
def guardar():
    d = request.get_json()
    c = conectar()
    try:
        with c:
            c.execute("INSERT INTO scores (jugador, puntos) VALUES (?, ?) "
                      "ON CONFLICT(jugador) DO UPDATE SET puntos = puntos + excluded.puntos",
                      (d["jugador"], int(d["puntos"])))
    finally:
        c.close()
    return "ok", 201

@app.get("/top")
def top():
    c = conectar()
    try:
        rows = c.execute("SELECT jugador, puntos FROM scores ORDER BY puntos DESC LIMIT 10").fetchall()
    finally:
        c.close()
    return jsonify([{"jugador": j, "puntos": p} for j, p in rows])

@app.get("/health")
def health():
    return "ok"
