from typing import Any
from app.utils.video.video import analyze_video
from app.utils.image.image import analyze_image

from fastapi import APIRouter

router = APIRouter()


@router.get("/video/{video_id}")
async def process_video(*, video_id: str) -> Any:
    res = await analyze_video(video_id)
    return res


@router.get("/image/{image_id}")
async def process_image(*, image_id: str) -> Any:
    res = await analyze_image(image_id)
    return res
