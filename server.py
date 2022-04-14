from logging import exception
from flask import Flask, send_from_directory, request, jsonify
import random
import pymongo
import json

app = Flask(__name__)

# Path for our main Svelte page
@app.route("/")
def base():

    initPageConfiguration = open("Client/public/initPageConfiguration.json")
    data = json.load(initPageConfiguration)

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myclient["cms"]
    db_collection_users = db["users"]    
    db_collection_pageConfiguration = db["pageConfiguration"]

    try:
        db_collection_users.insert_one({ "_id": "admin", "password": "admin", "permission": "admin"})
    except Exception as exception:
        print("Admin already exists")

    try:
        db_collection_pageConfiguration.insert_one({"_id": "pageConfigurationSettings", "configuration": data})
    except Exception as exception:
        print("Page configuration is already set")


    return send_from_directory('Client/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('Client/public', path)

@app.route("/rand")
def hello():
    return str(random.randint(0, 100))


#dfddddddddddddd

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    print(data)

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myclient["cms"]
    db_collection_users = db["users"]

    userObject = { "_id": data["email"], "password": data["password"], "permission": data["permission"] }


    try:
        x = db_collection_users.insert_one(userObject)
        print(x.inserted_id)
        return jsonify({
            'email': data["email"],
            'password': data["password"],
            'permission': data["permission"]
        })
    except Exception as exception:
        #assert type(exception).__name__ == 'NameError'
        return jsonify({
            'errorMessage': "This email is actually used"
        })


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myclient["cms"]
    db_collection_users = db["users"]

    x = db_collection_users.find_one({ "_id": data["email"], "password": data["password"]})

    print(x)

    if x != None:
        return jsonify({
            'email': x["_id"],
            'password': x["password"],
            'permission': x["permission"]
        })
    else:
        return jsonify({
            'errorMessage': "Wrong password or email"
        })

"""
TODO Connect MongoDB
Handle users
Save configuration as one big JSON
Figure out how to use GridFS to save images and what format of files you will need
"""

@app.route("/saveConfiguration", methods=["POST"])
def saveConfiguration():
    data = request.get_json()

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myclient["cms"]
    db_collection_pageConfiguration = db["pageConfiguration"]

    try:
        db_collection_pageConfiguration.update_one({"_id": "pageConfigurationSettings"}, {"configuration": data})
    except Exception as exception:
        print("Page configuration is already set")

    try:
        db_collection_pageConfiguration.insert_one(data)
        return jsonify({
            'message': "Configuration is saved!"
        })
    except Exception as exception:
        #assert type(exception).__name__ == 'NameError'
        return jsonify({
            'errorMessage': "Cant save configuration"
        })

"""
TODO Send users
"""

"""
TODO Save configuration json
"""

"""
TODO Send configuration json
"""

#dziala czy nie
#TESTESTTEST
#asssssssfasfdssdaf
#kolejny testdd
#zzz
#dffffff

if __name__ == "__main__":
    app.run(debug=True)