import time
from typing import List
from server.utils.image.image import make_video

from server.utils.utils import download_session_images
from server.utils.video.video import analyze_final_video
from .emotions import EmotionPoint, EmotionArray


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

    # Video URL to hold and store
    video_url: str = None

    # Local session instances
    emotion_array: EmotionArray = None

    async def create_analysis(self) -> List:
        """
        Creates analysis based when session is ended
        @return list: [session_time:float, global_score:int, emotion_array:Dict]
        """

        await self.process_images()
        self.end_time = time.time()
        self.duration = (self.end_time - self.start_time).total_seconds()
        global_score: int = self.emotion_array.create_global_score()
        return [self.duration, global_score, self.emotion_array]

    async def process_images(self, draw_boxes=True) -> int:
        """
        Processes an image using session ID
        @return string array from video API
        """
        await download_session_images(self.session_id)
        await make_video(self.session_id, draw_boxes)
        res = await analyze_final_video(self.session_id)
        # self.emotion_array = EmotionArray(res)
        return res

    def __init__(self, id: str) -> None:
        """
        Data instantiation
        """
        self.session_id = id
        self.start_time = time.time()
        print(f"Created new session {id}")
