import json
import uuid
import re
import threading
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

class URLShortener:
    def __init__(self, data_file='urls.json'):
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def validate_url(self, url):
        pattern = re.compile(
            r'^(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]*[-A-Za-z0-9+&@#/%=~_|]$'
        )
        return bool(pattern.match(url))

    def shorten_url(self, url):
        if not self.validate_url(url):
            raise ValueError("Invalid URL")
        uid = str(uuid.uuid4())[:11]  # generate a unique ID (less than 12 ASCII chars)
        self.data[uid] = url
        self.save_data()
        return f"http://localhost:5000/{uid}"

    def get_original_url(self, short_id):
        return self.data.get(short_id, None)

    def count_shortened_urls(self):
        return len(self.data)

# Create an instance of the URLShortener
shortener = URLShortener()


@app.route('/shorten', methods=['POST'])
def shorten():
    try:
        url = request.form['url']
        short_url = shortener.shorten_url(url)
        return jsonify({'shortened_url': short_url}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/<short_id>', methods=['GET'])
def redirect_to_original(short_id):
    original_url = shortener.get_original_url(short_id)
    if original_url:
        return redirect(original_url)
    else:
        return jsonify({'error': 'Shortened URL not found'}), 404

@app.route('/count', methods=['GET'])
def count_shortened_urls():
    total = shortener.count_shortened_urls()
    return jsonify({'total_shortened_urls': total}), 200
