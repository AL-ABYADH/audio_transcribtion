from flask import Flask, render_template, request, redirect
from transcribe_audio import transcribe_audio

app = Flask(__name__)
app.template_folder = ''  # set template folder to the root directory

@app.route('/')
def index():
    return render_template('index.html', message='')

@app.route('/', methods=['POST'])
def upload():
    audio_file = request.files['audio_file']
    output_dir = request.form['output_dir']
    if request.form['output_file']:
        output_file = request.form['output_file']
    else:
        output_file = 'Transcription.txt'
    audio_file.save(audio_file.filename)
    transcribe_audio(audio_file.filename, output_dir, output_file)
    return render_template('index.html', message='Successfully transcribed')

if __name__ == '__main__':
    app.run(debug=True)
