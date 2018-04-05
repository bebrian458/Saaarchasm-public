from flask import Flask, render_template, request, jsonify
from evaluate import tweetscore
import evaluate
import emoticonTranslator
from text2speech import synthesize_text_file

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        phrase = request.form['phrase']
        score = tweetscore(phrase)
        score = (score+1)/2*100
        score = float("{0:.2f}".format(score))

        isSarcastic = (score > 50)
        if isSarcastic:
            print("Yep sarcastic.")

        newAudio = synthesize_text_file(phrase,isSarcastic)
        print(newAudio)
        results = {"score": str(score), "newAudio":str(newAudio)}
        return jsonify(results)
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug = True)
