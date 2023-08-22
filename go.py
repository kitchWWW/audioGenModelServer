import baseten
import truss
import base64

# audiogen_truss = truss.load('.')
# baseten.deploy(audiogen_truss)

print("going!")
model = baseten.deployed_model_id('ZBAgWGP')
model_output = model.predict({'prompts': ['wet smack', 'very wet kissing sounds', 'footsteps in a corridor'], 'duration': 8})
print("gone!")

for idx, clip in enumerate(model_output["data"]):
  with open(f"clip_{idx}.wav", "wb") as f:
    print("Writing!")
    f.write(base64.b64decode(clip))


