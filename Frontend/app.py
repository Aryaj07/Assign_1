import os

import requests
from flask import Flask, jsonify, request, send_from_directory, redirect

from urllib.parse import urlencode, quote
import uuid

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


@app.get("/")
def root():
    return redirect("/cas/login")


@app.get("/cas/login")
def cas_login():
    callback = "https://sso.oit-gatech.com/cas/callback"

    service_params = {
        "session": "lab",
        "entityId": "https://lab.oit-gatech.com/saml2",
        "requestId": f"lab-{uuid.uuid4()}",
        "relayState": "simulation",
        "client": "lab-client"
    }

    service = callback + "?" + urlencode(service_params)

    return redirect(
        "/cas/login?" + urlencode({"service": service})
    )


@app.get("/sso_gatech_edu/cas/login/casservice")
def legacy_login():
    return redirect("/cas/login")


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