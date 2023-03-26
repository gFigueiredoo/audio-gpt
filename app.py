from flask import Flask, request, render_template
from pydub import AudioSegment

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def upload():
    file = request.files['audio']
    audio = AudioSegment.from_file(file)
    # faça aqui as manipulações desejadas com o arquivo de áudio
    # por exemplo: 
    audio = audio.reverse()
    audio.export('output.mp3', format='mp3')
    return 'Arquivo de áudio carregado com sucesso!'

if __name__ == '__main__':
    app.run()