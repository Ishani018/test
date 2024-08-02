from flask import Flask, render_template, request, redirect, send_file
import os

app = Flask(__name__)
app.secret_key = "flower123456"


@app.route("/")
def home():
    return render_template("base.html")


