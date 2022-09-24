import operator
import itertools
from random import randint, sample
from typing import Dict

class Recommendations:
    """
    Recommendation files
    """

    # Video database
    videos_cars: Dict = {
        "https://www.youtube.com/watch?v=fPYho_m142c": ["bmw", "european", "german", "munich", "luxury", "performance", "sedan", "coupe", "suv"], 
        "https://www.youtube.com/watch?v=qmqm5FrRN8A": ["bmw", "european", "german", "munich", "luxury", "performance", "sedan", "coupe", "suv"], 
        "https://www.youtube.com/watch?v=i3XNDsADQM4": ["bmw", "european", "german", "munich", "luxury", "performance", "sedan", "coupe", "suv"], 
        "https://www.youtube.com/watch?v=nzwsdBdFxmI": ["bmw", "european", "german", "munich", "luxury", "performance", "sedan", "coupe", "suv"], 
        "https://www.youtube.com/watch?v=FkVItMcrSh4": ["bmw", "european", "german", "munich", "luxury", "performance", "sedan", "coupe", "suv"], 
        "https://www.youtube.com/watch?v=eMpszInH0xw": ["bmw", "european", "german", "munich", "luxury", "performance", "sedan", "coupe", "suv"], 
        "https://www.youtube.com/watch?v=XO93x4PAI1U": ["mercedes", "european", "german", "affalterbach", "luxury", "performance", "sedan", "coupe", "suv"], 
        "https://www.youtube.com/watch?v=_wMTw_MeELY": ["mercedes", "european", "german", "affalterbach", "luxury", "performance", "sedan", "coupe", "suv"], 
        "https://www.youtube.com/watch?v=gCMQS3UDabo": ["mercedes", "european", "german", "affalterbach", "luxury", "performance", "sedan", "coupe", "suv"], 
        "https://www.youtube.com/watch?v=YqvOHgBhnBU": ["mercedes", "european", "german", "affalterbach", "luxury", "performance", "sedan", "coupe", "suv"], 
        "https://www.youtube.com/watch?v=xTm6b6mQTIQ": ["mercedes", "european", "german", "affalterbach", "luxury", "performance", "sedan", "coupe", "suv"], 
        "https://www.youtube.com/watch?v=o86qjnOmyXs": ["mercedes", "european", "german", "affalterbach", "luxury", "performance", "sedan", "coupe", "suv"], 
        "https://www.youtube.com/watch?v=9MRmNDDp5i8": ["toyota", "asian", "japanese", "economy", "performance", "sedan", "coupe", "suv", "hatchback"],
        "https://www.youtube.com/watch?v=vftaaO-iMWE": ["toyota", "asian", "japanese", "economy", "performance", "sedan", "coupe", "suv", "hatchback"],
        "https://www.youtube.com/watch?v=Gvn7jwqj8Zo": ["toyota", "asian", "japanese", "economy", "performance", "sedan", "coupe", "suv", "hatchback"],
        "https://www.youtube.com/watch?v=3rXTHobmQQo": ["toyota", "asian", "japanese", "economy", "performance", "sedan", "coupe", "suv", "hatchback"],
        "https://www.youtube.com/watch?v=u8dGzTZ9Z2s": ["toyota", "asian", "japanese", "economy", "performance", "sedan", "coupe", "suv", "hatchback"],
        "https://www.youtube.com/watch?v=4oC8cvUb0kI": ["toyota", "asian", "japanese", "economy", "performance", "sedan", "coupe", "suv", "hatchback"],
    }
    videos_fashion: Dict = {}
    videos_food: Dict = {}

    # Tag index holder
    tags_cars: Dict = {}
    tags_fashion: Dict = {}
    tags_food: Dict = {}

    # Quick enum definition based on category
    holder: Dict = {
        "cars": [videos_cars, tags_cars],
        "fashion": [videos_fashion, tags_fashion],
        "food": [videos_food, tags_food],
    }

    # Checks if we have initialized any scored
    updated: bool = False

    def _adjust_weights(self, url: str, video_arr: Dict, tag_arr: Dict, amount: int) -> None:
        """
        Private function the weight of the index url in the video array based on specific params
        @param url: string: url that's used as the index in the video database
        @param video_arr: dict: The video dictionary category
        @param tag_arr: dict: The tag index holder associated with the category
        @param amount: int: Integer amount associated with how much we want to adjust the weight
        """
        for tag in video_arr[url]:
            tag_arr[tag] += (amount+randint(-2,2))

    def adjust_weights(self, category: str, url: str, amount: int) -> None:
        """
        Public function to call internal function to adjust weights based on amount
        @param category: string: Category of data to mutate
        @param url: string: url that's used as the index in the video database
        @param amount: int: Integer amount associated with how much we want to adjust the weight
        """
        self.updated = True
        if category == "cars":
            self._adjust_weights(url, self.videos_cars, self.tags_cars, amount)
        elif category == "fashion":
            self._adjust_weights(url, self.videos_fashion, self.tags_fashion, amount)
        elif category == "food":
            self._adjust_weights(url, self.videos_food, self.tags_food, amount)

    def check_top_weights(self, video_arr: Dict, tag_arr: Dict) -> Dict:
        """
        Checks and returns the top weighted functions in descending order from highest to lowest
        @param video_arr: dict: The video dictionary category
        @param tag_arr: dict: The tag index holder associated with the category
        """
        urls: Dict = {}
        for url in video_arr:
            urls[url] = 0
            for tag in video_arr[url]:
                urls[url] += tag_arr[tag]
        return urls

    def _generate_recommendations(self, video_arr: Dict, tag_arr: Dict) -> Dict:
        """
        Internal function to generate recommendations based on inputs
        Returns random videos if we don't have any data
        @param video_arr: dict: The video dictionary category
        @param tag_arr: dict: The tag index holder associated with the category
        """
        weighted_tags: Dict = self.check_top_weights(video_arr, tag_arr)
        sorted_tags: Dict = dict( sorted(weighted_tags.items(), key=operator.itemgetter(1),reverse=True))
        if self.updated:
            return dict(itertools.islice(sorted_tags.items(), 5))
        else:
            sam = sample(list(video_arr), 3)
            return(sam)

    def generate_recommendations(self, category: str) -> Dict:
        """
        Function to call internal recommendation function based on category
        @param category: string: Category of recommendations we want to query
        """
        if category == "cars":
            return self._generate_recommendations(self.videos_cars, self.tags_cars)
        elif category == "fashion":
            return self._generate_recommendations(self.videos_fashion, self.tags_fashion)
        elif category == "food":
            return self._generate_recommendations(self.videos_food, self.tags_food)

    def _index_tags(self, video_arr: Dict, tag_arr: Dict) -> None:
        """
        Function to call internal recommendation function based on category
        @param video_arr: dict: The video dictionary category
        @param tag_arr: dict: The tag index holder associated with the category
        """
        for key in video_arr:
            tags = video_arr[key]
            for tag in tags:
                tag_arr[tag] = 0

    def __init__(self) -> None:
        """
        Initialization function
        Initializes and indexes tags
        """
        self._index_tags(self.videos_cars, self.tags_cars)
        self._index_tags(self.videos_fashion, self.tags_fashion)
        self._index_tags(self.videos_food, self.tags_food)