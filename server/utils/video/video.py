from typing import Any
from server.utils.utils import ms_to_timestamp

import boto3
import cv2


async def analyze_final_video(session_id: str) -> Any:
    rekognition = boto3.client("rekognition")
    faceLabels = []
    cap = cv2.VideoCapture(f"sessions/{session_id}/output_video.avi")
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    save_interval = 1

    frame_count = 0
    print("Processing video...")
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame_count += 1

            if frame_count % (fps * save_interval) == 0:
                hasFrame, imageBytes = cv2.imencode(".jpg", frame)

                if hasFrame:
                    response = rekognition.detect_faces(
                        Image={
                            "Bytes": imageBytes.tobytes(),
                        },
                        Attributes=[
                            "ALL",
                        ],
                    )

                    for face in response["FaceDetails"]:
                        faceLabels.append(
                            {
                                "Emotions": face["Emotions"],
                                "Confidence": face["Confidence"],
                                "Timestamp": ms_to_timestamp(
                                    cap.get(cv2.CAP_PROP_POS_MSEC)
                                ),
                            }
                        )

                    frame_count = 0
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

    return faceLabels
