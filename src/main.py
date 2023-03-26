import openai
import tiktoken
import logging

COST_TOKEN = 0.000002

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def num_tokens_from_messages(messages, model="gpt-3.5-turbo"):
    """Returns the number of tokens used by a list of messages."""
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

openai.api_key = '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'

with open("D:\\Projetos\\chatGPT\\audio.mp4", "rb") as audio_file:
    transcript = openai.Audio.transcribe("whisper-1", audio_file).text

messages = [
    {"role": "system", "content": "You will do a resume of the music"},
    {"role": "user", "content": transcript}
]

cost = num_tokens_from_messages(messages) * COST_TOKEN
logger.info(f"This transcript will cost ${cost} dollars, do you want to continue?")
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
