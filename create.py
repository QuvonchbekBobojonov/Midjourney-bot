import requests
import json
from deep_translator import GoogleTranslator
from config import HOST, PORT, PASSWORD, USER, DATABESE
from db import DataBase

db = DataBase(host=HOST, port=PORT, database=DATABESE, user="postgres", password=PASSWORD)

def images_create(text):
    try:
      API_TOKEN = db.get_tokens()[0][1]
      print(API_TOKEN)
    except IndexError:
      return 'err'

    text = GoogleTranslator(source='uz', target='en').translate(text)

    r = requests.post('https://clipdrop-api.co/text-to-image/v1',
      files = {
          'prompt': (None, text, 'text/plain')
      },
      headers = { 'x-api-key': API_TOKEN}
    )
    print(r.status_code)
    if r.status_code == 200:
       return r.content
    else:
        db.delete_token(token=API_TOKEN)
        images_create(text)


if __name__ == "__main__":
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(images_create('bots')))
    with open('img.png', 'w') as f:
        f.write(img)