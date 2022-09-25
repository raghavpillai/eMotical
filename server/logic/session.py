import datetime
import time
from typing import List
from server.utils.image.image import make_video

from server.utils.utils import download_session_images
from server.utils.video.video import analyze_final_video
from .emotions import EmotionPoint, EmotionArray
from .chat_instance import ChatInstance


class Session(object):
    """
    Session object to create for each new emotion session
    """
    
    # Session files
    session_id: int = None

    # Times
    start_time: int = None
    end_time: int = None
    duration: int = None

    # Local session instances
    chat_instance: ChatInstance = None
    emotion_array: EmotionArray = None
    
    async def create_analysis(self) -> List:
        """
        Creates analysis based when session is ended
        @return list: [session_time:float, global_score:int, emotion_array:Dict]
        """

        videoUrl = await self.process_images()
        self.end_time = int(time.time())
        self.duration = self.end_time - self.start_time
        global_score: int = self.emotion_array.create_global_score()


        return [self.duration, global_score, self.emotion_array.to_arr(), videoUrl[-1]["VideoURL"]]
        

    async def process_images(self) -> int:
        """
        Processes an image using session ID
        @return string array from video API
        """
        await download_session_images(self.session_id)
        await make_video(self.session_id)
        res = await analyze_final_video(self.session_id)
        self.emotion_array = EmotionArray(res)
        return res

    def process_chat(self, msg: str, category: str, detail: str) -> str:
        """
        Processes chat into callback given message
        @param msg: str: message to process
        @return str: chat to fire back to client
        """
        return self.chat_instance.chat_callback(msg, category, detail)

    def __init__(self, id: str) -> None:
        """
        Data instantiation
        """
        self.session_id = id
        self.start_time = int(time.time())
        self.chat_instance = ChatInstance()
        print(f"Created new session {id}")