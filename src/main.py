from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
import pymongo
import json

with open('config.json')as file:
     params = json.load(file)['params']

app = __name__()
run_with_ngrok(app)

@app.route("/", methods = ["POST"])
def handle_home():
    return "OK", 200

# Get the MongoDB client URL
client = pymongo.MongoClient(params["client_url"])

# Connect to your database
db = client[params["DB"]]

@app.route("/webhook", methods = ["POST", "GET"])
def dialogflow_mongo_DB():
    req = request.get_json(force = True)
    user_query = req["queryResult"]["queryText"]
    parameters = req["queryResult"]["parameters"]
    card_type = parameters.get["cardtype"]
    card_brand = parameters.get["cardbrand"]
    card_number = parameters.get["cardnumber"]
    card_expiry_date = parameters.get["cardexpirydate"] 
    cvv = parameters.get["CVV"]
    given_name = parameters.get["givenname"]
    Last_name = parameters.get["lastname"]
    data = { "user_query": user_query,
              "cardtype" : card_type,
              "cardbrand" : card_brand,
              "cardnumber" : card_number,
              "cardexpirydate" : card_expiry_date,
              "cvv" : cvv,
              "givenname" : given_name,
              "lastname" : Last_name         
    }

    col = db["Viranis-Transient-Business"]
    col.insert_one(data)
    print("Data got inserted successfully")
    
    return response(status = 200)



if __name__ == "__main__":
        app.run(debug = True)


