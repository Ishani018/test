from flask import Flask

app = Flask(__name__)
app.secret_key = "flower123456"

@app.route('/home')
def home():
    return "Hello world"