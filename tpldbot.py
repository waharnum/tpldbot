from lxml import etree
from random import randint
import sys
import tweepy
import time

# Expected usage: $ "python tpldbot.py [consumer_key] [consumer_secret] [access_token] [access_token_secret]"

consumer_key = str(sys.argv[1])
consumer_secret = str(sys.argv[2])

access_token = str(sys.argv[3])
access_token_secret = str(sys.argv[4])

result_feed_URL = "http://www.torontopubliclibrary.ca/rss.jsp?N=38550&Erp=0"

def get_random_item_number():
    tree = etree.parse(result_feed_URL)
    # Get the total results
    total_results = tree.find('channel').find('results').find('total-results').text
    # Generate a random number from the total results
    item_number = randint(1, int(total_results))
    return item_number

def get_item_by_number(number):
    record_feed_URL = "http://www.torontopubliclibrary.a/rss.jsp?N=38550&Erp=1&No=" + str(number)
    record_tree = etree.parse(record_feed_URL)
    item = record_tree.find('channel').find('item')
    return item

def construct_tweet(item):
    item_title = item.find('title').text

    item_link = item.find('link').text

    item_record = item.find('record')

    item_id = item_record.find('recordId').text

    item_image_file_name = item_record.xpath("./attributes/attr[@name='p_file_name']/text()")

    # We have to convert the file name to lowercase

    item_image_URL = "http://static.torontopubliclibrary.ca/da/images/MC/" + item_image_file_name[0].lower()

    # print("Title: " + item_title)
    # print("Record ID: " + item_id)
    # print("Link: " + item_link)
    # print("Image URL:" + item_image_URL)

    # Manual t.co length, should be safe for a while
    tweet_URL_max_length = 25
    tweet_title_trim_length = 140 - tweet_URL_max_length

    tweet_text = item_title[:tweet_title_trim_length] + " " + item_link

    return tweet_text

def make_tweet():
    # Get the record associated with a random number

    item = get_item_by_number(get_random_item_number())

    # Make a tweet from it

    tweet_text = construct_tweet(item)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    print("I'm making a tweet!")
    print(tweet_text)
    api.update_status(status=tweet_text)

# Run in an infinite loop, make a tweet every hour

while True:
    try:
        make_tweet()
        time.sleep(3600)
    except Exception as e:
        print("Failed to tweet. Exception:")
        print(str(e))
        time.sleep(900)
