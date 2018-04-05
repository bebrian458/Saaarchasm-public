from flask import Flask, render_template, request, jsonify
import src.evaluate
import src.emoticonTranslator
from src.evaluate import tweetscore
from src.text2speech import synthesize_text_file
from src.audio import audioName, clearAudio
import os

app = Flask(__name__)
oldAudio = 'test'

@app.route('/', methods=['POST', 'GET'])
def result():
    global oldAudio
    if request.method == 'POST':
        phrase = request.form['phrase']        
        newAudio = audioName(str(phrase))
        newAudio = 'static/audio/' + newAudio
        score = tweetscore(phrase)
        score = (score+1)/2*100
        score = float("{0:.2f}".format(score))

        isSarcastic = (score > 50)
        if isSarcastic:
            print("Yep sarcastic.")

        newAudio = synthesize_text_file(phrase, newAudio, isSarcastic)
        print 'oldAudio: ' + oldAudio 
        if os.path.exists(oldAudio):
            print 'deleting ' + oldAudio
            os.remove(oldAudio)
        oldAudio = newAudio
        print 'new OldAudio: ' + oldAudio

        results = {"score": str(score), "newAudio":str(newAudio), "oldAudio": oldAudio}
        return jsonify(results)
    return render_template("index.html")

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

if __name__ == '__main__':
    clearAudio()
    app.run(debug = True)
