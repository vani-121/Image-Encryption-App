from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import os
from rsa_utils import generate_keys, encrypt_image, decrypt_image

app = Flask(__name__)
app.secret_key = "secret_key_for_flash"

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'POST':
        file = request.files.get('image')
        if not file:
            flash("No file selected!")
            return redirect(request.url)

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Generate keys if not exist
        if not os.path.exists("public.pem") or not os.path.exists("private.pem"):
            generate_keys()

        encrypted_path = encrypt_image(filepath)
        flash(f"Image encrypted successfully! Saved as {encrypted_path}")
        return render_template("encrypt.html", encrypted_file=encrypted_path)

    return render_template("encrypt.html")

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    if request.method == 'POST':
        file = request.files.get('image')
        private_key_text = request.form.get('private_key')

        if not file or not private_key_text:
            flash("Please select an encrypted file and enter the private key.")
            return redirect(request.url)

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        try:
            decrypted_path = decrypt_image(filepath, private_key_text)
            flash(f"Image decrypted successfully! Saved as {decrypted_path}")
            return render_template("decrypt.html", decrypted_file=decrypted_path)
        except Exception as e:
            flash(f"Decryption failed: {str(e)}")
            return redirect(request.url)

    return render_template("decrypt.html")

if __name__ == "__main__":
    app.run(debug=True)
