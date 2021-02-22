from pymongo import MongoClient
from flask import Flask, request, jsonify
from datetime import date 
import json

def connectDb():
    twitterConfig = json.load(open('keys/config.json', 'r'))
    clientUri = twitterConfig['clientUri']

    try:
        client = MongoClient(clientUri)
        return client
    
    except Exception as error:
        print(f"Connection Error: {error}")
        return False


def addItem():
    client = connectDb()
    print(f"Connection Status: {client}")

    if client is False:
        return jsonify({
            "error": "Connection failed"
        })
    else:
        try:
            db = client['emart']
            collection = db["product"]

            pid = request.json.get("pid")
            pname = request.json.get("pname")
            pdescp = request.json.get("pdescp")
            pprice = request.json.get("pprice")

            query = {"pid": pid, "pname": pname, "pdescp": pdescp, "pprice":pprice}
             
            result = collection.insert_one(query)

            return jsonify({
                # "result": response,
                 "result": "success",
                "_id": str(result.inserted_id),
                "acknowledged": str(result.acknowledged)
            })
            
        except Exception as error:
            print(error)
            return jsonify({
                "error": error
            })
        
        finally:
            if client:
                client.close()


def allItem():
    client = connectDb()
    print(f"Connection Status: {client}")

    if client is False:
        return jsonify({
            "error": "Connection failed"
        })
    else:
        try:
            db = client['emart']
            collection = db["product"]

            cursor = collection.find()
            items = []
            for item in cursor:
                items.append({
                    "pid" : item['pid'],
                    "pname" : item['pname'],
                    "pdescp" : item['pdescp'],
                    "pprice": item['pprice'],
                    "pimage": f"{item['pid']}.jpg"
                })

            return items

        
        except Exception as error:
            print(error)
            return jsonify({
                "error": error
            })
        
        finally:
            if client:
                client.close()


def getItem(pid):
    client = connectDb()
    print(f"Connection Status: {client}")

    if client is False:
        return jsonify({
            "error": "Connection failed"
        })
    else:
        try:
            db = client['emart']
            collection = db["product"]

            query = {"pid": pid}
            result = collection.find_one(query)

            return result

        except Exception as error:
            print(error)
            return jsonify({
                "error": error
            })
        
        finally:
            if client:
                client.close()

def storeFeedback(data):
    client = connectDb()
    print(f"Connection Status: {client}")

    if client is False:
        return jsonify({
            "error": "Connection failed"
        })

    else:
        try:
            db = client['emart']
            collection = db["feedback"]

            pid = data["pid"]
            pname = data["pname"]
            uname = data["uname"]
            umail = data["umail"]
            umobile = data["umobile"]
            text = data["text"]
            sentiment = data["sentiment"]
            

            query = {
                "pid": pid,
                "pname": pname,
                "uname": uname,
                "umail": umail,
                "umobile": umobile,
                "text": text,
                "sentiment": sentiment,
                "date": str(date.today())
            
            }
            # print(query)
            result = collection.insert_one(query)

            return {
                "result": "success",
                "_id": str(result.inserted_id),
                "acknowledged": str(result.acknowledged)
            }
            
        except Exception as error:
            print(error)
            return {
                "error": error
            }
        
        finally:
            if client:
                client.close()

def getProductFeedback(pid):
    client = connectDb()
    print(f"Connection Status: {client}")

    if client is False:
        return jsonify({
            "error": "Connection failed"
        })
    else:
        try:
            db = client['emart']
            collection = db["product"]
            
            feedbacks = []
            allProducts = []
            oneProduct = {"pid": "all"}
            cursor = collection.find()
            for item in cursor:
                allProducts.append({"pid": item["pid"], "pname": item["pname"]})
            
            
            collection = db["feedback"]
            
            if pid == "all":
                cursor = collection.find()
                for item in cursor:
                    feedbacks.append(item)
                
                
            else:
                query = {"pid": pid}
                cursor = collection.find(query)
                for item in cursor:
                    feedbacks.append(item)
               
                collection = db["product"]
                oneProduct = collection.find_one(query)

            
            return {
                "allProducts": allProducts,
                "feedbacks": feedbacks,
                "oneProduct": oneProduct
            }

        except Exception as error:
            print(error)
            return jsonify({
                "error": error
            })
        
        finally:
            if client:
                client.close()

