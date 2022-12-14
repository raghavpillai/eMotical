from typing import List, Dict


class EmotionPoint(object):
    """
    EmotionPoint object that holds and individual emotion point
    """
    # Emotion confidence levels
    calm: float = 0
    surprised: float = 0
    fear: float = 0
    sad: float = 0
    angry: float = 0
    happy: float = 0
    confused: float = 0
    disgusted: float = 0

    def return_score(self) -> int:
        """
        Returns a score from -100 to 100 based on emotions
        -100 being most negative, 100 being most positive
        """
        print(self.calm)
        print(self.happy)
        positive = ( (self.calm*0.25) + self.happy * 1.75)/1.5
        negative = (self.fear + self.sad + self.angry + self.confused + self.disgusted)/5
        score = (positive - negative)
        return score

    def to_dict(self):
        return{
            "calm": self.calm,
            "surprised": self.surprised,
            "fear": self.fear,
            "sad": self.sad,
            "angry": self.angry,
            "happy": self.happy,
            "confused": self.confused,
            "disgusted": self.disgusted
        }

    def __init__(self, emotion_dict) -> None:
        """
        Initialization function
        @param emotion_dict: Dict: dictionary with key value pairs of emotion types (type) and confidence level (confidence)
        """
        for obj in emotion_dict:
            if obj == "Emotions":
                for emotion in emotion_dict[obj]:
                    emotion_type = emotion["Type"].lower()
                    confidence = emotion["Confidence"]
                    print(emotion_type)
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
    """
    Emotion array object, stores an array (list) of emotions
    """
    array: List = []

    def create_global_score(self) -> int:
        sum = 0
        for point in self.array:
            sum += point.return_score()
        return sum/len(self.array)

    def construct_timestamp(self, emotion_arr: Dict) -> None:
        """
        Constructs an emotion point from an emotion dictionary from API
        @param emotion_arr: Dict: Emotion array from emotion API
        """
        timestamp = EmotionPoint(emotion_arr)
        self.array.append(timestamp)

    def _construct_timestamps(self, emotion_arr: Dict) -> None:
        """
        Constructs an emotion point from an emotion dictionary from API
        @param emotion_arr: Dict: Emotion array from emotion API
        """
        timestamp = EmotionPoint(emotion_arr)
        self.array.append(timestamp)

    def _construct_array(self, emotion_arr: Dict) -> None:
        """
        Constructs an array from an inputted emotion array
        @param emotion_arr: Dict: Emotion array from emotion api
        """
        for emotion in emotion_arr:
            self._construct_timestamps(emotion)

    def to_arr(self):
        arr: List = []
        for point in self.array:
            arr.append(point.to_dict())
        return arr

    def __init__(self, emotion_arr: Dict) -> None:
        """
        Initialization function
        """
        self.array = []
        self._construct_array(emotion_arr)