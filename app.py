from flask import Flask,render_template

app = Flask(__name__)
app.secret_key = "flower123456"

@app.route('/home')
def home():
    return render_template("base.html")