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
        "https://www.youtube.com/watch?v=fPYho_m142c": ["bmw", "european", "german", "munich", "luxury", "sedan"],
        "https://www.youtube.com/watch?v=eMpszInH0xw": ["bmw", "european", "german", "munich", "luxury", "suv"],
        "https://www.youtube.com/watch?v=gCMQS3UDabo": ["mercedes", "european", "german", "affalterbach", "luxury", "performance", "suv"], 
        "https://www.youtube.com/watch?v=YqvOHgBhnBU": ["mercedes", "european", "german", "affalterbach", "luxury", "performance", "coupe"], 
        "https://www.youtube.com/watch?v=9MRmNDDp5i8": ["toyota", "asian", "japanese", "economy", "performance", "hatchback"],
        "https://www.youtube.com/watch?v=Gvn7jwqj8Zo": ["toyota", "asian", "japanese", "economy", "performance", "suv"],
        "https://www.youtube.com/watch?v=kbulCM90w8w": ["tesla", "united states", "luxury", "electric", "sedan"],
        "https://www.youtube.com/watch?v=hmd3mks6HPs": ["tesla", "united states", "luxury", "electric", "suv"],
        "https://www.youtube.com/watch?v=l5zT005oGbA": ["ford", "united states", "performance", "coupe", "v8"],
        "https://www.youtube.com/watch?v=Bq5EwFRab6Q": ["ford", "united states", "economy", "electric", "truck"],
        "https://www.youtube.com/watch?v=3YAIfSVln9s": ["nissan", "asian", "japanese", "economy", "sedan"],
        "https://www.youtube.com/watch?v=SQSaV7xp568": ["nissan", "asian", "japanese", "performance", "coupe"],
        "https://www.youtube.com/watch?v=yZT3hyhao-o": ["chevrolet", "united states", "mid-engined", "performance", "coupe"],
        "https://www.youtube.com/watch?v=d2ogGZXmepY": ["chevrolet", "united states", "economy", "electric", "hatchback"],
        "https://www.youtube.com/watch?v=5GhqclVU-so": ["honda", "asian", "japanese", "economy", "suv"],
        "https://www.youtube.com/watch?v=9ysZV_IA8ZU": ["honda", "asian", "japanese", "economy", "sedan"],
        "https://www.youtube.com/watch?v=ytfoYf5sjsA": ["hyundai", "asian", "korean", "economy", "performance", "hatchback"],
        "https://www.youtube.com/watch?v=RLf1CQg0Zpw": ["hyundai", "asian", "korean", "economy", "sedan"],
        "https://www.youtube.com/watch?v=VPDoBbfL7-E": ["volkswagen", "europen", "german", "economy", "sedan"],
        "https://www.youtube.com/watch?v=C4P6SJ6PCx8": ["volkswagen", "europen", "german", "performance", "hatchback"],
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

    def adjust_all_weights(self, category: str, url: str, amount: int) -> None:
        """
        Public function to call internal function to adjust weights based on amount
        @param category: string: Category of data to mutate
        @param url: string: url that's used as the index in the video database
        @param amount: int: Integer amount associated with how much we want to adjust the weight
        """
        self.updated = True
        self._adjust_weights(url, category, amount)
        for tag in self.holder[category][0][url]:
            self.holder[category][1][tag] += (amount+randint(-2,2))

    def adjust_ind_weight(self, category: str, tag: str, amount: int):
        """
        Adjust individual weights for the specific tag we want to adjust
        @param category: string: Category of data to mutate
        @param tag: str: actual tag we want to mutate
        @param amount: amount that we want to mutate the tag by
        """
        self.holder[category][1][tag] += (amount+randint(-2,2))

    def check_top_weights(self, category: str) -> Dict:
        """
        Checks and returns the top weighted functions in descending order from highest to lowest
        @param category: string: Category of recommendations we want to check
        """
        urls: Dict = {}
        for url in self.holder[category][0]:
            urls[url] = 0
            for tag in self.holder[category][0][url]:
                urls[url] += self.holder[category][1][tag]
        return urls

    def generate_recommendations(self, category: str) -> Dict:
        """
        Function to call internal recommendation function based on category
        @param category: string: Category of recommendations we want to query
        """
        weighted_tags: Dict = self.check_top_weights(category)
        sorted_tags: Dict = dict( sorted(weighted_tags.items(), key=operator.itemgetter(1),reverse=True))
        if self.updated:
            return dict(itertools.islice(sorted_tags.items(), 5))
        else:
            sam = sample(list(self.holder[category][0]), 3)
            return(sam)

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