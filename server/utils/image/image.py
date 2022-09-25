from typing import Any
from server.utils.utils import base64_to_image

import boto3
import os
import cv2
from PIL import Image, ImageDraw, ImageFont


async def get_images(session_id):
    print("Converting all images from Base64 to PNG...")
    path = f"server/sessions/images/{session_id}"
    files_content = []
    images = []
    for filename in filter(lambda p: p.endswith("txt"), os.listdir(path)):
        filepath = os.path.join(path, filename)
        with open(filepath, mode="r") as f:
            text = f.read()
            files_content.append(text)
    for i in range(0, len(files_content)):
        images.append(base64_to_image(session_id, i, files_content[i]))
    return images


async def draw_bounding_box(img_path: str):
    print(f"Drawing bounding box for {img_path}")
    rekognition = boto3.client("rekognition")
    cvImg = cv2.imread(img_path)
    _, im_buf_arr = cv2.imencode(".jpg", cvImg)
    byte_im = im_buf_arr.tobytes()

    response = rekognition.detect_faces(
        Image={
            "Bytes": byte_im,
        },
        Attributes=[
            "ALL",
        ],
    )
    image = Image.open(img_path)
    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(
        os.path.join("server", "fonts/Montserrat-Black.ttf"), 16
    )

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

    image.save(img_path, format="PNG")


async def draw_all_boxes(session_id):
    print("Drawing bounding boxes for all images...")
    images = await get_images(session_id)
    for image in images:
        await draw_bounding_box(image)


async def make_video(session_id):
    print("Making video from images...")
    await draw_all_boxes(session_id)
    image_folder = f"server/sessions/images/{session_id}"
    video_name = f"{session_id}.avi"
    images = [
        img
        for img in os.listdir(os.path.join(image_folder))
        if img.endswith("png")
    ]

    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, _ = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*"DIVX")
    video = cv2.VideoWriter(
        os.path.join(f"server/sessions/videos/{video_name}"),
        fourcc,
        1,
        (width, height),
    )

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
