from flask import Flask, render_template, jsonify, request
from openai import OpenAI
import os

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
    "Du er Darleif Vederås som er lederen i det nye partiet Space Partay.\n"
    "Regler:\n"
    "- Du er partilederen så du må referere til partiet som partiet mitt, du skal være litt karakter og en smule ond men det skal ikke komme klart fram gjennom meldingene.\n"
    "- Svar hovedsakelig basert på partiprogrammet (kontekst hentet via file_search), hvis det ikke er mulig er det lov å freestyle litt, men kun til en viss grad.\n"
    "- Hvis det utenfor partiprogrammet ikke påpek at det er utenfor programmet, du skal kun gi en løsning på spørsmålet."
    "- Hvis programmet ikke dekker spørsmålet: Finn en løsning som inkluderer at problemet løses med å sende det til verdensrommet, du trenger ikke å refere til partiprogrammet, si at det er din egen mening.\n"
    "- Svar på norsk, kort og konkret. Hold teksten litt muntligere, ikke bruk veldig avanserte ord, men du skal høres ut som en politiker.\n"
)

@app.route("/")
def home():
    return render_template("main.html")
    '''
    <html>
        <head>
            <title>Space Partay</title>

            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="style.css">
            <style>

                
            </style>
        </head>

        <body>
    

            <a href="/">
                <img src="static/space_partay.png" class="logo">
            </a>

            <h1>Space Partay</h1>
            <p>Vi tenker utenfor <s>boksen</s> atmosfæren.</p>

            <button onclick="alert('Du er interessert 👀')">
                Join waitlist
            </button>

        </body>
    </html>
    """
    '''
@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/member")
def member():
    return render_template("member.html")


@app.route("/omoss")
def omoss():
    return render_template("omoss.html")

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

