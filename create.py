import openai
import requests
import json
from deep_translator import GoogleTranslator
from config import OPENAI_TOKEN, API_TOKEN


def image_create_openai(text):
    text = GoogleTranslator(source='auto', target='en').translate(text)
    openai.api_key = OPENAI_TOKEN
    response = openai.Image.create(
        prompt=text,
        n=1,
        size="256x256",
    )
    return response["data"][0]["url"]

def images_create(text):
    text = GoogleTranslator(source='auto', target='en').translate(text)

    r = requests.post('https://clipdrop-api.co/text-to-image/v1',
      files = {
          'prompt': (None, text, 'text/plain')
      },
      headers = { 'x-api-key': API_TOKEN}
    )
    return r.content


if __name__ == "__main__":
    print(images_create_relicate("quyon bilan bo'ri va "))                    
