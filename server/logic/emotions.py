from typing import List, Dict
import json


class EmotionPoint(object):
    calm: float = None
    surprised: float = None
    fear: float = None
    sad: float = None
    angry: float = None
    happy: float = None
    confused: float = None
    disgusted: float = None

    def return_score(self) -> int:
        return 50

    def __init__(self, emotion_dict) -> None:
        for i in emotion_dict["Emotions"]:
            emotion_type = i["Type"].lower()
            confidence = i["Confidence"]
            if emotion_type == "calm":
                self.calm = confidence
            elif emotion_type == "surprised":
                self.surprised = confidence
            elif emotion_type == "fear":
                self.fear = confidence
            elif emotion_type == "sad":
                self.sad = confidence
            elif emotion_type == "angry":
                self.angry = confidence
            elif emotion_type == "happy":
                self.happy = confidence
            elif emotion_type == "confused":
                self.confused = confidence
            elif emotion_type == "disgusted":
                self.disgusted = confidence


class EmotionArray(object):
    array: List = []

    def construct_timestamp(self, json_timestamp) -> None:
        timestamp = EmotionPoint(json_timestamp)
        self.array.append(timestamp)

    def _construct_timestamps(self, emotion_arr: Dict) -> None:
        timestamp = EmotionPoint(emotion_arr)
        self.array.append(timestamp)

    def _construct_array(self, emotion_arr: Dict) -> None:
        self._construct_timestamps(emotion_arr["Emotions"])

    def __init__(self, emotion_arr: Dict) -> None:
        self.array = []
        self._construct_array(emotion_arr)