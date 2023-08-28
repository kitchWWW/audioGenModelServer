from flask import Flask, request, jsonify
from flask_cors import CORS
import baseten
import truss
import base64
import os
# import doGen
import json

app = Flask(__name__)
CORS(app)

allIds=[]

@app.route('/audioGenServer/generate_audio', methods=['POST'])
def generate_audio():
    print("generate_audio")
    print(request.json)
    recieved = request.json
    prompt = recieved['content']
    dur = recieved['dur']
    idToUse = recieved['timestamp']

    print("going!")
    # doGen.doGen(recieved)
    fd = open("todoList.txt","a")
    fd.write(json.dumps(recieved)+"\n")

    allIds.append(idToUse)
    return jsonify({"id":idToUse})

@app.route('/audioGenServer/get_all_ids', methods=['GET'])
def get_all_ids():
    print("get_all_ids")
    return jsonify(allIds)

if __name__ == '__main__':
    app.run(host="localhost", port=3006, debug=True)