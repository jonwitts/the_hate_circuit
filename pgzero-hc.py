#!/usr/bin/python3

# Force the Pygame window to open at a specific position on the screen
import os

x = 0
y = -55  # account for taskbar and window title height
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'

import sys
import pgzrun
import pygame
import RPi.GPIO as GPIO
import time
# used for testing with random sentiment values
# from random import uniform
from socialapis import Facebook
from unidecode import unidecode
from textblob import TextBlob
# import the fb_api_token from the socialapis_auth.py file
# not included in this repo for security reasons
from socialapis_auth import fb_api_token

# Set up window dimensions and title
WIDTH = 1920
HEIGHT = 1080
TITLE = "The Hate Circuit"

# Interval in seconds between API calls
FETCH_INTERVAL = 300  # 5 minutes

# Fallback path detection for Pygame Zero / pgzrun execution
try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
except Exception:
    SCRIPT_DIR = os.getcwd()

# Path for persistent storage of sentiment scores
SCORES_FILE = os.path.join(SCRIPT_DIR, 'scores.txt')


def load_scores(debug=False):
    '''Reads saved love and hate scores from a file, defaulting to (0, 0).'''
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, 'r') as f:
                data = f.read().strip().split(',')
                love, hate = int(data[0]), int(data[1])
                if debug:
                    print(f"Successfully loaded scores from {SCORES_FILE}: Love={love}, Hate={hate}")
                return love, hate
        except Exception as e:
            if debug:
                print(f"Error reading scores file: {e}")
                print(f"File exists at {SCORES_FILE} but failed to read ({e}). Resetting to 0, 0.")
    else:
        if debug:
            print(f"Scores file {SCORES_FILE} does not exist. Initializing scores to 0, 0.")
    return 0, 0


def save_scores(love, hate, debug=False):
    '''Saves love and hate scores to a file.'''
    try:
        with open(SCORES_FILE, 'w') as f:
            f.write(f"{love},{hate}")
        if debug:
            print(f"Successfully saved scores to {SCORES_FILE}: Love={love}, Hate={hate}")
    except Exception as e:
        if debug:
            print(f"Error writing scores to {SCORES_FILE}: {e}")


# Variables for sentiment image, initial sentiment, scores, and fetch time
current_image = 'hate-circuit-bg'
current_sentiment = 0.0
last_fetch_time = time.time() - FETCH_INTERVAL + 10
# Initialize scores from file on startup
love_score, hate_score = load_scores(True)


def fb_post_sentiment(debug=False):
    try:
        # Set up FB search terms
        fb = Facebook(api_token=fb_api_token)
        result = fb.search_posts(
            "immigrant",
            start_time="2025-01-01",
            recent_posts=True,
            location_id="113013485375759",  # Kingston upon Hull
        )

        # Safely extract fb_info whether result is a dict or custom object
        if isinstance(result, dict):
            fb_info = result.get("data", {}).get("items", [])
        else:
            fb_info = result["data"]["items"]

        # handle empty responses safely
        if not fb_info:
            return 0.0

        # Empty list to store sentiment scores
        sentiment_list = []

        # Loop through each post, clean the text, and calculate sentiment
        for entry in fb_info:
            if isinstance(entry, dict):
                raw_post = entry.get("basic_info", {}).get("post_text", "")
            else:
                raw_post = entry["basic_info"]["post_text"]

            if not raw_post:
                continue  # Skip if post text is empty

            # Clean the post text by removing newlines and converting to ASCII
            clean_post = unidecode(raw_post.replace("\n", " "))
            if debug:
                print(clean_post)
                print("----------")

            # Use TextBlob to calculate sentiment polarity
            blob = TextBlob(clean_post)
            # Append the sentiment score to the list
            sentiment_list.append(blob.sentiment.polarity)
            if debug:
                print(blob.sentiment.polarity)
                print("----------")

        # Avoid DivisionByZero if no valid posts were found
        if not sentiment_list:
            return 0.0

        if debug:
            print(sentiment_list)

        # Calculate the average sentiment score
        avg_sentiment = sum(sentiment_list) / len(sentiment_list)
        if debug:
            print(f"Average Sentiment: {avg_sentiment}")
        return avg_sentiment
    except Exception as e:
        if debug:
            print(f"Error during sentiment fetch: {e}")
        # Default to neutral sentiment if an error occurs
        return 0.0


def relay_trigger(relay_int, on_off, debug=False):
    '''
    wire positive between A and C on relay
    A to power, C to device

    relay_int = 5, 6, 13, 16, 19, 20, 21, 26
    on_off = on OR off
    debug = True OR False, defaults to False
    '''

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    Relay = [5, 6, 13, 16, 19, 20, 21, 26]

    if debug:
        print("setup relays")
    for i in range(len(Relay)):
        GPIO.setup(Relay[i], GPIO.OUT)
        GPIO.output(Relay[i], GPIO.HIGH)

    if debug:
        print("checking relay_int")
    if relay_int in Relay:
        if debug:
            print("toggle relay")
        if on_off == "on":
            GPIO.output(relay_int, GPIO.LOW)
        elif on_off == "off":
            GPIO.output(relay_int, GPIO.HIGH)


def update_sentiment_data():
    global current_image, current_sentiment, love_score, hate_score

    # Fetch the current sentiment score from Facebook posts
    # pass True to enable debug output
    current_sentiment = fb_post_sentiment()

    # Track if scores changed so we only write to disk when necessary
    score_updated = False

    # Split the -1.0 to +1.0 range into thresholds
    if current_sentiment < 0:
        # set image to hate, increment hate score and switch off relay
        current_image = 'hate'
        hate_score += 1
        relay_trigger(5, "off")
        score_updated = True
    elif current_sentiment > 0.009:
        # set image to love, increment love score and switch on relay
        current_image = 'love'
        love_score += 1
        relay_trigger(5, "on")
        score_updated = True
    elif 0 <= current_sentiment <= 0.009:
        # set image to unsure, switch off relay
        current_image = 'unsure'
        relay_trigger(5, "off")
    else:
        current_image = 'hate-circuit-bg'

    # Save scores to file if either score incremented
    if score_updated:
        save_scores(love_score, hate_score, True)


def draw():
    screen.clear()
    screen.blit(current_image, (0, 0))

    # Overlay sentiment score on top of the image
    sentiment_text = f"CURRENT SENTIMENT SCORE: {current_sentiment:.3f}"
    screen.draw.text(
        sentiment_text,
        center=(WIDTH // 2, 100),
        fontsize=70,
        color="black",
        fontname="anton-regular"
    )

    # Overlay love and hate scores
    love_text = f"LOVE: {love_score}"
    hate_text = f"HATE: {hate_score}"
    screen.draw.text(
        love_text,
        center=(WIDTH // 4, HEIGHT - 100),
        fontsize=60,
        color="black",
        fontname="anton-regular"
    )
    screen.draw.text(
        hate_text,
        center=(3 * WIDTH // 4, HEIGHT - 100),
        fontsize=60,
        color="black",
        fontname="anton-regular"
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
        time_to_fetch = FETCH_INTERVAL - (current_time - last_fetch_time)
        print(f"Time to next fetch: {time_to_fetch}")


pgzrun.go()
