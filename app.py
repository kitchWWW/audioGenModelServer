from flask import Flask, request, jsonify
from flask_cors import CORS
import baseten
import truss
import base64
import os

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
    model = baseten.deployed_model_id('ZBAgWGP')
    model_output = model.predict({'prompts': [prompt], 'duration': dur})
    print("done!")

    for idx, clip in enumerate(model_output["data"]):
      with open(f"clips/clip_{idToUse}.wav", "wb") as f:
        print("Writing!")
        f.write(base64.b64decode(clip))
        #hopefully we only get here once!
    
    # now we have to like fucking do the shit and upload to aws
    os.system('python uploader.py ./clips/clip_'+str(idToUse)+'.wav '+str(idToUse)+'.wav')
    allIds.append(idToUse)
    return jsonify({"id":idToUse})

@app.route('/audioGenServer/get_all_ids', methods=['GET'])
def get_all_ids():
    print("get_all_ids")
    return jsonify(allIds)

if __name__ == '__main__':
    app.run(host="localhost", port=3006, debug=True)