import random
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

def doAndSay(com):
    print(com)
    os.system(com)

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

    print("going!")
    model_output = model.predict({'prompts': prompts, 'duration': statistics.mean(durs)})
    print("done!")

    for idx, clip in enumerate(model_output["data"]):
        idToUse = ids[idx]
        with open(f"clips/clip_{idToUse}.wav", "wb") as f:
            print("Writing!")
            f.write(base64.b64decode(clip))
            if False:
                doAndSay('sox ./clips/clip_'+str(idToUse)+'.wav  ./clips/clip_'+str(idToUse)+'_z.wav  fade t .5 -0 .5 pad 0 '+str((1 + (random.random() * 5))))
            else:
                f.close()
                import numpy as np
                from scipy.io import wavfile
                # Load the wav file
                sample_rate, data = wavfile.read(f"clips/clip_{idToUse}.wav")
                # Convert data to float64 for processing
                data = data.astype(np.float64)
                # Extract the last one second of the audio
                num_samples_for_fade = sample_rate * 1
                last_second = data[-num_samples_for_fade:].copy()
                fade_out = np.linspace(1, 0, num_samples_for_fade)
                fade_in = np.linspace(0, 1, num_samples_for_fade)
                data[:num_samples_for_fade] *= fade_in
                last_second *= fade_out
                trimmed_data = data[:-num_samples_for_fade]
                data = trimmed_data
                data[:num_samples_for_fade] += last_second
                # Save the modified audio
                wavfile.write('./clips/clip_'+str(idToUse)+'_z.wav', sample_rate, data.astype(np.int16))

            doAndSay('python uploader.py ./clips/clip_'+str(idToUse)+'_z.wav '+str(idToUse)+'.wav')
            doAndSay('rm ./clips/clip_'+str(idToUse)+'.wav')
            doAndSay('rm ./clips/clip_'+str(idToUse)+'_z.wav')



