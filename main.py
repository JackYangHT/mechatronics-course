import os

from flask import Flask, send_file, jsonify
import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK
cred = credentials.Certificate("src/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)

@app.route("/")
def index():
    return send_file('src/index.html')

@app.route("/token")
def token():
    # This is a placeholder UID. In a real application, you would create
    # a unique identifier for each user.
    uid = 'some-uid'
    custom_token = auth.create_custom_token(uid)
    return jsonify({'token': custom_token.decode('utf-8')})

def main():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    main()
