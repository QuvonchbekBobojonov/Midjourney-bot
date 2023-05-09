import openai
import json
from deep_translator import GoogleTranslator
from config import OPENAI_TOKEN


def image_create_openai(text):
    text = GoogleTranslator(source='auto', target='en').translate(text)
    openai.api_key = OPENAI_TOKEN
    response = openai.Image.create(
        prompt=text,
        n=1,
        size="256x256",
    )
    return response["data"][0]["url"]
                                           
