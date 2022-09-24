from typing import Any
from server.utils.utils import base64_to_image

import boto3
import os
import io
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def get_images(session_id):
    path = f"sessions/{session_id}/images"
    files_content = []
    images = []
    for filename in filter(lambda p: p.endswith("txt"), os.listdir(path)):
        filepath = os.path.join(path, filename)
        with open(filepath, mode="r") as f:
            files_content += [f.read()]
    for file_content in files_content:
        images += [base64_to_image(file_content)]
    return images


def draw_bounding_box(image_bytes: bytes):
    rekognition = boto3.client("rekognition")
    image = Image.open(io.BytesIO(image_bytes))
    response = rekognition.detect_faces(
        Image={
            "Bytes": image_bytes,
        },
        Attributes=[
            "ALL",
        ],
    )
    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("sans-serif.ttf", 16)

    for faceDetail in response["FaceDetails"]:
        box = faceDetail["BoundingBox"]
        emotion = faceDetail["Emotions"][0]["Type"]
        left = imgWidth * box["Left"]
        top = imgHeight * box["Top"]
        width = imgWidth * box["Width"]
        height = imgHeight * box["Height"]
        points = (
            (left, top),
            (left + width, top),
            (left + width, top + height),
            (left, top + height),
            (left, top),
        )
        draw.line(points, fill="#00d400", width=2)
        draw.text((10, 10), emotion, (255, 255, 255), font=font)

    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    return buf.getvalue()


def get_new_image_buffer(session_id):
    images = get_images(session_id)
    return [draw_bounding_box(image) for image in images]


def make_video(session_id):
    frameSize = (1920, 1080)
    out = cv2.VideoWriter(
        "sessions/{session_id}/output_video.avi",
        cv2.VideoWriter_fourcc(*"DIVX"),
        30,
        frameSize,
        isColor=True,
    )
    for im_b in get_new_image_buffer(session_id):
        image_np = np.frombuffer(im_b, np.uint8)
        img_np = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        out.write(img_np)
    out.release()
