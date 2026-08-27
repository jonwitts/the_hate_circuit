#!/usr/bin/python3

# used for testing with random sentiment values
#from random import uniform
from socialapis import Facebook
from unidecode import unidecode
from textblob import TextBlob
# import the fb_api_token from the socialapis_auth.py file
# not included in this repo for security reasons
from socialapis_auth import fb_api_token


def fb_post_sentiment(debug=False):
    # Set up FB search terms
    fb = Facebook(api_token=fb_api_token)
    result = fb.search_posts(
        "immigrant",
        start_time="2025-01-01",
        recent_posts=True,
        location_id="113013485375759",  # Kingston upon Hull
    )

    # filter FB results to post data
    fb_info = result["data"]["items"]

    # handle empty responses safely
    if not fb_info:
        return 0.0

    # Empty list to store sentiment scores
    sentiment_list = []

    # Loop through each post, clean the text, and calculate sentiment
    for entry in fb_info:
        raw_post = entry["basic_info"]["post_text"]
        # Clean the post text by removing newlines and converting to ASCII
        clean_post = unidecode(raw_post.replace("\n", " "))
        if debug:
            print(clean_post)
            print("----------")

        # Use TextBlob to calculate sentiment polarity
        blob = TextBlob(clean_post)
        sentiment = blob.sentiment.polarity
        # Append the sentiment score to the list
        sentiment_list.append(sentiment)
        if debug:
            print(sentiment)
            print("----------")
    if debug:
        print(sentiment_list)
    # Calculate the average sentiment score
    avg_sentiment = sum(sentiment_list) / len(sentiment_list)
    if debug:
        print(f"Average Sentiment: {avg_sentiment}")
    return avg_sentiment

fb_post_sentiment(True)