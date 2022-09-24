from typing import Any
from server.utils.utils import base64_to_image

import boto3


def analyze_image(uuid: str) -> Any:
    rekognition = boto3.client("rekognition")
    response = rekognition.detect_faces(
        Image={
            "Bytes": base64_to_image(uuid),
        },
        Attributes=[
            "ALL",
        ],
    )
    return {
        "Emotions": response["FaceDetails"][0]["Emotions"],
        "Confidence": response["FaceDetails"][0]["Confidence"],
    }
