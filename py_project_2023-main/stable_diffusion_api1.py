import requests
import io
import base64
from PIL import Image
import image_api
from tkinter import filedialog
import time
import cv2
import sys
import json

url = "http://127.0.0.1:7860"

confirm = input('자신만의 프로필 만들기를 시작하시겠습니까? (Y/N) : ').upper()
filename = str()

if confirm == 'Y':
    print('프로필이 될 사진을 골라주세요!!')
    time.sleep(3)
    filename = filedialog.askopenfilename()

    c1 = image_api.ImageApi(filename)

    c1.save_face()
    dd = c1.face_img_to_json(fr'{filename}_face.jpg')

    payload = {
        "image": f"{dd}"
    }

    response_clip = requests.post(url=f'{url}/sdapi/v1/interrogate', json=payload)

    r = response_clip.text
    prompt_clip = json.loads(r)
    prompt_clip = list(prompt_clip.values())[0]
    print(prompt_clip)

    payload = {

        "prompt": f"{prompt_clip}",
        "negative_prompt": "EasyNegative",
        "init_images": [
            c1.face_img_to_json(fr'{filename}_face.jpg')
        ],
        "denoising_strength": 0.58,

        "steps": 30
    }

    response = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)

    r = response.json()

    image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
    image.save('output.png')

    print('이미지가 완성 되었습니다!!')


elif confirm == 'N':
    print('다음에 만나요~~~')
    sys.exit()


else:
    print('잘못된 입력 입니다.')


print('다음과 같은 기능들이 있습니다.')
while True:
    menu = input('''
                    1. 나의 얼굴 보기!!
                    2. 나만의 프로필 보기!

                 원하는 기능의 번호를 입력해주세요! : ''')

    if menu == '1':
        c1.show_image()
        br = input('다른 기능도 해보시겠습니까?(Y/N) : ').upper()
        if br == 'Y':
            pass
        elif br == 'N':
            print('다음에 다시 만나요!!')
            break

    elif menu == '2':
        output = cv2.imread('output.png')
        cv2.imshow('Window Name', output)
        cv2.waitKey(0)  # 키 이벤트를 기다림, 0은 무한 대기
        cv2.destroyAllWindows()  # 열린 창을 모두 닫음

        br = input('다른 기능도 해보시겠습니까?(Y/N) : ').upper()
        if br == 'Y':
            pass
        elif br == 'N':
            print('다음에 다시 만나요!!')
            break

        else:
            print('잘못된 입력 입니다.')

