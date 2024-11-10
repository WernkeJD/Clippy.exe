from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory clipboard data
clipboard_data = ""

# Endpoint to update clipboard data
@app.route('/clipboard', methods=['POST'])
def update_clipboard():
    global clipboard_data
    data = request.json.get('data', '')
    clipboard_data = data
    return jsonify({"status": "success"}), 200

# Endpoint to retrieve clipboard data
@app.route('/clipboard', methods=['GET'])
def get_clipboard():
    return jsonify({"data": clipboard_data}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

