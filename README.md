<img src="https://cdn.discordapp.com/attachments/1021609354065105036/1023634974194278520/logoB.png" width="100" height="100" align="right">
<br/><br/>

# eMotical


## Information
eMotical is a tool designed to improve the customer experience by tracking facial expressions and chat data. As we've seen in the past couple years, sales at brick and mortar stores are at an all time low. Online sales on the other hand have skyrocketed, and continue to rise. eCommerce is now the new status quo, and many companies are now digital first. eMotical focuses on understanding and creating a connection with the customer. By having a large amount of accurate data from our facial recognition and chat functions, we can leverage this in our data analysis to understand the customer further. We also focus on building trust, by transparency in data, and connecting further by showing sentiment in our chat conversations and expressing sympathy during these conversations. In the page of post-physical buying experiences, we can take advantage of the isolation that comes with eCommerce and offer an anonymous, safe and unjudged space where the user can interact with our platform. 

## Quick Overview
When the user loads the site, we create an instance for them. This instance has information like what attributes per category they feel positive about, which is taken by the recommendation engine to find similar videos they'd like. Each video is called a 'session', which has data local to the session like chat data and session specific emotional data. 

Recommendations are served based on categorical tagged data, which are influenced based on how the user feels about similar videos. When the emotions are processed for that video, it'll take how the user felt about aspects of the video and add those to the tagged weights. 

At the end of each session, the user is shown two graphs -- a graph of their emotions over the session, and a graph of their perceieved negativity and positivity through a score. It'll also give them a general score (-100 to 100) on how they felt about the video. 

## Connecting to Customers
Our first goal with eMotion is to connect with the customer as much as possible, which allows them to have a positive experience and get better recommendations of what to buy, and gives us the most amount of data while having accurate data since they trust the platform more. We take a couple of approaches to do this. 
- By appealing the environment to the customer, we're able to target individual customers and understand their wants over time
  - We establish a connection as not just an advertisement, but as an experience
- Reaching out to the customer in a friendly manner through our chatbot
  - We can collect the most accurate data through the chatbot since it's directly from the customer, with a large quantity of data if done right
  - We use their previous data to generate more responses through our decision tree
  - The user is asked for things they like or don't like from their data, which is analyzed into tags and more words through our wordnet and used to change recommendation weight to similar products if they like or don't like these things
  - We keep sentiment over session to form chats depending if they like or don't like the product, and express sympathy to ensure that they feel comfortable chatting. This positive energy makes sure the user provides the most data as possible. This aligns with our goal of being able to offer a safe space
- Engaging and influencing users
  - We have an advantage being able to engage with the customer from the comfort of their own home
    - We want to make sure they feel secure and trust the platform, hence why we show all emotion data and their video at the end
  - By tracking facial expressions in conjuction with the chat, we can understand the customer more
    - Understanding the customer means being able to better appeal with them
  - We build recommendations from our collected data to better serve them content that they'll enjoy
    - We update the recommendation engine's categorical tags that are associated with that content

## Tech Stack

- Frontend
  - React.js
- API Delivery
  - FastAPI
    - Writing a backend in Python allows for the quickest possible development experience
    - Natively supports concurrency and asynchronous
    - Comes with data validation, so we don't have to build this ourself
- Computer Vision
  - OpenCV
    - We used this for identifying and tracking faces
    - We were able to easily create bounding boxes around faces
    - Visualize the sentiments and most confident emotions
- Machine Learning
  - Rekognition
    - This was the weapon of choice for tackling facial expression analyis
    - Used a model to index emotions
      - Ran analysis at a rate of 10hz
      - Returns confidence of each emotion
  - PyTorch
    - We used this to construct a basic neural network and applied transfer learning for use with our NLP libraries
- Natural Language Processing
  - Natural Language Toolkit
    - TextBlobs
      - These have a naive bayne classifier natively
      - We used this specifically for sentiment analysis
    - Vader Lexicon Model  
      - Out of all the models we used, this model showed the best results
      - We focused on conversational and modern language, and Vader is specifically attuned to this
    - Parrot
      - In accordance with our vision to create actual conversations, Parrot allowed us to use a paraphraser model to create unique conversations
      - 

## Computing Optimizations

With the amount of raw data running through the backend of our stack, we noticed that running all of these functions, especially our artificial intelligence and machine learning functions were taking up a lot of resources and resulting in unacceptable latency times. These are some of the technologies and philosophies that we used to optimize our stack.

- Implemented parallel computing and multithreading
  - We ran many of our functions in parallel that don't require or access the same data or access
  - Implemented a thread pool for video export and computer vision functions
  - Used multiprocessing to run sentiment analysis functions in parallel
- Keep time-sensitive data close
  - Our CV, NLP and neural net algorithms all run on low latency, vertically scaling algorithms
    - All our models were pre-compiled and run locally to reduce latency
  - Our database and unessential APIs lie on Lambda functions that can run in the cloud
    - These queries generally don't require the level of latency associated with cloud computing, so we can deal with the latency associated
- Cython implementation
  - When optimizing our stack, Python's Global Interpreter Lock proved to be a problem
    - The Global Interpreter Lock is fine for 99% of use cases, but we were limited by the fact that it only allows one thread to control the Python interpreter
      - Proves to be a bottleneck since we can't perform 'true' multi-threading
    - By moving from the original implementation of Python, to Cython, we can bypass GIL
      - Once we moved over, we had to refactor our code heavily because the GIL prevents against memory leaks and allocating/releasing memory, something that we don't have to take into account when doing our initial system
      - Had to take into account when data is accessed and mutated, so we don't do concurrent accessing of memory addresses
    - We observed our CV functions, which went from a ridiculous amount of latency, to nearly being able to support realtime processing

## Data Implementation and Artificial Intelligence
- We track a heavy amount of live data points per second, which are fed to our facial recognition algorithms
  - We use Rekognition and OpenCV for facial recognition and expression analysis, as well as drawing bounding boxes to recognize faces
- Created an interaction chatbot with a basic decision tree
  - We use PyTorch and Parrot for utterance augmentation and NLU models
  - We decided to use the Vader Lexicon Model for sentiment analysis, which was great for casual conversaion -- which was the context of what we used the chatbot for
- Implemented dynamic tagging for our recommenation engine
  - We used a wordnet for tagging, which was able to give us the ability to relate words to each other and find similar tags in other video instances
  - This data was used to score tags based on the categorical data we had