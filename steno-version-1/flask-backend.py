from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
import re
from werkzeug.utils import secure_filename
from encrypt import encrypt_message
from decrypt import decrypt_message

app = Flask(__name__, static_folder="static")
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "static/uploaded_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Utility function to check password validity
def is_valid_password(password):
    return bool(re.match(r"^[a-zA-Z0-9]{5}$", password))  # 5-char alphanumeric

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/encrypt", methods=["POST"])
def encrypt():
    if "image" not in request.files or "message" not in request.form or "password" not in request.form:
        flash("All fields are required!", "danger")
        return redirect(url_for("home"))

    image = request.files["image"]
    message = request.form["message"]
    password = request.form["password"]

    if not is_valid_password(password):
        flash("Password must be exactly 5 characters (alphanumeric).", "danger")
        return redirect(url_for("home"))

    filename = secure_filename(image.filename)
    img_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(img_path)

    encrypted_img_path = os.path.join(UPLOAD_FOLDER, "encrypted_" + filename)
    success = encrypt_message(img_path, password, message, encrypted_img_path)

    if success:
        flash("Message successfully encrypted!", "success")
        return render_template("index.html", encrypted_image=encrypted_img_path)
    else:
        flash("Encryption failed!", "danger")
        return redirect(url_for("home"))

@app.route("/decrypt", methods=["POST"])
def decrypt():
    if "image" not in request.files or "password" not in request.form or "message_length" not in request.form:
        flash("All fields are required!", "danger")
        return redirect(url_for("home"))

    image = request.files["image"]
    entered_password = request.form["password"]
    message_length = int(request.form["message_length"])

    filename = secure_filename(image.filename)
    img_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(img_path)

    extracted_password, extracted_message = decrypt_message(img_path, message_length)

    print(extracted_password)
    print(entered_password)
    if extracted_password is None:
        flash("Decryption failed!", "danger")
        return redirect(url_for("home"))

    if entered_password == extracted_password:
        flash(f"Decryption successful! Message: {extracted_message}", "success")
    else:
        flash("Incorrect password! Decryption failed.", "danger")

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
