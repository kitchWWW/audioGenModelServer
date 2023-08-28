import time
import json
import statistics
import sys
import baseten
import truss
import base64
import os


model = baseten.deployed_model_id('ZBAgWGP')

completedTasks = []


while True:
    allTodos = open("todoList.txt").readlines()
    newList = list(set(allTodos) - set(completedTasks))
    print(newList)
    if(len(newList) == 0):
        time.sleep(1)
        continue

    prompts = []
    durs = []
    ids = []
    for data in newList:
        dat = json.loads(data)
        prompts.append(dat['content'])
        durs.append(int(dat['dur']))
        ids.append(dat['timestamp'])
        completedTasks.append(data)

    continue
    model_output = model.predict({'prompts': prompts, 'duration': statistics.mean(durs)})
    print("done!")

    for idx, clip in enumerate(model_output["data"]):
        idToUse = ids[idx]
        with open(f"clips/clip_{idToUse}.wav", "wb") as f:
            print("Writing!")
            f.write(base64.b64decode(clip))
            #hopefully we only get here once!
            os.system('python uploader.py ./clips/clip_'+str(idToUse)+'.wav '+str(idToUse)+'.wav')
