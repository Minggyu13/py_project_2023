import cv2
import mediapipe as mp
import base64
import os, sys
from PIL import Image
from tkinter import *


class ImageApi:
    img = None
    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils
    drawing_spec = mp_drawing.DrawingSpec()
    face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.1)
    result = None

    def __init__(self, file_name):
        self.img = cv2.imread(file_name)
        self.results = self.face_detection.process(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))
        self.filename = file_name



    def show_image(self):
        box = list()
        result_img = self.img.copy()

        if self.results.detections:
            for detection in self.results.detections:
                ImageApi.mp_drawing.draw_detection(result_img, detection)

            for i, detection in enumerate(self.results.detections):
                box.append(detection.location_data.relative_bounding_box)

            xmin = max(int(box[0].xmin * self.img.shape[1]), 0)
            ymin = max(int(box[0].ymin * self.img.shape[0]), 0)
            width = int(box[0].width * self.img.shape[1])
            height = int(box[0].height * self.img.shape[0])

            face_img = self.img[ymin:ymin + height, xmin:xmin + width]

        else:
            print('얼굴이 검출되지 않았습니다!')


        cv2.imshow('Window Name', face_img)
        cv2.waitKey(0)  # 키 이벤트를 기다림, 0은 무한 대기
        cv2.destroyAllWindows()  # 열린 창을 모두 닫음

    def save_face(self):
        box = list()

        if self.results.detections:
            for i, detection in enumerate(self.results.detections):
                box.append(detection.location_data.relative_bounding_box)

            xmin = max(int(box[0].xmin * self.img.shape[1]), 0)
            ymin = max(int(box[0].ymin * self.img.shape[0]), 0)
            width = int(box[0].width * self.img.shape[1])
            height = int(box[0].height * self.img.shape[0])

            face_img = self.img[ymin:ymin + height, xmin:xmin + width]

            cv2.imwrite(f'{self.filename}_face.jpg', face_img)



    def face_img_to_json(self, face_fileName):
        with open(face_fileName, "rb") as image_file:
            image_binary = image_file.read()
            encoded_string = base64.b64encode(image_binary)

            image_dict = {
                "test_image.png": encoded_string.decode()
            }

            # image_json = json.dumps(image_dict)
            image_base64_string = list(image_dict.values())[0]

            return image_base64_string





