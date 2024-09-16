# URL-Storage
an application to store URL’s of any length and return a shortened version of the URL

import json
import hashlib
import validators
import os

class URLShortener:
    def __init__(self, storage_file='urls.json'):
        self.storage_file = storage_file
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                self.url_data = json.load(f)
        else:
            self.url_data = {}
    
    def save_data(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self.url_data, f)
    
    def is_valid_url(self, url):
        return validators.url(url)
    
    def shorten_url(self, original_url):
        if not self.is_valid_url(original_url):
            return "Invalid URL"
        
        # Create a unique shortened URL ID (using MD5 hash)
        short_id = hashlib.md5(original_url.encode()).hexdigest()[:12]
        shortened_url = f"https://myApp.com/{short_id}"
        
        # Store the mapping
        self.url_data[shortened_url] = original_url
        self.save_data()
        
        return shortened_url
    
    def expand_url(self, short_url):
        return self.url_data.get(short_url, "URL not found")
    
    def count_urls(self):
        return len(self.url_data)

# Example usage
shortener = URLShortener()

while True:
    choice = input("1. Shorten URL\n2. Expand URL\n3. Count URLs\nEnter your choice: ")
    
    if choice == '1':
        url = input("Enter the full URL: ")
        print("Shortened URL:", shortener.shorten_url(url))
    elif choice == '2':
        short_url = input("Enter the shortened URL: ")
        print("Original URL:", shortener.expand_url(short_url))
    elif choice == '3':
        print("Total URLs shortened:", shortener.count_urls())
    else:
        print("Invalid choice!")
