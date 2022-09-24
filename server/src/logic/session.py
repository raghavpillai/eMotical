import time
from typing import IO

from emotion_array import EmotionArray

class Session(object):
    session_id: int = None
    session_data_file: IO = None

    start_time: int = None
    end_time: int = None

    video_url: str = None
    
    live_emotion_array: EmotionArray = None
    final_emotion_array: EmotionArray = None
    
    def analyze_video(self):
        # Get emotions from array

    def end_session(self):
        end_time = time.time()

    def __init__(self, json_file):        
        # Data instantiation
        self.session_id = int(time.time()) 
        self.session_data_file = open(self.session_id+".json", "a")

        self.start_time = time.time()