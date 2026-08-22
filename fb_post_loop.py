from socialapis import Facebook
from unidecode import unidecode
from textblob import TextBlob
from socialapis_auth import fb_api_token

# display debug messages to screen
debug = False

# Set up FB search terms
fb = Facebook(api_token=fb_api_token)
result = fb.search_posts(
    "immigrant",
    #recency="last_year",
    start_time = "2024-01-01",
    end_time = "2026-08-01",
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

print(sentiment_list)

# create average sentiment of all returned posts
avg_sentiment = sum(sentiment_list) / len(sentiment_list)

print(avg_sentiment)

