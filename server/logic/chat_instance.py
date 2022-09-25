import time
from typing import List

from textblob import TextBlob
import time
from random import choice
from parrot import Parrot
import warnings
warnings.filterwarnings("ignore")

parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)

class ChatInstance(object):
    # Quick status to see if we went past description chat
    status: int = 0

    def response_feedback(self,input_text) -> str:
        """
        Initial response when the user states their feeling
        @param input_text: str: Message string from the client
        @return str: Returns either good or bad sentiment asking user to explain feeling
        """
        feedback_polarity = TextBlob(input_text).sentiment.polarity
        if feedback_polarity < 0:
            return choice(parrot.augment("I'm sorry you feel that way"))[0].capitalize()+" What would you like to see?"
        elif feedback_polarity > 0:
            return choice(parrot.augment("I'm glad you feel that way"))[0].capitalize()+" What makes you feel this way?"

    def initial_chat(self) -> str:
        """
        First message to start our chat process
        @return str: initial chat message
        """
        return "Hello, what do you think about this product?"
    
    def chat_callback(self, msg: str) -> str:
        """
        Function called when a new chat is sent to the server
        @param msg: str: Message from client
        @return str: String to return and fire back to the client
        """
        feedback_polarity = TextBlob(msg).sentiment.polarity
        if feedback_polarity == 0:
            return "Please be more specific and try again"
        
        if self.status == 0:
            return self.response_feedback(msg)
        
        return(choice(parrot.augment("Thank you have a good day!"))[0].capitalize())
    
    def __init__(self):
        """
        Object initialization
        """
        print("Created chat instance")