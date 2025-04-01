from flask import Flask, request, jsonify, render_template
import os
import json

app = Flask(__name__)
FILES_DIRECTORY = "files"
PASSWORDS_FILE = "passwords.json"
OPEN_FILES = set()  # Track opened files

# Ensure directory exists
if not os.path.exists(FILES_DIRECTORY):
    os.makedirs(FILES_DIRECTORY)

# Load or initialize password storage
if os.path.exists(PASSWORDS_FILE):
    with open(PASSWORDS_FILE, "r") as f:
        passwords = json.load(f)
else:
    passwords = {}

def save_passwords():
    with open(PASSWORDS_FILE, "w") as f:
        json.dump(passwords, f, indent=4)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/set_password", methods=["POST"])
def set_password():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    filename = data.get("filename")
    
    if not username or not password or not filename:
        return jsonify({"status": "error", "message": "All fields are required!"})
    
    if username not in passwords:
        passwords[username] = {}
    
    # Store password in plain text (not secure)
    passwords[username][filename] = password
    save_passwords()
    return jsonify({"status": "success", "message": "Password set successfully!"})

@app.route("/open_file", methods=["POST"])
def open_file():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    filename = data.get("filename")
    
    if not username or not password or not filename:
        return jsonify({"status": "error", "message": "All fields are required!"})
    
    if username in passwords and passwords[username].get(filename) == password:
        file_path = os.path.join(FILES_DIRECTORY, filename)
        open(file_path, "a").close()
        OPEN_FILES.add(filename)  # Mark file as opened
        return jsonify({"status": "success", "message": "File opened successfully!"})
    
    return jsonify({"status": "error", "message": "Invalid credentials!"})

@app.route("/read_file", methods=["POST"])
def read_file():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    filename = data.get("filename")
    
    if not username or not password or not filename:
        return jsonify({"status": "error", "message": "All fields are required!"})
    
    if filename not in OPEN_FILES:
        return jsonify({"status": "error", "message": "File not open!"})
    
    if username in passwords and passwords[username].get(filename) == password:
        file_path = os.path.join(FILES_DIRECTORY, filename)
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                content = f.read()
            return jsonify({"status": "success", "message": "File read successfully!", "content": content})
    
    return jsonify({"status": "error", "message": "Invalid credentials or file not found!"})

@app.route("/write_file", methods=["POST"])
def write_file():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    filename = data.get("filename")
    content = data.get("content")
    
    if not username or not password or not filename or not content:
        return jsonify({"status": "error", "message": "All fields are required!"})
    
    if filename not in OPEN_FILES:
        return jsonify({"status": "error", "message": "File not open!"})
    
    if username in passwords and passwords[username].get(filename) == password:
        file_path = os.path.join(FILES_DIRECTORY, filename)
        with open(file_path, "w") as f:
            f.write(content)
        return jsonify({"status": "success", "message": "File written successfully!"})
    
    return jsonify({"status": "error", "message": "Invalid credentials!"})

@app.route("/delete_file", methods=["POST"])
def delete_file():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    filename = data.get("filename")
    
    if not username or not password or not filename:
        return jsonify({"status": "error", "message": "All fields are required!"})
    
    if filename not in OPEN_FILES:
        return jsonify({"status": "error", "message": "File not open!"})

    if username in passwords and passwords[username].get(filename) == password:
        file_path = os.path.join(FILES_DIRECTORY, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({"status": "success", "message": "File deleted successfully!"})
    
    return jsonify({"status": "error", "message": "Invalid credentials or file not found!"})

@app.route("/list_files", methods=["GET"])
def list_files():
    files = os.listdir(FILES_DIRECTORY)
    return jsonify({"status": "success", "files": files})

if __name__ == "__main__":
    app.run(debug=True)
