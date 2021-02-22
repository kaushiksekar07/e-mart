import json
import base64
import urllib.parse
import requests


def generateBearerToken(consumerKey, consumerSecret):
    encodedConsumerKey = urllib.parse.quote(consumerKey)
    encodedConsumerSecret = urllib.parse.quote(consumerSecret)
    credential = encodedConsumerKey + ":" + encodedConsumerSecret
    credential = base64.b64encode(credential.encode("utf-8"))

    url = "https://api.twitter.com/oauth2/token"
    headers = {
        "Authorization": f"Basic {credential.decode() }",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Accept-Encoding": "gzip"
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers = headers, data = data)
    response = response.json()

    bearerToken = response["access_token"]

    return bearerToken


def searchTweets(query, bearerToken):

    url = "https://api.twitter.com/1.1/search/tweets.json"
    headers = {
        "Authorization": f"Bearer {bearerToken}"
    }
    payload = {
        "q": urllib.parse.quote(query),
        "lang": "en",
        "count": 100,
        "tweet_mode": "extended"
    }
    response = requests.get(url, headers=headers, params=payload)
    response = response.json()

    tweets = []
    for tweet in response["statuses"]:
        tweets.append(tweet["full_text"])
    count = len(tweets)
    
    return tweets, count


    