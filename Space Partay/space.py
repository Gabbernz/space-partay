from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

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

@app.get("/health")
def health():
    return jsonify({"ok": True})

@app.post("/api/chat")
def api_chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"answer": "Skriv et spørsmål, så svarer jeg basert på partiprogrammet."})

    # Midlertidig test: Echo. Bytt ut med OpenAI/LangChain senere.
    return jsonify({"answer": f"Echo: {message}"})



if __name__ == "__main__":
    app.run(debug=True)

