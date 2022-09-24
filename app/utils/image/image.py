from typing import Any

import boto3


async def analyze_image(name: str) -> Any:
    rekognition = boto3.client("rekognition")
    response = rekognition.detect_faces(
        Image={
            "S3Object": {
                "Bucket": "carmotion-video-images",
                "Name": name,
            }
        },
        Attributes=["EMOTIONS" | "ALL"],
    )
    return response
