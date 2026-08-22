x = 0
y = 0
import os
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

def fb_post_sentiment(debug = False):
    # Set up FB search terms
    fb = Facebook(api_token=fb_api_token)
    result = fb.search_posts(
        "immigrant",
        #recency="last_year",
        start_time = "2025-01-01",
        #end_time = "2026-08-01",
        location_id="113013485375759", # 113013485375759 is Kingston upon Hull
        )

    # filter FB results to post data
    fb_info = result["data"]["items"]

    # create empty list to store post sentiments
    sentiment_list = []

    # loop through all retrieved posts
    for entry in fb_info:
        # grab raw post text
        raw_post = entry["basic_info"]["post_text"]
        # remove line breaks
        clean_post = raw_post.replace("\n", " ")
        # remove non-unicode characters
        clean_post = unidecode(clean_post)
        if debug:
            print(clean_post)
            print("----------")
        # create blob for sentiment analysis
        blob = TextBlob(clean_post)
        sentiment = blob.sentiment.polarity
        # append post sentiment value to list
        sentiment_list.append(sentiment)
        if debug:
            print(sentiment)
            print("----------")

    if debug:
        print(sentiment_list)

    # create average sentiment of all returned posts
    avg_sentiment = sum(sentiment_list) / len(sentiment_list)
    print(avg_sentiment)

    return(avg_sentiment)

def get_sentiment_image():
    sentiment = fb_post_sentiment(True)

    # Split the -1.0 to +1.0 range into three thresholds
    if sentiment < 0:
        return 'hate'    # Negative sentiment
    elif sentiment > 0.05:
        return 'love'   # Positive sentiment
    elif 0 < sentiment < 0.05:
        return 'unsure' # Neutral sentiment
    else:
        return 'hate-circuit-bg'      # Neutral sentiment

def draw():
    screen.clear()

    # Fetch image choice based on current sentiment and render full screen
    current_image = get_sentiment_image()
    screen.blit(current_image, (0, 0))

def update():
    # Pygame Zero game loop update logic (if needed for animations or state)
    pass

pgzrun.go()
