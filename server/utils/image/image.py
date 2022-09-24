from typing import Any
from server.utils.utils import base64_to_image

import boto3


async def analyze_image(uuid: str) -> Any:
    rekognition = boto3.client("rekognition")
    faceLabels = []
    response = rekognition.detect_faces(
        Image={
            "Bytes": base64_to_image(uuid),
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
