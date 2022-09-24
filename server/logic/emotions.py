from typing import List, Dict


class EmotionPoint(object):
    """
    EmotionPoint object that holds and individual emotion point
    """
    # Emotion confidence levels
    calm: float = None
    surprised: float = None
    fear: float = None
    sad: float = None
    angry: float = None
    happy: float = None
    confused: float = None
    disgusted: float = None

    def return_score(self) -> int:
        """
        Returns a score from -100 to 100 based on emotions
        -100 being most negative, 100 being most positive
        """
        positive = (self.calm + self.happy)/2
        negative = (self.fear + self.sad + self.angry + self.confused + self.disgusted)/5
        score = (positive - negative)
        return score

    def __init__(self, emotion_dict: Dict) -> None:
        """
        Initialization function
        @param emotion_dict: Dict: dictionary with key value pairs of emotion types (type) and confidence level (confidence)
        """
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
    """
    Emotion array object, stores an array (list) of emotions
    """
    array: List = []

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
        self._construct_timestamps(emotion_arr["Emotions"])

    def __init__(self, emotion_arr: Dict) -> None:
        """
        Initialization function
        """
        self.array = []
        self._construct_array(emotion_arr)