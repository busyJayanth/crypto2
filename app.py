from flask import Flask, request, render_template, send_file
from cryptography.fernet import Fernet

app = Flask(__name__)

# Secret key for encryption and decryption
secret_key = Fernet.generate_key()
fernet = Fernet(secret_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'mp4_file' in request.files:
        mp4_file = request.files['mp4_file']
        if mp4_file.filename != '':
            encrypted_data = fernet.encrypt(mp4_file.read())
            with open('encrypted.mp4', 'wb') as encrypted_file:
                encrypted_file.write(encrypted_data)
            return "File encrypted and saved as encrypted.mp4. <a href='/download/encrypted'>Download</a>"
    return "File not provided."

@app.route('/decrypt', methods=['POST'])
def decrypt():
    if 'encrypted_file' in request.files:
        encrypted_file = request.files['encrypted_file']
        if encrypted_file.filename != '':
            decrypted_data = fernet.decrypt(encrypted_file.read())
            with open('decrypted.mp4', 'wb') as decrypted_file:
                decrypted_file.write(decrypted_data)
            return "File decrypted and saved as decrypted.mp4. <a href='/download/decrypted'>Download</a>"
    return "File not provided."

@app.route('/download/<file_type>')
def download_file(file_type):
    if file_type == 'encrypted':
        return send_file('encrypted.mp4', as_attachment=True, download_name='encrypted.mp4')
    elif file_type == 'decrypted':
        return send_file('decrypted.mp4', as_attachment=True, download_name='decrypted.mp4')

if __name__ == '__main__':
    app.run(debug=True)
