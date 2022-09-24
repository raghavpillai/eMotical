# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 22:01:16 2022

@author: bcohn
"""

from textblob import TextBlob
import time
time.clock = time.time
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer,ChatterBotCorpusTrainer

chatbot = ChatBot("Bot")

trainer = ListTrainer(chatbot)
def response_feedback(input_text):
    """
    args:
        input_text (str): Input_text.
    returns:
        response (str): A response to the feedback.
    """
    feedback_polarity = TextBlob(input_text).sentiment.polarity
    return ''.join("I'm glad you're doing well!" 
           if feedback_polarity>0 
           else "Sorry you feel that way!")
        
input_text=input("Hello, how can I help you? ")
response_feedback=response_feedback(input_text)+" Why do you feel that way?"
feedback_polarity = TextBlob(input_text).sentiment.polarity
trainer.train([
    input_text,
    response_feedback,
    
])
response = chatbot.get_response(input_text)
input_text=input(response)
trainer.train([
    input_text,
    "Thank you, have a good day.",
    
])
response = chatbot.get_response(input_text)
print(response)



