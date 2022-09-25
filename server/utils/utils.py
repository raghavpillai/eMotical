import base64
import concurrent
from concurrent.futures import ThreadPoolExecutor
import datetime
from functools import partial
from PIL import Image
from io import BytesIO
from moviepy.editor import *
import boto3
import os
import moviepy

blank_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAoAAAAHgCAYAAAA10dzkAAAAAXNSR0IArs4c6QAAGJxJREFUeF7t1sENADAMAjG6/9Ct1DXO2QCTB2fbnSNAgAABAgQIEMgIHAMw07WgBAgQIECAAIEvYAB6BAIECBAgQIBATMAAjBUuLgECBAgQIEDAAPQDBAgQIECAAIGYgAEYK1xcAgQIECBAgIAB6AcIECBAgAABAjEBAzBWuLgECBAgQIAAAQPQDxAgQIAAAQIEYgIGYKxwcQkQIECAAAECBqAfIECAAAECBAjEBAzAWOHiEiBAgAABAgQMQD9AgAABAgQIEIgJGICxwsUlQIAAAQIECBiAfoAAAQIECBAgEBMwAGOFi0uAAAECBAgQMAD9AAECBAgQIEAgJmAAxgoXlwABAgQIECBgAPoBAgQIECBAgEBMwACMFS4uAQIECBAgQMAA9AMECBAgQIAAgZiAARgrXFwCBAgQIECAgAHoBwgQIECAAAECMQEDMFa4uAQIECBAgAABA9APECBAgAABAgRiAgZgrHBxCRAgQIAAAQIGoB8gQIAAAQIECMQEDMBY4eISIECAAAECBAxAP0CAAAECBAgQiAkYgLHCxSVAgAABAgQIGIB+gAABAgQIECAQEzAAY4WLS4AAAQIECBAwAP0AAQIECBAgQCAmYADGCheXAAECBAgQIGAA+gECBAgQIECAQEzAAIwVLi4BAgQIECBAwAD0AwQIECBAgACBmIABGCtcXAIECBAgQICAAegHCBAgQIAAAQIxAQMwVri4BAgQIECAAAED0A8QIECAAAECBGICBmCscHEJECBAgAABAgagHyBAgAABAgQIxAQMwFjh4hIgQIAAAQIEDEA/QIAAAQIECBCICRiAscLFJUCAAAECBAgYgH6AAAECBAgQIBATMABjhYtLgAABAgQIEDAA/QABAgQIECBAICZgAMYKF5cAAQIECBAgYAD6AQIECBAgQIBATMAAjBUuLgECBAgQIEDAAPQDBAgQIECAAIGYgAEYK1xcAgQIECBAgIAB6AcIECBAgAABAjEBAzBWuLgECBAgQIAAAQPQDxAgQIAAAQIEYgIGYKxwcQkQIECAAAECBqAfIECAAAECBAjEBAzAWOHiEiBAgAABAgQMQD9AgAABAgQIEIgJGICxwsUlQIAAAQIECBiAfoAAAQIECBAgEBMwAGOFi0uAAAECBAgQMAD9AAECBAgQIEAgJmAAxgoXlwABAgQIECBgAPoBAgQIECBAgEBMwACMFS4uAQIECBAgQMAA9AMECBAgQIAAgZiAARgrXFwCBAgQIECAgAHoBwgQIECAAAECMQEDMFa4uAQIECBAgAABA9APECBAgAABAgRiAgZgrHBxCRAgQIAAAQIGoB8gQIAAAQIECMQEDMBY4eISIECAAAECBAxAP0CAAAECBAgQiAkYgLHCxSVAgAABAgQIGIB+gAABAgQIECAQEzAAY4WLS4AAAQIECBAwAP0AAQIECBAgQCAmYADGCheXAAECBAgQIGAA+gECBAgQIECAQEzAAIwVLi4BAgQIECBAwAD0AwQIECBAgACBmIABGCtcXAIECBAgQICAAegHCBAgQIAAAQIxAQMwVri4BAgQIECAAAED0A8QIECAAAECBGICBmCscHEJECBAgAABAgagHyBAgAABAgQIxAQMwFjh4hIgQIAAAQIEDEA/QIAAAQIECBCICRiAscLFJUCAAAECBAgYgH6AAAECBAgQIBATMABjhYtLgAABAgQIEDAA/QABAgQIECBAICZgAMYKF5cAAQIECBAgYAD6AQIECBAgQIBATMAAjBUuLgECBAgQIEDAAPQDBAgQIECAAIGYgAEYK1xcAgQIECBAgIAB6AcIECBAgAABAjEBAzBWuLgECBAgQIAAAQPQDxAgQIAAAQIEYgIGYKxwcQkQIECAAAECBqAfIECAAAECBAjEBAzAWOHiEiBAgAABAgQMQD9AgAABAgQIEIgJGICxwsUlQIAAAQIECBiAfoAAAQIECBAgEBMwAGOFi0uAAAECBAgQMAD9AAECBAgQIEAgJmAAxgoXlwABAgQIECBgAPoBAgQIECBAgEBMwACMFS4uAQIECBAgQMAA9AMECBAgQIAAgZiAARgrXFwCBAgQIECAgAHoBwgQIECAAAECMQEDMFa4uAQIECBAgAABA9APECBAgAABAgRiAgZgrHBxCRAgQIAAAQIGoB8gQIAAAQIECMQEDMBY4eISIECAAAECBAxAP0CAAAECBAgQiAkYgLHCxSVAgAABAgQIGIB+gAABAgQIECAQEzAAY4WLS4AAAQIECBAwAP0AAQIECBAgQCAmYADGCheXAAECBAgQIGAA+gECBAgQIECAQEzAAIwVLi4BAgQIECBAwAD0AwQIECBAgACBmIABGCtcXAIECBAgQICAAegHCBAgQIAAAQIxAQMwVri4BAgQIECAAAED0A8QIECAAAECBGICBmCscHEJECBAgAABAgagHyBAgAABAgQIxAQMwFjh4hIgQIAAAQIEDEA/QIAAAQIECBCICRiAscLFJUCAAAECBAgYgH6AAAECBAgQIBATMABjhYtLgAABAgQIEDAA/QABAgQIECBAICZgAMYKF5cAAQIECBAgYAD6AQIECBAgQIBATMAAjBUuLgECBAgQIEDAAPQDBAgQIECAAIGYgAEYK1xcAgQIECBAgIAB6AcIECBAgAABAjEBAzBWuLgECBAgQIAAAQPQDxAgQIAAAQIEYgIGYKxwcQkQIECAAAECBqAfIECAAAECBAjEBAzAWOHiEiBAgAABAgQMQD9AgAABAgQIEIgJGICxwsUlQIAAAQIECBiAfoAAAQIECBAgEBMwAGOFi0uAAAECBAgQMAD9AAECBAgQIEAgJmAAxgoXlwABAgQIECBgAPoBAgQIECBAgEBMwACMFS4uAQIECBAgQMAA9AMECBAgQIAAgZiAARgrXFwCBAgQIECAgAHoBwgQIECAAAECMQEDMFa4uAQIECBAgAABA9APECBAgAABAgRiAgZgrHBxCRAgQIAAAQIGoB8gQIAAAQIECMQEDMBY4eISIECAAAECBAxAP0CAAAECBAgQiAkYgLHCxSVAgAABAgQIGIB+gAABAgQIECAQEzAAY4WLS4AAAQIECBAwAP0AAQIECBAgQCAmYADGCheXAAECBAgQIGAA+gECBAgQIECAQEzAAIwVLi4BAgQIECBAwAD0AwQIECBAgACBmIABGCtcXAIECBAgQICAAegHCBAgQIAAAQIxAQMwVri4BAgQIECAAAED0A8QIECAAAECBGICBmCscHEJECBAgAABAgagHyBAgAABAgQIxAQMwFjh4hIgQIAAAQIEDEA/QIAAAQIECBCICRiAscLFJUCAAAECBAgYgH6AAAECBAgQIBATMABjhYtLgAABAgQIEDAA/QABAgQIECBAICZgAMYKF5cAAQIECBAgYAD6AQIECBAgQIBATMAAjBUuLgECBAgQIEDAAPQDBAgQIECAAIGYgAEYK1xcAgQIECBAgIAB6AcIECBAgAABAjEBAzBWuLgECBAgQIAAAQPQDxAgQIAAAQIEYgIGYKxwcQkQIECAAAECBqAfIECAAAECBAjEBAzAWOHiEiBAgAABAgQMQD9AgAABAgQIEIgJGICxwsUlQIAAAQIECBiAfoAAAQIECBAgEBMwAGOFi0uAAAECBAgQMAD9AAECBAgQIEAgJmAAxgoXlwABAgQIECBgAPoBAgQIECBAgEBMwACMFS4uAQIECBAgQMAA9AMECBAgQIAAgZiAARgrXFwCBAgQIECAgAHoBwgQIECAAAECMQEDMFa4uAQIECBAgAABA9APECBAgAABAgRiAgZgrHBxCRAgQIAAAQIGoB8gQIAAAQIECMQEDMBY4eISIECAAAECBAxAP0CAAAECBAgQiAkYgLHCxSVAgAABAgQIGIB+gAABAgQIECAQEzAAY4WLS4AAAQIECBAwAP0AAQIECBAgQCAmYADGCheXAAECBAgQIGAA+gECBAgQIECAQEzAAIwVLi4BAgQIECBAwAD0AwQIECBAgACBmIABGCtcXAIECBAgQICAAegHCBAgQIAAAQIxAQMwVri4BAgQIECAAAED0A8QIECAAAECBGICBmCscHEJECBAgAABAgagHyBAgAABAgQIxAQMwFjh4hIgQIAAAQIEDEA/QIAAAQIECBCICRiAscLFJUCAAAECBAgYgH6AAAECBAgQIBATMABjhYtLgAABAgQIEDAA/QABAgQIECBAICZgAMYKF5cAAQIECBAgYAD6AQIECBAgQIBATMAAjBUuLgECBAgQIEDAAPQDBAgQIECAAIGYgAEYK1xcAgQIECBAgIAB6AcIECBAgAABAjEBAzBWuLgECBAgQIAAAQPQDxAgQIAAAQIEYgIGYKxwcQkQIECAAAECBqAfIECAAAECBAjEBAzAWOHiEiBAgAABAgQMQD9AgAABAgQIEIgJGICxwsUlQIAAAQIECBiAfoAAAQIECBAgEBMwAGOFi0uAAAECBAgQMAD9AAECBAgQIEAgJmAAxgoXlwABAgQIECBgAPoBAgQIECBAgEBMwACMFS4uAQIECBAgQMAA9AMECBAgQIAAgZiAARgrXFwCBAgQIECAgAHoBwgQIECAAAECMQEDMFa4uAQIECBAgAABA9APECBAgAABAgRiAgZgrHBxCRAgQIAAAQIGoB8gQIAAAQIECMQEDMBY4eISIECAAAECBAxAP0CAAAECBAgQiAkYgLHCxSVAgAABAgQIGIB+gAABAgQIECAQEzAAY4WLS4AAAQIECBAwAP0AAQIECBAgQCAmYADGCheXAAECBAgQIGAA+gECBAgQIECAQEzAAIwVLi4BAgQIECBAwAD0AwQIECBAgACBmIABGCtcXAIECBAgQICAAegHCBAgQIAAAQIxAQMwVri4BAgQIECAAAED0A8QIECAAAECBGICBmCscHEJECBAgAABAgagHyBAgAABAgQIxAQMwFjh4hIgQIAAAQIEDEA/QIAAAQIECBCICRiAscLFJUCAAAECBAgYgH6AAAECBAgQIBATMABjhYtLgAABAgQIEDAA/QABAgQIECBAICZgAMYKF5cAAQIECBAgYAD6AQIECBAgQIBATMAAjBUuLgECBAgQIEDAAPQDBAgQIECAAIGYgAEYK1xcAgQIECBAgIAB6AcIECBAgAABAjEBAzBWuLgECBAgQIAAAQPQDxAgQIAAAQIEYgIGYKxwcQkQIECAAAECBqAfIECAAAECBAjEBAzAWOHiEiBAgAABAgQMQD9AgAABAgQIEIgJGICxwsUlQIAAAQIECBiAfoAAAQIECBAgEBMwAGOFi0uAAAECBAgQMAD9AAECBAgQIEAgJmAAxgoXlwABAgQIECBgAPoBAgQIECBAgEBMwACMFS4uAQIECBAgQMAA9AMECBAgQIAAgZiAARgrXFwCBAgQIECAgAHoBwgQIECAAAECMQEDMFa4uAQIECBAgAABA9APECBAgAABAgRiAgZgrHBxCRAgQIAAAQIGoB8gQIAAAQIECMQEDMBY4eISIECAAAECBAxAP0CAAAECBAgQiAkYgLHCxSVAgAABAgQIGIB+gAABAgQIECAQEzAAY4WLS4AAAQIECBAwAP0AAQIECBAgQCAmYADGCheXAAECBAgQIGAA+gECBAgQIECAQEzAAIwVLi4BAgQIECBAwAD0AwQIECBAgACBmIABGCtcXAIECBAgQICAAegHCBAgQIAAAQIxAQMwVri4BAgQIECAAAED0A8QIECAAAECBGICBmCscHEJECBAgAABAgagHyBAgAABAgQIxAQMwFjh4hIgQIAAAQIEDEA/QIAAAQIECBCICRiAscLFJUCAAAECBAgYgH6AAAECBAgQIBATMABjhYtLgAABAgQIEDAA/QABAgQIECBAICZgAMYKF5cAAQIECBAgYAD6AQIECBAgQIBATMAAjBUuLgECBAgQIEDAAPQDBAgQIECAAIGYgAEYK1xcAgQIECBAgIAB6AcIECBAgAABAjEBAzBWuLgECBAgQIAAAQPQDxAgQIAAAQIEYgIGYKxwcQkQIECAAAECBqAfIECAAAECBAjEBAzAWOHiEiBAgAABAgQMQD9AgAABAgQIEIgJGICxwsUlQIAAAQIECBiAfoAAAQIECBAgEBMwAGOFi0uAAAECBAgQMAD9AAECBAgQIEAgJmAAxgoXlwABAgQIECBgAPoBAgQIECBAgEBMwACMFS4uAQIECBAgQMAA9AMECBAgQIAAgZiAARgrXFwCBAgQIECAgAHoBwgQIECAAAECMQEDMFa4uAQIECBAgAABA9APECBAgAABAgRiAgZgrHBxCRAgQIAAAQIGoB8gQIAAAQIECMQEDMBY4eISIECAAAECBAxAP0CAAAECBAgQiAkYgLHCxSVAgAABAgQIGIB+gAABAgQIECAQEzAAY4WLS4AAAQIECBAwAP0AAQIECBAgQCAmYADGCheXAAECBAgQIGAA+gECBAgQIECAQEzAAIwVLi4BAgQIECBAwAD0AwQIECBAgACBmIABGCtcXAIECBAgQICAAegHCBAgQIAAAQIxAQMwVri4BAgQIECAAAED0A8QIECAAAECBGICBmCscHEJECBAgAABAgagHyBAgAABAgQIxAQMwFjh4hIgQIAAAQIEDEA/QIAAAQIECBCICRiAscLFJUCAAAECBAgYgH6AAAECBAgQIBATMABjhYtLgAABAgQIEDAA/QABAgQIECBAICZgAMYKF5cAAQIECBAgYAD6AQIECBAgQIBATMAAjBUuLgECBAgQIEDAAPQDBAgQIECAAIGYgAEYK1xcAgQIECBAgIAB6AcIECBAgAABAjEBAzBWuLgECBAgQIAAAQPQDxAgQIAAAQIEYgIGYKxwcQkQIECAAAECBqAfIECAAAECBAjEBAzAWOHiEiBAgAABAgQMQD9AgAABAgQIEIgJGICxwsUlQIAAAQIECBiAfoAAAQIECBAgEBMwAGOFi0uAAAECBAgQMAD9AAECBAgQIEAgJmAAxgoXlwABAgQIECBgAPoBAgQIECBAgEBMwACMFS4uAQIECBAgQMAA9AMECBAgQIAAgZiAARgrXFwCBAgQIECAgAHoBwgQIECAAAECMQEDMFa4uAQIECBAgAABA9APECBAgAABAgRiAgZgrHBxCRAgQIAAAQIGoB8gQIAAAQIECMQEDMBY4eISIECAAAECBAxAP0CAAAECBAgQiAkYgLHCxSVAgAABAgQIGIB+gAABAgQIECAQEzAAY4WLS4AAAQIECBAwAP0AAQIECBAgQCAmYADGCheXAAECBAgQIGAA+gECBAgQIECAQEzAAIwVLi4BAgQIECBAwAD0AwQIECBAgACBmIABGCtcXAIECBAgQICAAegHCBAgQIAAAQIxAQMwVri4BAgQIECAAAED0A8QIECAAAECBGICBmCscHEJECBAgAABAgagHyBAgAABAgQIxAQMwFjh4hIgQIAAAQIEDEA/QIAAAQIECBCICRiAscLFJUCAAAECBAgYgH6AAAECBAgQIBATMABjhYtLgAABAgQIEDAA/QABAgQIECBAICZgAMYKF5cAAQIECBAgYAD6AQIECBAgQIBATMAAjBUuLgECBAgQIEDAAPQDBAgQIECAAIGYgAEYK1xcAgQIECBAgIAB6AcIECBAgAABAjEBAzBWuLgECBAgQIAAAQPQDxAgQIAAAQIEYgIGYKxwcQkQIECAAAECBqAfIECAAAECBAjEBAzAWOHiEiBAgAABAgQMQD9AgAABAgQIEIgJGICxwsUlQIAAAQIECBiAfoAAAQIECBAgEBMwAGOFi0uAAAECBAgQMAD9AAECBAgQIEAgJmAAxgoXlwABAgQIECBgAPoBAgQIECBAgEBMwACMFS4uAQIECBAgQMAA9AMECBAgQIAAgZiAARgrXFwCBAgQIECAgAHoBwgQIECAAAECMQEDMFa4uAQIECBAgAABA9APECBAgAABAgRiAgZgrHBxCRAgQIAAAQIGoB8gQIAAAQIECMQEDMBY4eISIECAAAECBAxAP0CAAAECBAgQiAkYgLHCxSVAgAABAgQIGIB+gAABAgQIECAQEzAAY4WLS4AAAQIECBAwAP0AAQIECBAgQCAmYADGCheXAAECBAgQIGAA+gECBAgQIECAQEzAAIwVLi4BAgQIECBAwAD0AwQIECBAgACBmIABGCtcXAIECBAgQICAAegHCBAgQIAAAQIxAQMwVri4BAgQIECAAAED0A8QIECAAAECBGICBmCscHEJECBAgAABAgagHyBAgAABAgQIxAQMwFjh4hIgQIAAAQIEDEA/QIAAAQIECBCICRiAscLFJUCAAAECBAgYgH6AAAECBAgQIBATMABjhYtLgAABAgQIEHiciuAQraEnKwAAAABJRU5ErkJggg=="


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


