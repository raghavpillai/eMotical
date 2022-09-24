import operator

class Recommendations:
    # Cars
    # Fashion
    # Food

    videos_cars = {
        "ff": ["","","",""],
    }
    videos_fashion = []
    videos_food = []

    tags_cars = []
    tags_fashion = []
    tags_food = []

    def adjust_weights(self, url, video_arr, tag_arr, amount):
        for tag in video_arr[url]:
            tag_arr[tag] += amount

    def increase_weights(self, category, url):
        if category == "cars":
            self.adjust_weights(url, self.videos_cars, self.tags_cars, 10)
        elif category == "fashion":
            self.adjust_weights(url, self.videos_fashion, self.tags_fashion, 10)
        elif category == "food":
            self.adjust_weights(url, self.videos_food, self.tags_food, 10)

    def check_top_weights(self, video_arr, tag_arr):
        sorted_tags = dict( sorted(tag_arr.items(), key=operator.itemgetter(1),reverse=True))
        
        urls = {}
        for url in video_arr:
            urls[url] = 0
            for tag in video_arr[url]:
                urls[url] += tag


    def generate_recommendations(self, category):
        for url in 

    def _index_tags(self, video_arr, tag_arr):
        for key in video_arr:
            tags = video_arr[key]
            for tag in tags:
                tag_arr[tag] = 0

    def __init__(self):
        self._index_tags(self.video_cars, self.tags_cars)
        self._index_tags(self.videos_fashion, self.tags_fashion)
        self._index_tags(self.videos_food, self.tags_food)