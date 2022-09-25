import base64
import datetime
from PIL import Image
from io import BytesIO
from moviepy.editor import *
import boto3
import os
import numpy as np


def ms_to_timestamp(ms) -> str:
    seconds = ms / 1000
    b = int((seconds % 3600) // 60)
    c = int((seconds % 3600) % 60)
    dt = datetime.time(0, b, c)
    return dt.strftime("%M:%S")


def base64_to_image(session_id: str, image_id: int, base64_string: str):
    print(f"Converting {image_id} Base64 to PNG...")
    base64_data = base64_string.split(",")[1]
    sbuf = BytesIO()
    sbuf.write(base64.b64decode(base64_data))
    image = Image.open(sbuf)
    image.save(
        f"server/sessions/images/{session_id}/{str(image_id)}.png",
        format="PNG",
    )
    return f"server/sessions/images/{session_id}/{str(image_id)}.png"


async def download_session_images(
    session_id,
    local="server/sessions",
    bucket="carmotion-videos",
):
    get_last_modified = lambda obj: int(obj["LastModified"].strftime("%s"))
    resource = boto3.resource("s3")
    paginator = resource.meta.client.get_paginator("list_objects")
    for result in paginator.paginate(
        Bucket=bucket, Delimiter="/", Prefix=f"{session_id}/"
    ):
        if result.get("CommonPrefixes") is not None:
            for subdir in result.get("CommonPrefixes"):
                download_session_images(
                    resource, subdir.get("Prefix"), local, bucket
                )
        objects = result.get("Contents", [])
        files = [obj["Key"] for obj in sorted(objects, key=get_last_modified)]
        print("Downloading session images... Please wait...")
        for file_name in files:
            dest_pathname = os.path.join(local, f"images/{file_name}")
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
            if not file_name.endswith("/"):
                resource.meta.client.download_file(
                    bucket, file_name, dest_pathname
                )
