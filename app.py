from flask import Flask, render_template, request, redirect, send_file, url_for
import os
import logging

app = Flask(__name__)
app.secret_key = "flower123456"

# Use a writable directory
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['DOWNLOAD_FOLDER'] = '/tmp/downloads'

# Create upload and download folders if they don't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['DOWNLOAD_FOLDER']):
    os.makedirs(app.config['DOWNLOAD_FOLDER'])

# Set up logging
logging.basicConfig(level=logging.DEBUG)

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
        try:
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

        except Exception as e:
            logging.error(f"Error processing upload: {e}")
            formatted_poem = f"Error processing upload: {e}"

    return render_template("upload.html", formatted_poem=formatted_poem, download_path=download_path)

@app.route("/download/<filename>")
def download_file(filename):
    try:
        return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], filename), as_attachment=True)
    except Exception as e:
        logging.error(f"Error sending file: {e}")
        return "Error sending file."

def uniform_process_poem(content, length):
    lines = content.splitlines()
    first_line = lines[0].strip()
    content_lines = [line.strip() for line in lines[1:] if line.strip()]

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
        lengths = [int(length.strip()) for length in lengths_str.split(',') if length.strip().isdigit()]
        return lengths
    except ValueError:
        return []

def non_uniform_process_poem(content, lengths):
    lines = content.splitlines()
    first_line = lines[0].strip()
    content_lines = [line.strip() for line in lines[1:] if line.strip()]

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

