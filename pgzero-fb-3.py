import os
import time

x = 0
y = 0
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'

import pgzrun
from random import uniform
from socialapis import Facebook
from unidecode import unidecode
from textblob import TextBlob
from socialapis_auth import fb_api_token

# Match these dimensions to your display resolution
WIDTH = 1920
HEIGHT = 1080

# Interval in seconds between API calls
FETCH_INTERVAL = 60

# State variables to store sentiment image, raw score, and timing
current_image = 'hate-circuit-bg'
current_sentiment = 0.0
last_fetch_time = 0

def fb_post_sentiment(debug=False):
    # Set up FB search terms
    fb = Facebook(api_token=fb_api_token)
    result = fb.search_posts(
        "immigrant",
        start_time="2025-01-01",
        location_id="113013485375759", # Kingston upon Hull
    )

    # filter FB results to post data
    fb_info = result["data"]["items"]

    # handle empty responses safely
    if not fb_info:
        return 0.0

    sentiment_list = []

    for entry in fb_info:
        raw_post = entry["basic_info"]["post_text"]
        clean_post = unidecode(raw_post.replace("\n", " "))

        if debug:
            print(clean_post)
            print("----------")

        blob = TextBlob(clean_post)
        sentiment = blob.sentiment.polarity
        sentiment_list.append(sentiment)

        if debug:
            print(sentiment)
            print("----------")

    if debug:
        print(sentiment_list)

    avg_sentiment = sum(sentiment_list) / len(sentiment_list)
    print(f"Average Sentiment: {avg_sentiment}")

    return avg_sentiment

def update_sentiment_data():
    global current_image, current_sentiment
    
    current_sentiment = fb_post_sentiment(True)

    # Split the -1.0 to +1.0 range into thresholds
    if current_sentiment < 0:
        current_image = 'hate'
    elif current_sentiment > 0.05:
        current_image = 'love'
    elif 0 <= current_sentiment <= 0.05:
        current_image = 'unsure'
    else:
        current_image = 'hate-circuit-bg'

def draw():
    screen.clear()
    screen.blit(current_image, (0, 0))
    
    # Overlay sentiment score on top of the image
    sentiment_text = f"Sentiment Score: {current_sentiment:.3f}"
    screen.draw.text(
        sentiment_text,
        center=(WIDTH // 2, 80),
        fontsize=60,
        color="white",
        shadow=(2, 2),
        scolor="black"
    )

def update():
    global last_fetch_time

    debug = False  # Set to True if you want to print fetch countdowns

    current_time = time.time()

    # Run API request only if the interval time has elapsed
    if current_time - last_fetch_time >= FETCH_INTERVAL:
        update_sentiment_data()
        last_fetch_time = current_time
        
    if debug:
        print(f"Time to next fetch: {FETCH_INTERVAL - (current_time - last_fetch_time)}")

pgzrun.go()