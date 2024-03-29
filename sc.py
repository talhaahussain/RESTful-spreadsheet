from flask import Flask, request
import os
import json
import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument("-r")
args = parser.parse_args()

if args.r == "sqlite" or args.r == "Sqlite":
    print("You are using an Sqlite database to store data.\n")
    import sqlite_backend as store
    cursor = store.create_table()
    store_mode = 0
elif args.r == "firebase" or args.r == "Firebase":
    print("You are using a Firebase Realtime Database to store data.\n")
    import firebase_backend as store
    try:
        FBASE = os.environ["FBASE"]
    except KeyError:
        print("Error - no environment variable defined for Firebase.\n")
        print("Please use: 'export FBASE=<database_name>' to read database name from environment variable.\n")
        exit(1)
    else:
        FBASE_URL = "https://" + FBASE + "-default-rtdb.europe-west1.firebasedatabase.app"
        store_mode = 1
else:
    print("Invalid argument. Please try again.\n")
    print("(Hint - Try run the program with \"-r sqlite\" or \"-r firebase\".)\n")
    exit(1)

app = Flask(__name__)

##################################
######### Flask methods ##########
##################################

@app.route("/cells/<string:id>", methods=["PUT"])
def create(id):
    if store_mode == 0:
        js = request.get_json()
        cid = js.get("id")
        cformula = js.get("formula")

        if cid != id or cid == None or cformula == None:
            return "", 400 # Bad Request
    
        cformula = store.eval_cformula(cformula, cursor)
    
        if id not in store.list_all(cursor):
            cell = store.create(cid, cformula, cursor)
            if cell != None:
                return "", 201 # Created
            else:
                return "", 500 # Internal Server Error
        else:
            cell = store.create(cid, cformula, cursor)
            if cell != None:
                return "", 204 # No Content
            else:
                return "", 500 # Internal Server Error

    elif store_mode == 1:
        js = request.get_json()
        cid = js.get("id")
        cformula = js.get("formula")

        if cid != id or cid == None or cformula == None:
            return "", 400 # Bad Request

        cformula = store.eval_cformula(cformula, FBASE_URL)
        js["formula"] = cformula
        js = json.dumps(js)
    
        if id not in store.list_all(FBASE_URL):
            r = store.create(id, js, FBASE_URL)
            if r.status_code == 200:
                return "", 201 # Created
            else:
                return "", 500 # Internal Server Error
        else:
            r = store.create(id, js, FBASE_URL)
            if r.status_code == 200:
                return "", 204 # No Content
            else:
                return "", 500 # Internal Server Error


@app.route("/cells/<string:id>", methods=["GET"])
def read(id):
    if store_mode == 0:
        if id not in store.list_all(cursor):
            return "", 404 # Not Found
        
        cell = store.read(id, cursor)
        if cell == None:
            return "", 500 # Interal Server Error

        answer = "{\"id\":\"" + str(cell.cid) + "\", \"formula\":\"" + str(cell.cformula) + "\"}"
        if answer != None:
            return answer, 200 # OK
        else:
            return "", 500 # Internal Server Error
    

    elif store_mode == 1:
        if id not in store.list_all(FBASE_URL):
            return "", 404 # Not Found
        
        cell = store.read(id, FBASE_URL)
        if cell == None:
            return "", 500 # Internal Server Error

        answer = "{\"id\":\"" + str(cell["id"]) + "\", \"formula\":\"" + str(cell["formula"]) + "\"}"
        if answer != None:
            return answer, 200 # OK
        else:
            return "", 500 # Internal Server Error
 

@app.route("/cells/<string:id>", methods=["DELETE"])
def delete(id):
    if store_mode == 0:
        if id not in store.list_all(cursor):
            return "", 404 # Not Found
        if store.delete(id, cursor) == True:
            return "", 204 # No Content
        else:
            return "", 500 # Internal Server Error
    
    elif store_mode == 1:
        if id not in store.list_all(FBASE_URL):
            return "", 404 # Not Found
        response = store.delete(id, FBASE_URL)
        if response.status_code == 200:
            return "", 204 # No Content
        else:
            return "", 500 # Internal Server Error


@app.route("/cells", methods=["GET"])
def list():
    if store_mode == 0:
        ids = store.list_all(cursor)
        if ids != None:
            return str(ids), 200 # OK
        else:
            return "", 500 # Internal Server Error
    
    elif store_mode == 1:
        ids = store.list_all(FBASE_URL)
        if ids != None:
            return str(ids), 200 # OK
        else:
            return "", 500 # Internal Server Error

if __name__ == "__main__":
    app.run(host="localhost", port=3000)
