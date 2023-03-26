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
    # Set the output format to mp4
    output_format = "mp4"
    # Export the audio in mp4 format
    audio.export('audio_mp4.' + output_format, format=output_format)
    
    with open(f"D:\\Projetos\\meet\\audio_mp4.{output_format}", "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file).text   
        
    messages = [
        {"role": "system", "content": "You will do a resume of the music"},
        {"role": "user", "content": transcript}
    ]

    cost = num_tokens_from_messages(messages) * COST_TOKEN

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    
    return completion.choices[0].message.content

if __name__ == '__main__':
    app.run()


    """   
    is_continue = input("Press 'S' to continue or 'N' to cancel: ").upper()

    if is_continue == 'S':
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )

        print("\n***************************MUSIC********************************\n")
        print(completion.choices[0].message.content)
        print("\n****************************************************************\n")
    else:
        exit(0)
    """