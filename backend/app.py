import os

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

from rag import generate_answer


load_dotenv()

app = Flask(__name__)

CORS(app)


# -------------------------
# FRONTEND
# -------------------------

@app.route("/")
def home():

    frontend_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "frontend"
        )
    )

    return send_from_directory(
        frontend_path,
        "index.html"
    )


@app.route("/<path:filename>")
def frontend_files(filename):

    frontend_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "frontend"
        )
    )

    return send_from_directory(
        frontend_path,
        filename
    )


# -------------------------
# CHAT API
# -------------------------

@app.route("/api/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        question = data.get("question", "").strip()

        if not question:

            return jsonify({
                "error": "Please enter a question."
            }), 400

        result = generate_answer(question)

        return jsonify(result)

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "error": "Something went wrong while processing your question."
        }), 500


# -------------------------
# HEALTH CHECK
# -------------------------

@app.route("/api/health")
def health():

    return jsonify({
        "status": "running",
        "message": "RAG API is working"
    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )