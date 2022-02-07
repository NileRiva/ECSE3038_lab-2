from flask import Flask, request, jsonify
from datetime import datetime
app = Flask(__name__)



def currdatetime():
    dt=datetime.now()
    currdatetimestr= dt.strftime("%d/%m/%Y, %H:%M:%S")
    return currdatetimestr

FAKEPROFDB = {} 
FAKETANKDB = [] 
id_count = 0
profcount = 0
#CRUD

#CREATE PROFILE
@app.route("/profile", methods=["POST"])
def postprofile():
    username = request.json["username"]
    role = request.json["role"]
    color = request.json["color"] 
    user_profile = {
        "data":{
            "role": role,
            "color": color,
            "username": username,
            "last_updated": currdatetime(),
        },   
    }
    global FAKEPROFDB   
    #global profcount 
    #profcount+=1
    FAKEPROFDB = user_profile #cannot use .append() on dictionary 
    #FAKEPROFDB.update(user_profile: profcount)
    return jsonify(FAKEPROFDB)

#CREATE TANK DATA
@app.route("/data",methods=["POST"])
def posttankdata():
    location = request.json["location"]
    lat = request.json["lat"]
    long = request.json["long"]
    percenatge_full = request.json["percentage_full"]
    global id_count
    id_count+=1
    tank_data = {
        "id": id_count,
        "location":location,
        "lat": lat,
        "long":long,
        "percentage_full":percenatge_full,
        }
    global FAKETANKDB

    FAKETANKDB.append(tank_data) 
    return jsonify(FAKETANKDB) 

#READ PROFILE
@app.route("/profile",methods = ["GET"])
def getprofiles():
    return jsonify(FAKEPROFDB)

#READ DATA
@app.route("/data",methods = ["GET"])
def gettankdata():
    return jsonify(FAKETANKDB)

#UPDATE PROFILE 
@app.route("/profile",methods = ["PATCH"])
def patchprofile():
    if "username" in  request.json:
        FAKEPROFDB["data"]["username"] = request.json["username"]
        FAKEPROFDB["data"]["last_updated"] = currdatetime()
    if "color" in request.json:
        FAKEPROFDB["data"]["color"] = request.json["color"]
        FAKEPROFDB["data"]["last_updated"] = currdatetime()
    if  "role" in request.json:
        FAKEPROFDB["data"]["role"] = request.json["role"]
        FAKEPROFDB["data"]["last_updated"] = currdatetime()    
    return jsonify(FAKEPROFDB)

#UPDATE TANK DATA
@app.route("/data/<int:id>",methods = ["PATCH"])
def patchtankdata(id):
    for tank in FAKETANKDB: 
        if tank ["id"] == id:
            if "location" in request.json:
                tank["location"] = request.json["location"]
            if "lat" in request.json:
                tank["lat"] = request.json["lat"]   
            if "long" in request.json:              
                tank["long"] = request.json["long"] 
            if "percentage_full" in request.json:
                tank["percentage_full"] = request.json["percentage_full"]
    for tank in FAKETANKDB: 
        if tank ["id"] == id:
            return jsonify(tank)

#DELETE TANK  DATA
@app.route("/data/<int:id>",methods = ["DELETE"])
def deletetank(id):
    
        for tank_id in FAKETANKDB: 
            if tank_id["id"] == id:
                FAKETANKDB.remove(tank_id) 
        return {
            "success": True
        }

if __name__ == '__main__':
    app.run(
    debug=True, 
    port=3000,
    host="0.0.0.0") 
