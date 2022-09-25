import time
from typing import IO
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

    # Video URL to hold and store
    video_url: str = None

    def __init__(self, id):
        """
        Data instantiation
        """
        self.session_id = id
        self.start_time = time.time()
        print(f"Created new session {id}")

    # def create_analysis(self):
    #     # Session time
    #     #
    #     # Total score (-100 to 100)
    #     # Positive and negative score breakdowns with confidence levels
    #     # Individual score breakdowns
    #     # Graph with data points
    #     pass

    async def process_images(self, image_id: str) -> int:
        """
        Processes an image
        @param image_id: str: Image ID to analyze, base64
        @return string array from video API
        """
        await download_session_images(self.session_id)
        await make_video(image_id)
        res = await analyze_final_video(self.session_id)
        # convert to emotion array please <3
        # point = EmotionPoint(res)
        # score = point.return_score()
        return res

    # def process_video(self) -> str:
    #     """
    #     Processes video from session id
    #     @return string array from video API
    #     """
    #     download_session_videos(self.session_id)

    #     paths = get_video_paths(self.session_id)
    #     concatenate(paths, self.session_id)

    #     res = analyze_final_video(self.session_id)
    #     return res

    def end_session(self):
        """
        Ends the session and time
        """
        self.end_time = time.time()