AWS_BUCKET = "carmotion-videos"
OUTPUT_DIR = "/sessions"

session = boto3.Session()
resource = session.resource("s3")


def download_one_file(
    client: boto3.client, dest_pathname: str, file_name: str
):
    client.download_file(
        Bucket=AWS_BUCKET, Key=file_name, Filename=dest_pathname
    )


func = partial(download_one_file, resource.meta.client)


async def download_session_images(session_id):
    get_last_modified = lambda obj: int(obj["LastModified"].strftime("%s"))
    resource = boto3.resource("s3")
    paginator = resource.meta.client.get_paginator("list_objects")
    for result in paginator.paginate(
        Bucket=AWS_BUCKET, Delimiter="/", Prefix=f"{session_id}/"
    ):
        objects = result.get("Contents", [])
        files = [obj["Key"] for obj in sorted(objects, key=get_last_modified)]
        files_to_download = []
        for file_name in files:
            dest_pathname = os.path.join(OUTPUT_DIR, f"/images/{file_name}")
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
            if not file_name.endswith("/"):
                files_to_download.append(file_name)
        print("Downloading session images... Please wait...")
        with ThreadPoolExecutor(max_workers=32) as executor:
            futures = {
                executor.submit(
                    func, dest_pathname, file_name
                ): file_to_download
                for file_to_download in files_to_download
            }
            for file_name in files_to_download:
                futures.append(executor.submit(func, dest_pathname, file_name))
            for future in concurrent.futures.as_completed(futures):
                try:
                    print(f"File download result: {future.result()}")
                except Exception as exc:
                    print("Failed to download file: %s" % exc)
            return True
