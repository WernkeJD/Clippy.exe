from flask import Flask, request, jsonify
import os

# Function to read from a file
def read_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    return ""

# Function to write to a file
def write_to_file(file_path, data):
    with open(file_path, 'w') as file:
        file.write(data)

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

# Endpoint to update clipboard data
@app.route('/clipboard', methods=['POST'])
def updateclipboard():
    clipboard_data = request.json.get('data', '')
    write_to_file('clipboard.txt', clipboard_data)
    return jsonify({"status": "success"}), 200

# Endpoint to retrieve clipboard data
@app.route('/clipboard', methods=['GET'])
def get_clipboard():
    clipboard_data = read_from_file('clipboard.txt')
    return jsonify({"data": clipboard_data}), 200

def run_server():
    app.run(debug=True, host='172.16.2.241', port=5000)

if __name__ == '__main__':
    run_server()