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
            match emotion_type:
                case "calm": self.calm = confidence
                case "surprised": self.surprised = confidence
                case "fear": self.fear = confidence
                case "sad": self.sad = confidence
                case "angry": self.angry = confidence
                case "happy": self.happy = confidence
                case "confused": self.confused = confidence
                case "disgusted": self.disgusted = confidence
        

class EmotionArray(object):
    array: List = []

    def _construct_timestamps(self,json_obj):
        timestamp = Timestamp(json_obj)
        self.array.append(timestamp)

    def _construct_array(self):
        file = open("testing.json")
        for i in json.load(file):
            self._construct_timestamps(i["Emotions"])
            #print(i["Timestamp"])

    def __init__(self) -> None:
        self.array = []
        self._construct_array()


e = EmotionArray()