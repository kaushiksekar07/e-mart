from flask import Flask, request, redirect, url_for, render_template
import json

from Twitter import generateBearerToken
from Controller import itemDetails, addFeedback, adminProductDetails, adminGetFeedback
from Mongo import addItem, allItem

app = Flask(__name__)


@app.route("/", methods=["GET"])
def indexPage():
    return render_template("index.html")


@app.route("/deals", methods=["POST", "GET"])
def deals():
    if request.method == "POST":
        itemCode = request.form["itemCode"]
        return redirect(url_for("viewItem", itemCode = itemCode))
    else:
        data = allItem()
        return render_template("deals.html", data=data)


@app.route("/item/<string:itemCode>", methods = ["GET"])
def viewItem(itemCode):
        data = itemDetails(itemCode, bearerToken, True)
        return render_template("viewItem.html", data=data)
        

@app.route("/feedback", methods=["POST","GET"])
def respondFeedback():
    if request.method == "POST":
        requestData = request.form.to_dict()
        if requestData["feedbackType"] == "audio":
            requestData["audio"] = dict((request.files))["audioBlob"]

        data = addFeedback(requestData)

        return render_template("feedbackResponse.html", 
                customerName = requestData["customerName"],
                sentiment = data['sentiment'],
                responseGreet = data['greet'],
                responseMessage = data['message'],
                sentimentImage = data["sentimentImage"]
            )
    else:
        return redirect(url_for("index"))


@app.route("/reviews", methods=["POST", "GET"])
def reviews():
    if request.method == "POST":
        searchKey = request.form['searchKey']
        data = itemDetails(searchKey, bearerToken, False)
        return render_template("reviews.html", method = "POST", data = data)
    else:
        return render_template("reviews.html", method = "GET")


@app.route("/admin", methods=["POST", "GET"])
def adminLogin():
    if request.method == "POST":
        amail = request.form['amail']
        apassword = request.form['apassword']
        if apassword == "admin":
            return redirect(url_for("adminProducts"))
    else:
        return render_template("adminLogin.html")


@app.route("/admin/products", methods=["POST", "GET"])
def adminProducts():
    if request.method == "POST":
        itemCode = request.form["itemCode"]
        return redirect(url_for("adminViewProduct", itemCode = itemCode))
    else:
        data = allItem()
        return render_template("adminProducts.html", data=data)


@app.route("/admin/products/<string:itemCode>", methods=["GET"])
def adminViewProduct(itemCode):
    data = adminProductDetails(itemCode)
    return render_template("adminViewProduct.html", data=data)


@app.route("/admin/feedbacks", methods=["GET"])
def adminFeedback():
    if request.args:
        pid = request.args["pid"]
        sentiment = request.args["sentiment"]
    else:
        pid = "all"
        sentiment = "all"
    
    print(pid,sentiment)
    data = adminGetFeedback(pid, sentiment)

    return render_template("adminFeedback.html", data = data)


#POST - Add a new item
@app.route("/item", methods=["POST"])
def handleNewItem():
    data = addItem()
    return data


#Handler - Not Found
@app.errorhandler(404)
def handle_404(e):
    return redirect(url_for("indexPage"))


#Load JSON Twitter API Keys
config = json.load(open('keys/config.json', 'r'))
consumerKey = config['consumerKey']
consumerSecret = config['consumerSecret']


if __name__ == "__main__":
    bearerToken = generateBearerToken(consumerKey, consumerSecret)
    app.run(debug=True)