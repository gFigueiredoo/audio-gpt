import openai
import tiktoken
import logging
from flask import Flask, request, render_template
from pydub import AudioSegment

COST_TOKEN = 0.000002
openai.api_key = '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'

def num_tokens_from_messages(messages, model="gpt-3.5-turbo"):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":  
        num_tokens = 0
        for message in messages:
            num_tokens += 4  
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name": 
                    num_tokens += -1  
        num_tokens += 2  
        return num_tokens
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.""")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
    
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def upload():
    file = request.files['audio']
    audio = AudioSegment.from_file(file)
    output_format = "mp4"
    audio.export('audio_mp4.' + output_format, format=output_format)
    
    with open(f"D:\\Projetos\\meet\\audio_mp4.{output_format}", "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file).text   
        
    messages = [
        {"role": "system", "content": "You will do a formal resume and a minute of this meeting. You need especify what is resume and what is minute, always put a title in each text. You need to separate paragraphs correctly"},
        {"role": "user", "content": transcript}
    ]

    #cost = num_tokens_from_messages(messages) * COST_TOKEN

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2,
    )
    
    completion2 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=2,
    )

    summary = completion.choices[0].message.content + "\n\n\n" + completion2.choices[0].message.content
    
    print(summary)
    return render_template('resultado.html', summary=summary)

if __name__ == '__main__':
    app.run()
