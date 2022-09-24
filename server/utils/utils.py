import base64
import datetime
from PIL import Image
from io import BytesIO
import boto3
import os
import moviepy


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


def download_session_videos(session_id):
    s3_resource = boto3.resource("s3")
    my_bucket = s3_resource.Bucket("carmotion-videos")
    objects = my_bucket.objects.filter(Prefix=f"{session_id}/")
    for obj in objects:
        path, filename = os.path.split(obj.key)
        my_bucket.download_file(
            obj.key, f"sessions/${session_id}/videos/{filename}"
        )


def get_video_paths(session_id):
    video_paths = []
    for file in os.listdir(f"sessions/${session_id}"):
        if file.endswith(".mp4"):
            video_paths.append(f"sessions/${session_id}/videos/{file}")
    return video_paths


def concatenate(video_clip_paths, session_id):
    clips = [moviepy.VideoFileClip(c) for c in video_clip_paths]
    min_height = min([c.h for c in clips])
    min_width = min([c.w for c in clips])
    clips = [c.resize(newsize=(min_width, min_height)) for c in clips]
    final_clip = moviepy.concatenate.concatenate_videoclips(clips)
    final_clip.write_videofile(f"sessions/${session_id}/final_video.mp4")
    final_clip.close()


def upload_final_video(session_id):
    s3 = boto3.client("s3")
    s3.upload_file(
        f"sessions/${session_id}/final_video.mp4",
        "carmotion-videos",
        f"{session_id}/final_video.mp4",
    )
