import random
import os
import baseten
import truss
import base64

# audiogen_truss = truss.load('.')
# baseten.deploy(audiogen_truss)

def doAndSay(com):
  print(com)
  os.system(com)



print("going!")
model = baseten.deployed_model_id('ZBAgWGP')
p = "wind"
model_output = model.predict({'prompts': [p,p,p,p,p,p,p,p,p], 'duration': 4 + (random.random()*3)})
print("gone!")

for idx, clip in enumerate(model_output["data"]):
  with open(f"clip_{idx}.wav", "wb") as f:
    print("Writing!")
    f.write(base64.b64decode(clip))
  doAndSay("sox clip_"+str(idx)+".wav o_clip_"+str(idx)+".wav fade .5 -0 .5")
