# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 22:01:16 2022

@author: bcohn
"""
"""
Before running, run the following commands in the termina;:
pip install textblod
pip install git+https://github.com/PrithivirajDamodaran/Parrot.git
pip install chatterbot
"""


from textblob import TextBlob
import time
from random import choice
time.clock = time.time
from parrot import Parrot
import torch
import warnings

warnings.filterwarnings("ignore")

parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=True)

def response_feedback(input_text):
    """
    args:
        input_text (str): Input_text.
    returns:
        response (str): A response to the feedback.
    """
    
    if feedback_polarity<0:
        return choice(parrot.augment("I'm sorry you feel that way"))[0].capitalize()+". What would you like to see? "
    elif feedback_polarity>0:
        return choice(parrot.augment("I'm glad you feel that way"))[0].capitalize()+". What makes you feel this way?"
input_text=input("Hello, what do you think about this product?: ")
feedback_polarity = TextBlob(input_text).sentiment.polarity
while feedback_polarity==0:
    input_text=input("Please be more specific: ")
    feedback_polarity = TextBlob(input_text).sentiment.polarity
input_text=input(response_feedback(input_text))
print(choice(parrot.augment("Thank you have a good day!"))[0].capitalize())
