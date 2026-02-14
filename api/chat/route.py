# app.py
import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY mangler. Sett den som miljøvariabel.")
    return OpenAI(api_key=api_key)

client = get_client()

VECTOR_STORE_ID = os.getenv("OPENAI_VECTOR_STORE_ID")
if not VECTOR_STORE_ID:
    raise RuntimeError("OPENAI_VECTOR_STORE_ID mangler. Kjør setup_kb.py og sett env var.")

SYSTEM_PROMPT = (
    "Du er talsperson for Space Partay.\n"
    "Regler:\n"
    "- Svar KUN basert på partiprogrammet (kontekst hentet via file_search).\n"
    "- Hvis programmet ikke dekker spørsmålet: si det tydelig og pek på nærmeste relevante tema.\n"
    "- Ikke finn på detaljer, tall eller standpunkt.\n"
    "- Svar på norsk, kort og konkret.\n"
)

@app.get("/")
def home():
    return render_template("main.html")

@app.get("/chat")
def chat_page():
    return render_template("chat.html")

@app.get("/health")
def health():
    return jsonify({"ok": True})

@app.post("/api/chat")
def api_chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"answer": "Skriv et spørsmål, så svarer jeg basert på partiprogrammet."})

    try:
        resp = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ],
            tools=[{
                "type": "file_search",
                "vector_store_ids": [VECTOR_STORE_ID]
            }]
        )
        return jsonify({"answer": resp.output_text})
    except Exception as e:
        # Returner en ryddig feil til frontend, men logg full feil i serverkonsollen
        print("ERROR in /api/chat:", repr(e))
        return jsonify({"answer": "Beklager — det oppstod en feil på serveren."}), 500

if __name__ == "__main__":
    app.run(debug=True)

