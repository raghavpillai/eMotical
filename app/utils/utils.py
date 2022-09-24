import base64
import datetime
from PIL import Image
from io import BytesIO


def ms_to_timestamp(ms) -> str:
    seconds = ms / 1000
    b = int((seconds % 3600) // 60)
    c = int((seconds % 3600) % 60)
    dt = datetime.time(0, b, c)
    return dt.strftime("%M:%S")


def base64_to_image(base64_string: str):
    sbuf = BytesIO()
    sbuf.write(base64.b64decode(base64_string))
    image = Image.open(sbuf)
    image.save(sbuf, format="PNG")
    sbuf.seek(0)
    return sbuf.read()
