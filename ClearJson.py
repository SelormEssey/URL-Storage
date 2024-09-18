import json

# Function to reset the JSON file
def reset_json_file(file_path):
    # Open the file in write mode and write an empty list or dictionary
    with open(file_path, 'w') as file:
        # If URLs are stored in a list
        json.dump([], file)
        # If URLs are stored in a dictionary, you can use this:
        # json.dump({}, file)
    print(f"The JSON file '{file_path}' has been reset.")

# Example usage
reset_json_file('shortened_urls.json')
reset_json_file('urls.json')