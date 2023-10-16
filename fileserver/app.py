import os
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

@app.route('/record', methods=['POST', 'OPTIONS'])
def upload_file():
    # print('REQUEST >>>>>>>>>>>>>>>>>>>>>>>>>>>' + request)
    if request.method == 'OPTIONS':
        return make_response('Preflight OK', 200, {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "*"})
    else:
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            # TODO: add a file name logic
            uploaded_file.save(uploaded_file.filename)
        return make_response('File uploaded successfully')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8080)