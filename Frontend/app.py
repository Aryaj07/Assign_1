import os

import requests
from flask import Flask, jsonify, request, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

API_INTERNAL_URL = os.environ.get(
    "API_INTERNAL_URL",
    "http://127.0.0.1:3000"
)

app = Flask(
    __name__,
    static_folder=STATIC_DIR,
    static_url_path=""
)


@app.get("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.get("/sso_gatech_edu/cas/login/casservice")
def home():
    return send_from_directory(
        STATIC_DIR,
        "index.html"
    )


@app.post("/api/submit")
def submit():
    try:
        response = requests.post(
            f"{API_INTERNAL_URL}/api/submit",
            json=request.get_json(silent=True),
            timeout=10
        )

        return (
            response.content,
            response.status_code,
            {
                "Content-Type": "application/json"
            }
        )

    except requests.RequestException as e:
        print(f"Backend request failed: {e}")

        return jsonify({
            "success": False,
            "message": "Simulation backend unavailable."
        }), 503


@app.get("/api/submissions")
def submissions():
    try:
        response = requests.get(
            f"{API_INTERNAL_URL}/api/submissions",
            timeout=10
        )

        return (
            response.content,
            response.status_code,
            {
                "Content-Type": "application/json"
            }
        )

    except requests.RequestException as e:
        print(f"Backend request failed: {e}")

        return jsonify({
            "success": False,
            "message": "Simulation backend unavailable."
        }), 503


@app.get("/admin")
def admin():
    return send_from_directory(
        STATIC_DIR,
        "admin.html"
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )