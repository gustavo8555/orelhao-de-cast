import os
from pathlib import Path
from flask import Flask, abort, current_app, make_response, render_template, request, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/record/*": {"origins": "*"}})

# TODO: study the file size limitations
# Sets file size limit to 1MB
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
# Sets the audio permited files
app.config['UPLOAD_EXTENSIONS'] = ['.wav']

RECORD_FOLDER_NAME = 'records' 
ACTUAL_APP_PATH = str(Path.cwd()) + "\\"


def setup():
    print("Initializing the file server")
    if not checks_record_folder_existence(RECORD_FOLDER_NAME):
        create_records_folder(RECORD_FOLDER_NAME)
    

def checks_record_folder_existence(folder_name):
    if os.path.exists and os.path.isdir(ACTUAL_APP_PATH + folder_name):
        return True
    else:
        return False

def create_records_folder(folder_name):
    print(f"Creating folder '{ACTUAL_APP_PATH + folder_name}'")
    folder = Path(ACTUAL_APP_PATH + folder_name)
    folder.mkdir(parents=True, exist_ok=True)

@app.route('/record', methods=['POST', 'OPTIONS'])
def upload_file():
    if request.method == 'OPTIONS':
        return make_response('Preflight OK', 200, {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "*"})
    else:
        uploaded_file = request.files['file']
        # uploaded_file.filename = uploaded_file.
        filename = secure_filename(uploaded_file.filename)
        print('filename: ' + filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            # TODO: add a file name logic
            uploaded_file.save(append_folder_name(uploaded_file.filename))
        return make_response('File uploaded successfully')

def append_folder_name(fullpath, server_path=RECORD_FOLDER_NAME):
    filename_path_chunks = fullpath.split('/')
    filename = filename_path_chunks[len(filename_path_chunks)-1]
    base_path = filename_path_chunks[0:len(filename_path_chunks)-1]
    base_path.append(server_path)
    base_path.append(filename)
    return '/'.join(base_path)


if __name__ == '__main__':
    setup()
    app.run(debug=True, host='localhost', port=8080)