from flask import Flask, render_template, request, send_file
import os
from encrypt import encrypt_image
from decrypt import decrypt_image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])  # ✅ Ensure GET only
def index():
    return render_template("index.html")

@app.route("/encrypt", methods=["POST"])  # ✅ Ensure POST
def encrypt():
    if "image" not in request.files or "message" not in request.form or "password" not in request.form:
        return "Missing fields", 400

    image = request.files["image"]
    message = request.form["message"]
    password = request.form["password"]

    if len(password) != 5 or not password.isalnum():
        return "Password must be 5 alphanumeric characters.", 400

    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    output_path = os.path.join(OUTPUT_FOLDER, "encrypted.png")

    image.save(image_path)
    encrypt_image(image_path, message, password, output_path)

    return send_file(output_path, as_attachment=True)

@app.route("/decrypt", methods=["POST"])  # ✅ Ensure POST
def decrypt():
    if "image" not in request.files or "password" not in request.form:
        return "Missing fields", 400

    image = request.files["image"]
    user_password = request.form["password"]

    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    decrypted_message = decrypt_image(image_path, user_password)

    if decrypted_message is None:
        return "Incorrect password or no message found.", 400

    return decrypted_message

if __name__ == "__main__":
    app.run(debug=True)
