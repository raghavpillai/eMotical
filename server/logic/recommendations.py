import operator
import itertools
from random import randint, sample
from typing import Dict

class Recommendations:
    """
    Recommendation files
    """

    # Video database
    _videos_cars: Dict = {
        "fPYho_m142c": ["bmw", "european", "german", "munich", "luxury", "sedan"],
        "eMpszInH0xw": ["bmw", "european", "german", "munich", "luxury", "suv"],
        "gCMQS3UDabo": ["mercedes", "european", "german", "affalterbach", "luxury", "performance", "suv"], 
        "YqvOHgBhnBU": ["mercedes", "european", "german", "affalterbach", "luxury", "performance", "coupe"], 
        "9MRmNDDp5i8": ["toyota", "asian", "japanese", "economy", "performance", "hatchback"],
        "Gvn7jwqj8Zo": ["toyota", "asian", "japanese", "economy", "performance", "suv"],
        "kbulCM90w8w": ["tesla", "united states", "luxury", "electric", "sedan"],
        "hmd3mks6HPs": ["tesla", "united states", "luxury", "electric", "suv"],
        "l5zT005oGbA": ["ford", "united states", "performance", "coupe", "v8"],
        "Bq5EwFRab6Q": ["ford", "united states", "economy", "electric", "truck"],
        "3YAIfSVln9s": ["nissan", "asian", "japanese", "economy", "sedan"],
        "SQSaV7xp568": ["nissan", "asian", "japanese", "performance", "coupe"],
        "yZT3hyhao-o": ["chevrolet", "united states", "mid-engined", "performance", "coupe"],
        "d2ogGZXmepY": ["chevrolet", "united states", "economy", "electric", "hatchback"],
        "5GhqclVU-so": ["honda", "asian", "japanese", "economy", "suv"],
        "9ysZV_IA8ZU": ["honda", "asian", "japanese", "economy", "sedan"],
        "ytfoYf5sjsA": ["hyundai", "asian", "korean", "economy", "performance", "hatchback"],
        "RLf1CQg0Zpw": ["hyundai", "asian", "korean", "economy", "sedan"],
        "VPDoBbfL7-E": ["volkswagen", "europen", "german", "economy", "sedan"],
        "C4P6SJ6PCx8": ["volkswagen", "europen", "german", "performance", "hatchback"],
    }
    _videos_fashion: Dict = {}
    _videos_food: Dict = {
        "https://www.youtube.com/watch?v=mxR3aGGBXt0": ["pizza", "european", "italian", "cheese", "vegetarian", "non-vegetarian", "meal"],
        "https://www.youtube.com/watch?v=G9Mj9BO-r1c": ["burger", "american", "meat", "cheese", "lettuce", "non-vegetarian", "meal"],
        "https://www.youtube.com/watch?v=S4T0VVNm07o": ["doughnut", "american", "sugar", "dough", "desert"],
        "https://www.youtube.com/watch?v=_eQ2Dry2R_8": ["taco", "latin american", "cheese", "vegetarian", "non-vegetarian", "meal"],
        "https://www.youtube.com/watch?v=L6IYy95ODDU": ["chips", "american", "potatoes", "salt", "baked", "snack"],
        "https://www.youtube.com/watch?v=nVfE0G19KaI": ["fried chicken", "american", "chicken", "salt", "non-vegetarian", "meal"],
        "https://www.youtube.com/watch?v=U4K7X6YboQM": ["french fries", "european", "potatoes", "salt", "fried", "snack"],
        "https://www.youtube.com/watch?v=VqANgtxKLbM": ["coffee", "worldwide", "sugar", "coffee beans", "milk", "beverage"],
        "https://www.youtube.com/watch?v=2H0tglcIKsM": ["chocolate", "worldwide", "cacao beans", "sugar", "desert"],
        "https://www.youtube.com/watch?v=5J43R-DDmNc": ["pasta", "european", "italian", "wheat", "vegetarian", "non-vegetarian", "meal"],
        "https://www.youtube.com/watch?v=CyOiXph_ahM": ["biryani", "asian", "india", "rice", "vegetarian", "non-vegetarian", "meal"],
        "https://www.youtube.com/watch?v=1qlrRmRTbVY": ["ice cream", "worldwide", "sugar", "milk", "flavoring", "desert"],
        "https://www.youtube.com/watch?v=WZpK-M7wKVk": ["popcorn", "worldwide", "corn kernels", "butter", "snack"],
        "https://www.youtube.com/watch?v=zMSrEBhQcUg": ["cake", "worldwide", "dough", "sugar", "milk", "desert"],
        "https://www.youtube.com/watch?v=GGxRzOkJtVc": ["sushi", "asian", "japanese", "rice", "seafood", "vegetables", "non-vegetarian", "meal"]
    }

    # Tag index holder
    _tags_cars: Dict = {}
    _tags_fashion: Dict = {}
    _tags_food: Dict = {}

    # Quick enum definition based on category
    holder: Dict = {
        "cars": [_videos_cars, _tags_cars],
        "fashion": [_videos_fashion, _tags_fashion],
        "food": [_videos_food, _tags_food],
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
        for tag in self.holder[category][0][url]:
            self.holder[category][1][tag] += (amount+randint(-2,2))
        print("\t\tAdjusting all weights")

    def adjust_ind_weight(self, category: str, tag: str, amount: int):
        """
        Adjust individual weights for the specific tag we want to adjust
        @param category: string: Category of data to mutate
        @param tag: str: actual tag we want to mutate
        @param amount: amount that we want to mutate the tag by
        """
        self.holder[category][1][tag] += (amount+randint(-2,2))
        print(f"\t\tUpdated individual weight for {category} by {amount}")

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
        print("\t\tRe-organizing entities")
        return urls

    def generate_recommendations(self, category: str) -> Dict:
        """
        Function to call internal recommendation function based on category
        @param category: string: Category of recommendations we want to query
        """
        weighted_tags: Dict = self.check_top_weights(category)
        sorted_tags: Dict = dict( sorted(weighted_tags.items(), key=operator.itemgetter(1),reverse=True))
        if self.updated:
            print("\tServing sorted recommendations")
            return dict(itertools.islice(sorted_tags.items(), 5))
        else:
            print("\tServing vanilla recommendations")
            sam = sample(list(self.holder[category][0]), 5)
            return(sam)

    def _index_tags(self, video_arr: Dict, tag_arr: Dict) -> None:
        """
        Function to call internal recommendation function based on category
        @param video_arr: dict: The video dictionary category
        @param tag_arr: dict: The tag index holder associated with the category
        """
        print(f"\t\tIndexing category dataset")
        for key in video_arr:
            tags = video_arr[key]
            for tag in tags:
                tag_arr[tag] = 0

    def __init__(self) -> None:
        """
        Initialization function
        Initializes and indexes tags
        """
        print("\tBeginning data indexing...")
        self._index_tags(self._videos_cars, self._tags_cars)
        self._index_tags(self._videos_fashion, self._tags_fashion)
        self._index_tags(self._videos_food, self._tags_food)
        print("\tEnded data indexing...")