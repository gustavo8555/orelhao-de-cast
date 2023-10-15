import os
from flask import Flask, abort, current_app, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
# TODO: study the file size limitations
# Sets file size limit to 1MB
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
# Sets the audio permited files
app.config['UPLOAD_EXTENSIONS'] = ['.wav']

@app.route('/')
def index():
    return render_template('audio_upload.html')

@app.route('/record', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        # TODO: add a file name logic
        uploaded_file.save(uploaded_file.filename)
    return redirect(url_for('index'))