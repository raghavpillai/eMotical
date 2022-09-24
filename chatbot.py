# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 22:01:16 2022

@author: bcohn
"""

from textblob import TextBlob
import time
time.clock = time.time
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Create a new chat bot named Charlie
chatbot = ChatBot("Bot")
input_text=input()
feedback_polarity = TextBlob(input_text).sentiment.polarity
trainer = ListTrainer(chatbot)
def response_feedback(input_text):
    """
    args:
        input_text (str): Input_text.
    returns:
        response (str): A response to the feedback.
    """
    feedback_polarity = TextBlob(input_text).sentiment.polarity
    if feedback_polarity>0:
         return "I'm glad you're feeling well!"
    else:
         return "Sorry you feel that way!"

trainer.train([
    "Hi, can I help you?",
    input_text,
    response_feedback(input_text)
])

response = chatbot.get_response(input_text)
print(response)