from flask import Flask, render_template, request, redirect, send_file,url_for
import os

app = Flask(__name__)
app.secret_key = "flower123456"

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOWNLOAD_FOLDER'] = 'downloads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['DOWNLOAD_FOLDER']):
    os.makedirs(app.config['DOWNLOAD_FOLDER'])

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/help")
def help_page():
    return render_template("help.html")

@app.route("/upload", methods=["POST", "GET"])
def upload():
    formatted_poem = ""
    download_path = ""

    if request.method == "POST":
        content = request.form.get('content')
        same_length = request.form.get('same_length')
        stanza_lengths_str = request.form.get('stanza_lengths')
        file = request.files.get('file')

        if file and file.filename:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            with open(file_path, 'r') as f:
                content = f.read()

        if content:
            if same_length == 'on':
                try:
                    length = int(stanza_lengths_str)
                    formatted_poem = uniform_process_poem(content, length)
                except ValueError:
                    formatted_poem = "Invalid stanza length provided."
            else:
                lengths = non_uniform_length(stanza_lengths_str)
                formatted_poem = non_uniform_process_poem(content, lengths)

            # Save the formatted poem to a text file
            poem_filename = "formatted_poem.txt"
            download_path = os.path.join(app.config['DOWNLOAD_FOLDER'], poem_filename)
            with open(download_path, 'w') as f:
                f.write(formatted_poem)

    return render_template("upload.html", formatted_poem=formatted_poem, download_path=download_path)

@app.route("/download/<filename>")
def download_file(filename):
    return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], filename), as_attachment=True)

def uniform_process_poem(content, length):
    lines = content.splitlines()
    first_line = lines[0].strip()
    content_lines = []
    for line in lines[1:]:
        if line.strip():
            content_lines.append(line.strip())

    formatted_content = [first_line + "\n"]

    index = 0
    for line in content_lines:
        formatted_content.append(line)
        index += 1
        if index == length:
            formatted_content.append("")
            index = 0

    return "\n".join(formatted_content)

def non_uniform_length(lengths_str):
    try:
        lengths = []
        for length in lengths_str.split(','):
            if length.strip().isdigit():
                lengths.append(int(length.strip()))
        return lengths
    except ValueError:
        return []

def non_uniform_process_poem(content, lengths):
    lines = content.splitlines()
    first_line = lines[0].strip()
    content_lines = []
    for line in lines[1:]:
        if line.strip():
            content_lines.append(line.strip())

    formatted_content = [first_line + "\n"]

    index = 0
    for length in lengths:
        for _ in range(length):
            if index < len(content_lines):
                formatted_content.append(content_lines[index])
                index += 1
        formatted_content.append("")

    # Handle remaining lines if any
    while index < len(content_lines):
        formatted_content.append(content_lines[index])
        index += 1

    return "\n".join(formatted_content)

