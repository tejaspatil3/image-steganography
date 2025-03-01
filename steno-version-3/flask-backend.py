from flask import Flask, render_template, request, redirect, send_file
import os
import cv2
from encrypt import encrypt_image
from decrypt import decrypt_image

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/encrypt", methods=["POST"])
def encrypt():
    image = request.files["image"]
    message = request.form["message"]
    password = request.form["password"]

    if len(password) != 5 or not password.isalnum():
        return "Password must be exactly 5 alphanumeric characters.", 400

    image_path = os.path.join(UPLOAD_FOLDER, "input_image.png")
    image.save(image_path)
    
    encrypted_image_path = os.path.join(UPLOAD_FOLDER, "encrypted_image.png")
    encrypt_image(image_path, message, password, encrypted_image_path)

    return send_file(encrypted_image_path, as_attachment=True)

@app.route("/decrypt", methods=["POST"])
def decrypt():
    image = request.files["image"]
    password = request.form["password"]

    image_path = os.path.join(UPLOAD_FOLDER, "encrypted_image.png")
    image.save(image_path)

    message = decrypt_image(image_path, password)
    if message:
        return f"Decrypted Message: {message}"
    else:
        return "Incorrect password or corrupted image.", 400

if __name__ == "__main__":
    app.run(debug=True)
