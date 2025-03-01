from flask import Flask, render_template, request, send_file
from stegano.lsb import hide, reveal
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/hide')
def hide_page():
    return render_template('hide.html')

@app.route('/view')
def view_page():
    return render_template('view.html')

@app.route('/stego/hide/image', methods=['POST'])
def hide_message():
    file = request.files['file']
    message = request.form['message']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Open image and convert to RGB to remove transparency
    image = image.open(file_path)
    if image.mode in ("P", "RGBA"):  
        image = image.convert("RGB")

    # Always save as PNG to maintain quality
    rgb_file_path = os.path.join(UPLOAD_FOLDER, "converted.png")
    image.save(rgb_file_path, format="PNG")

    # Ensure stegano works properly
    output_path = os.path.join(UPLOAD_FOLDER, "stego_image.png")
    hide(rgb_file_path, output_path, message)

    return send_file(output_path, as_attachment=True)



@app.route('/stego/extract/image', methods=['POST'])
def extract_message():
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        # Ensure the uploaded file is a valid image
        image = image.open(file_path)
        hidden_message = reveal(file_path)
        return hidden_message if hidden_message else "No hidden message found."
    
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)
