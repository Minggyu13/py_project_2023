import image_api
from tkinter import filedialog
import time
import cv2
import requests
import json

url = "http://127.0.0.1:7860"

c1 = image_api.ImageApi('download.png')

c1.save_face()
payload = {
        "image": f"{c1.face_img_to_json(fr'download.png_face.jpg')}"
            }

response = requests.post(url=f'{url}/sdapi/v1/interrogate', json=payload)

r = response.text
prompt = json.loads(r)

prompt = list(prompt.values())[0]
print(prompt)