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
import sqlite3
from datetime import datetime
import pandas as pd

current_date=datetime.now()
con = sqlite3.connect("users.db")
cur = con.cursor()

warnings.filterwarnings("ignore")
#We will have to get the product name and user based on the image from the frontend
product=""
user=""
parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=True)

def response_feedback(input_text):
    """
    args:
        input_text (str): Input_text.
    returns:
        response (str): A response to the feedback.
    """
    if feedback_polarity<0:  
        like_product="No"
        return choice(parrot.augment("I'm sorry you feel that way"))[0].capitalize()+". What would you like to see? ",like_product
    elif feedback_polarity>0:
        like_product="Yes"
        return choice(parrot.augment("I'm glad you feel that way"))[0].capitalize()+". What makes you feel this way?"
input_text=input("Hello, what do you think about this product?: ")
feedback_polarity = TextBlob(input_text).sentiment.polarity
while feedback_polarity==0:
    input_text=input("Please be more specific: ")
    feedback_polarity = TextBlob(input_text).sentiment.polarity
response_feedback,want_to_see=response_feedback(input_text)
input_text=input(response_feedback(input_text)[0])

sql_query=f"INSERT INTO transactions({user},{current_date},{product},{want_to_see})"
cur.execute()
con.commit()

print(choice(parrot.augment("Thank you have a good day!"))[0].capitalize())

items_df=pd.read_sql=("SELECT product,COUNT(Product) AS product_count FROM transacitons GROUP BY product ORDER BY COUNT(product) DESC")
print("You might also consider these items:\n")
for item in items_df["product"]:
    print(item)