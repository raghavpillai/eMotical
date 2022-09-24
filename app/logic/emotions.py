from typing import List, Dict
import json


class Timestamp(object):
    calm: float = None
    surprised: float = None
    fear: float = None
    sad: float = None
    angry: float = None
    happy: float = None
    confused: float = None
    disgusted: float = None

    def __init__(self, emotion_dict):
        for i in emotion_dict:
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

    def _construct_timestamps(self, json_obj):
        timestamp = Timestamp(json_obj)
        self.array.append(timestamp)

    def _construct_array(self):
        file = open("testing.json")
        for i in json.load(file):
            self._construct_timestamps(i["Emotions"])
            # print(i["Timestamp"])

    def __init__(self) -> None:
        self.array = []
        self._construct_array()


e = EmotionArray()
