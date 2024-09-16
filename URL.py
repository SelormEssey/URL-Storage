#### START 1
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

