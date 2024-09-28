import json

def load_json_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def save_json_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Additional utility functions
