import time
import os

def audioName(text):
    row = []
    name = ''
    ts = time.time()
    for word in text.split(" "):
        row.append(word)
    for word in row:
        name += word[0]
    name += '_' + str(ts).split('.')[0]
    name += '.mp3'
    return name

def clearAudio():
    dir_name = "static/audio/"
    oldFiles = os.listdir(dir_name)
    for item in oldFiles:
        if item.endswith(".mp3"):
            os.remove(os.path.join(dir_name, item))