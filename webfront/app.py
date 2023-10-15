from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Define a route to render the index.html page
@app.route('/')
def index():
    return render_template('index.html')

# Define a route for handling the audio file upload
@app.route('/upload', methods=['POST'])
def upload_audio():
    # Retrieve the uploaded audio file from the request
    audio_file = request.files['audio_data']

    # Check if an audio file was provided
    if audio_file:
        # Send the audio file to the /record endpoint in your backend
        response = requests.post('http://localhost:8080/record', files={'file': audio_file})

        # Check the response from the /record endpoint and return a response to the frontend
        if response.status_code == 200:
            # TODO: add make_response
            return jsonify({'message': 'Audio file uploaded successfully'})
        else:
            # TODO: add make_response
            return jsonify({'error': 'Failed to upload audio file'})

    return jsonify({'error': 'No audio file provided'})

if __name__ == '__main__':
    app.run(debug=True)
