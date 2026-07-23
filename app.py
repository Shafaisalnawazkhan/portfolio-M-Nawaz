import urllib.parse
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
PORTFOLIO_DIR = BASE_DIR / "portfolio"

WHATSAPP_NUMBER = "918431803243"
WHATSAPP_BASE_URL = "https://wa.me/"
EMAIL_TO = "nawazmhyr@gmail.com"


@app.route('/')
def home():
    return send_from_directory(PORTFOLIO_DIR, 'index.html')


@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip()
    message = (data.get('message') or '').strip()

    if not name or not email or not message:
        return jsonify({'success': False, 'error': 'Please provide your name, email, and message.'}), 400

    message_text = f"New portfolio contact\nName: {name}\nEmail: {email}\nMessage: {message}"

    whatsapp_text = urllib.parse.quote(message_text)
    whatsapp_url = f"{WHATSAPP_BASE_URL}{WHATSAPP_NUMBER}?text={whatsapp_text}"

    subject = urllib.parse.quote(f"New portfolio contact from {name}")
    body = urllib.parse.quote(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")
    mailto_url = f"mailto:{EMAIL_TO}?subject={subject}&body={body}"

    return jsonify({'success': True, 'whatsappUrl': whatsapp_url, 'mailtoUrl': mailto_url})


@app.route('/<path:filename>')
def serve_portfolio_file(filename):
    return send_from_directory(PORTFOLIO_DIR, filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
