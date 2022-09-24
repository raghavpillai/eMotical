from typing import Any
from app.utils.utils import base64_to_image

import boto3


async def analyze_image(base64_str: str) -> Any:
    rekognition = boto3.client("rekognition")
    faceLabels = []
    response = rekognition.detect_faces(
        Image={
            "Bytes": base64_to_image(base64_str),
        },
        Attributes=[
            "ALL",
        ],
    )
    for face in response["FaceDetails"]:
        faceLabels.append(
            {
                "BoundingBox": face["BoundingBox"],
                "Emotions": face["Emotions"],
                "Confidence": face["Confidence"],
            }
        )
    return faceLabels
