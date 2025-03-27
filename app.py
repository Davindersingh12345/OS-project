from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

# Dictionary to store file descriptors
file_descriptors = {}

def secure_open(username, filename, mode):
    """ Securely open a file """
    try:
        return os.open(filename, mode, 0o644)
    except OSError:
        return -1

def secure_read(fd, buffer_size):
    """ Securely read from a file """
    try:
        return os.read(fd, buffer_size)
    except OSError:
        return b""

def secure_write(fd, content):
    """ Securely write to a file """
    try:
        os.write(fd, content.encode())
    except OSError:
        print("Error writing to file.")

@app.route('/')
def home():
    """ Serve the HTML page """
    return render_template("index.html")

@app.route('/open_file', methods=['POST'])
def open_file():
    """ Handle file opening from the frontend """
    data = request.json
    username = data.get("username")
    filename = data.get("filename")

    if username and filename:
        if filename in file_descriptors:
            os.close(file_descriptors[filename])

        fd = secure_open(username, filename, os.O_RDWR | os.O_CREAT)
        if fd < 0:
            return jsonify({"status": "error", "message": "Failed to open file"}), 400

        file_descriptors[filename] = fd
        return jsonify({"status": "success", "message": "File opened successfully"})
    
    return jsonify({"status": "error", "message": "Invalid data"}), 400

@app.route('/read_file', methods=['POST'])
def read_file():
    """ Handle file reading from the frontend """
    data = request.json
    filename = data.get("filename")

    if filename in file_descriptors:
        content = secure_read(file_descriptors[filename], 256)
        return jsonify({"status": "success", "content": content.decode()})
    
    return jsonify({"status": "error", "message": "File not opened"}), 400

@app.route('/write_file', methods=['POST'])
def write_file():
    """ Handle file writing from the frontend """
    data = request.json
    filename = data.get("filename")
    content = data.get("content")

    if filename in file_descriptors:
        secure_write(file_descriptors[filename], content)
        return jsonify({"status": "success", "message": "Content written successfully"})
    
    return jsonify({"status": "error", "message": "File not opened"}), 400

if __name__ == "__main__":
    app.run(debug=True)
