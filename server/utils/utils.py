import base64
from concurrent.futures import ThreadPoolExecutor
import datetime
from functools import partial
from PIL import Image
from io import BytesIO
import boto3
import os


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


def download_one_file(
    bucket: str, client: boto3.client, output: str, s3_file: str
):
    client.download_file(
        Bucket=bucket, Key=s3_file, Filename=os.path.join(output, s3_file)
    )
    return True


session = boto3.Session()
resource = session.resource("s3")


async def download_session_images(
    session_id,
    local="server/sessions",
    bucket="carmotion-videos",
):
    get_last_modified = lambda obj: int(obj["LastModified"].strftime("%s"))
    paginator = resource.meta.client.get_paginator("list_objects")
    files_to_download = []
    for result in paginator.paginate(
        Bucket=bucket, Delimiter="/", Prefix=f"{session_id}/"
    ):
        objects = result.get("Contents", [])
        files = [obj["Key"] for obj in sorted(objects, key=get_last_modified)]
        print("Downloading session images... Please wait...")
        for file_name in files:
            dest_pathname = os.path.join(local, f"images/{file_name}")
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
            if not file_name.endswith("/"):
                files_to_download.append(file_name)

    with ThreadPoolExecutor(max_workers=32) as executor:
        func = partial(
            download_one_file,
            "carmotion-videos",
            resource.meta.client,
            f"server/sessions/images",
        )
        for result in executor.map(func, files_to_download):
            print(result)
