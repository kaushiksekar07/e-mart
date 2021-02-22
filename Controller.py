from flask import Flask, request, jsonify
from matplotlib import pyplot as plt 

from Twitter import searchTweets
from SentimentAnalysis import findTweetSentiment, findFeedbackSentiment
from Mongo import getItem, storeFeedback, getProductFeedback
from SpeechToText import speechToText


def createChart(positiveReviews, neutralReviews, negativeReviews, name, code, chartType):
    # sentiments = ["POSITIVE", "NEUTRAL", "NEGATIVE"]
    sentimentCount = [positiveReviews, neutralReviews, negativeReviews]
    fig = plt.figure(figsize=(10, 7))

    explodes = [0, 0, 0]
    explodes[sentimentCount.index(max(sentimentCount))] = 0.2

    colors = ["green", "orange", "red"]
    plt.title(label = f"Customer's {chartType} on {name}", family="monospace", fontsize = 20, fontweight = "bold" ) 
    plt.pie(sentimentCount, explode = explodes, colors = colors)
    
    reviewChartName = code + "-"+ chartType +".jpg"
    plt.savefig(f"static/charts/{reviewChartName}")

    return reviewChartName


def itemDetails(pid, bearerToken, isCode):

    if isCode:
        item = getItem(pid)
        pname = item['pname']
    
    else:
        pname = pid

    tweets, count = searchTweets(pname, bearerToken)

    scoreList = findTweetSentiment(tweets)

    positiveReviews = 0
    neutralReviews = 0
    negativeReviews = 0
    positivity = 0
    reviewChartName = ""
    pid = pid.replace(" ", "")
    
    
    if count != 0:
        for score in scoreList:
            if score >= 3.0:
                positiveReviews += 1

            elif score >= 0 and score < 3.0:
                neutralReviews += 1
            
            else:
                negativeReviews += 1
        positivity = round(((positiveReviews/count) * 100), 2)
        chartType = "review"
        reviewChartName = createChart(positiveReviews, neutralReviews, negativeReviews, pname, pid, chartType)
    
      
    data = {
        "pid": pid,
        "pname": pname,
        "neutralReviews": neutralReviews,
        "negativeReviews": negativeReviews,
        "positiveReviews": positiveReviews,
        "itemImage": pid + ".jpg",
        "reviewChart": reviewChartName,
        "count": count,
        "positivity": positivity
    }

    if isCode:
        data["pdescp"] = item['pdescp']
        data["pprice"] = item['pprice']

    return data


def addFeedback(request):
   
    if request["feedbackType"] == "audio":
        customerFeedback = speechToText(request["audio"])
    else:
        customerFeedback = request["customerFeedback"]
    
    score = findFeedbackSentiment(customerFeedback)
    
    if score >= 3.0:
        sentiment = "positive"
        greet = "Thank You"
        message = "We are so happy that you enjoy the product."

    elif score >= 0 and score < 3.0:
        sentiment = "neutral"
        greet = "Uh-huh"
        message = "We take your words."
    
    else:
        sentiment = "negative"
        greet = "Regretted"
        message = "Really need to work hard to offer you the best."

    data = {
        "sentiment": sentiment,
        "greet": greet,
        "message": message,
        "sentimentImage": sentiment + ".jpg",
        "pid": request["pid"],
        "pname": request["pname"],
        "uname": request["customerName"],
        "umail": request["customerEmail"],
        "umobile": request["customerMobile"],
        "text": customerFeedback,
    }

    result = storeFeedback(data)

    return data


def adminProductDetails(pid):

    result = getProductFeedback(pid)
    product = result["oneProduct"]
    feedbacks = result["feedbacks"]
    count = len(feedbacks)
    positiveReviews = 0
    neutralReviews = 0
    negativeReviews = 0
    
    if count > 0:
        for item in feedbacks:
            if item['sentiment'] == 'positive':
                positiveReviews += 1
            elif item['sentiment'] == 'neutral':
                neutralReviews += 1
            else:
                negativeReviews += 1

    chartType = "feedback"
    pname = product["pname"]
    feedbackChartName = createChart(positiveReviews, neutralReviews, negativeReviews, pname, pid, chartType)

    data = {
        "pname": pname,
        "pid": product["pid"],
        "pdescp": product["pdescp"],
        "pprice": product["pprice"],
        "itemImage": pid + ".jpg",
        "feedbackChart": feedbackChartName,
        "neutralReviews": neutralReviews,
        "positiveReviews": positiveReviews,
        "negativeReviews": negativeReviews,
        "count": count
    }

    return data


def adminGetFeedback(pid, sentiment):
    result = getProductFeedback(pid)
    feedbacks = result["feedbacks"]
    productList = result["allProducts"]
    oneProduct = result["oneProduct"]
    
    feedbackList = []
    count = 0
    if len(feedbacks) > 0:
        if sentiment == "all":
            for item in feedbacks:
                count += 1
                temp = {
                    "sno": count,
                    "date": item["date"],
                    "pname": item["pname"],
                    "uname": item["uname"],
                    "umail": item["umail"],
                    "text": item["text"],
                    "sentiment": item["sentiment"]
                }
                feedbackList.append(temp)
        else:
            for item in feedbacks:
                if item['sentiment'] == sentiment:
                    count += 1
                    temp = {
                        "sno": count,
                        "date": item["date"],
                        "pname": item["pname"],
                        "uname": item["uname"],
                        "umail": item["umail"],
                        "text": item["text"],
                        "sentiment": item["sentiment"]
                    }
                    feedbackList.append(temp)

    productList.append({"pid": "all", "pname": "All Products"})
    sentimentList = [
        {"value": "all", "sentiment": "All Sentiment"},
        {"value": "positive", "sentiment": "Positive"},
        {"value": "neutral", "sentiment": "Neutral"},
        {"value": "negative", "sentiment": "Negative"}
    ]
    
    data = {
        "productList": productList,
        "feedbackList": feedbackList,
        "sentimentList": sentimentList,
        "oneProduct": oneProduct["pid"],
        "oneSentiment": sentiment,
        "count": count
    }

    return data

    