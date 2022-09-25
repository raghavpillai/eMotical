import time
from typing import List
import requests
from textblob import TextBlob
import time
from random import choice
from parrot import Parrot
import warnings
warnings.filterwarnings("ignore")

import nltk
from nltk.corpus import wordnet as wn
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon', quiet = True)
nltk.download('omw-1.4')
nltk.download('wordnet', quiet = True)
sentiment_analyzer = SentimentIntensityAnalyzer()

parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)

class ChatInstance(object):
    # Quick status to see if we went past description chat
    status: int = 0

    # Status 0: Not given initial sentiment yet
    # Status 1: Given initial sentiment, waiting for more possible tags to increase
    # Status 2: Prompt complete, no more responses

    def check_sentiment(self, input_text: str) -> int:
        return sentiment_analyzer.polarity_scores(input_text)

    def response_0(self,input_text,url,category) -> str:
        # Initial response to how they feel. Ask then what 
        feedback_polarity = TextBlob(input_text).sentiment.polarity
        if feedback_polarity < 0:
            self.status = 1
            requests.get(f'http://127.0.0.1:8000/v1/emotions/update_entity/{category}/{url}/-15')
            return choice(parrot.augment("I'm sorry you feel that way."))[0].capitalize()+".What makes you feel this way?"
        elif feedback_polarity > 0:
            self.status = 1
            requests.get(f'http://127.0.0.1:8000/v1/emotions/update_entity/{category}/{url}/15')
            return choice(parrot.augment("I'm glad you feel that way."))[0].capitalize()+". What makes you feel this way?"

    def response_1(self,input_text,category,tag) -> str:
        # Asked what makes them feel this way
        # Ask what they'd they'd like to see in future products
        self.status = 2
        good_list=input_text.split(" ")
        for word in good_list:
            requests.get(f'http://127.0.0.1:8000/v1/emotions/update_ind_entity/{category}/{word}/5')
            print(word)
        #name = "love"+".n.01"
        #paths = wn.synsets(name).hypernym_paths()
        #for path in paths:
            #print([s.lemmas[0].name for s in path])
        
        return "I understand. What sort of things would you to see in future products in this category? A list of things would be great!"

    def response_2(self,input_text,category,tag) -> str:
        # Given a list of things they'd like to see in this category. 
        # Ask what they don't want to see in the next product
        self.status = 3
        bad_list=input_text.split(" ")
        for word in bad_list:
            requests.get(f'http://127.0.0.1:8000/v1/emotions/update_ind_entity/{category}/{word}/-5')
            print(word)
        #name = "love"+".n.01"
        #paths = wn.synsets(name).hypernym_paths()
        #for path in paths:
            #print([s.lemmas[0].name for s in path])
        return(choice(parrot.augment("What list of things wouldn't you want to see in the next category?")))[0].capitalize()

    def response_3(self,input_text,url,category) -> str:
        # Given a list of things they don't want to see in this category. 
        # Thank them for their time, and to enjoy their day
        self.status = 4
        return(choice(parrot.augment("Thank you for your insights"))[0].capitalize()+".Have a great day!")
    
    def chat_callback(self, msg: str,url,category) -> str:
        """
        Function called when a new chat is sent to the server
        @param msg: str: Message from client
        @return str: String to return and fire back to the client
        """
        feedback_polarity = TextBlob(msg).sentiment.polarity
        if self.status == 0 and feedback_polarity == 0:
            return "Please be more specific and try again"
        
        if self.status == 0: # Initial response to feeling
            return self.response_0(msg,url,category)

        if self.status == 1: # Response to why they felt that way
            return self.response_1(msg,url,category)

        if self.status == 2: # Given a list of things they'd like to see in this category
            return self.response_2(msg,url,category)

        if self.status == 3 : # Given a list of things they'd like to see in this category
            return self.response_3(msg,url,category)
        
        return(choice(parrot.augment("Hey, thanks for your insights! We'll talk  again soon.")))
    
    def __init__(self):
        """
        Object initialization
        """
        print("Created chat instance")