import face_recognition
import os
from PIL import Image, ImageDraw
import cv2
import re
import numpy as np
import json
import sys

video_capture = cv2.VideoCapture(0)

def detect_faces_in_image():
    dir = "./encodings"
    dir_list = os.listdir(dir)
    dir_list = list(map(lambda x: re.sub('\.jpg$', '', x), dir_list))
    number_files = len(dir_list)
    known_face_encodings = []
    tol_list = [0.085, 0.086, 0.087, 0.088, 0.089, 0.090, 0.091, 0.092, 0.093, 0.094, 0.095, 0.096, 0.097, 0.098, 0.099, 0.100, 0.101, 0.102, 0.105, 0.106, 0.107, 0.108, 0.109, 0.110, 0.111, 0.112, 0.113, 0.114, 0.115, 0.116, 0.117, 0.118, 0.119, 0.120, 0.121, 0.122, 0.123, 0.124, 0.125]


    for i in range(len(dir_list)):
        known_face = face_recognition.load_image_file(dir + '/' + dir_list[i] + ".jpg")
        known_face_encodings.append(face_recognition.face_encodings(known_face))

    while True:
        ret, frame = video_capture.read()
        frame = frame[:, :, ::-1]
        target_img = Image.fromarray(frame)
        draw = ImageDraw.Draw(target_img)

        unknown_face_encodings = face_recognition.face_encodings(frame)
        unknown_face_locations = face_recognition.face_locations(frame)
        for (top, right, bottom, left), unknown_face_encoding in zip(unknown_face_locations, unknown_face_encodings):
            for tol in tol_list :
                matches = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding, tolerance = tol)
                match_result = []
                for j in range(len(dir_list)):
                    match_result.append(matches[j].all())
                if np.where(match_result)[0] != []:
                    break
            name = "Unknown"
            if np.where(match_result)[0] != []:
                first_index = np.where(match_result)[0][0]
                name = dir_list[first_index]
            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
            text_width, text_height = draw.textsize(name)
            draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
            draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
        sys.stdout.buffer.write(np.asarray(target_img).tobytes())

detect_faces_in_image()
