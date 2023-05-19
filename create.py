import requests
import json
from deep_translator import GoogleTranslator
import torch
from diffusers import StableDiffusionPipeline
from config import HOST, PORT, PASSWORD, USER, DATABESE
from db import DataBase

model_id = "CompVis/stable-diffusion-v1-4"
device = "cuda"

db = DataBase(host=HOST, port=PORT, database=DATABESE, user="postgres", password=PASSWORD)

def images_create(text, file):
    text = GoogleTranslator(source='uz', target='en').translate(text)

    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to(device)

    prompt = "a photo of an astronaut riding a horse on mars"
    image = pipe(prompt).images[0]  

    image.save(f"image{file}.png")

