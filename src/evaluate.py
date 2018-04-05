""" This is the function which gets called by the button 'Test',
it takes a sentence and returns a percentage which describes how sarcastic
the input sentence is. """

import numpy as np
import pickle
#import _pickle as pickle
import os
import featureExtraction
import context
import nltk




fileObject1 = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'vectorDict.p'), 'rb')
fileObject2= open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'classifier84000.p'), 'rb')

#fileObject2 = open('/Users/silver/Desktop/michelle/Saaarchasm/clf84k.pkl', 'rb')

vec = pickle.load(fileObject1)


classifier = pickle.load(fileObject2)

#classifier = pickle.load(fileObject2) 

#classifier = pickle.load(fileObject2)



fileObject1.close()
fileObject2.close()

topic_mod = context.Context(model=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'context.tp'),\
                        dicttp=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'contexts_dict.tp'))

def tweetscore(sentence):
    
    features = featureExtraction.get_all_features(sentence,topic_mod)
    features_vec = vec.transform(features)
    score = classifier.decision_function(features_vec)[0]

    #print(score)
    #percentage = int(round(2.0*(1.0/(1.0+np.exp(-score))-0.5)*100.0))
    
    return score


#print(tweetscore("i love it when you hurt me so much that i just dont know what to do"))
#print(tweetscore("i love you"))
#print(tweetscore("i really love you"))

#print(tweetscore("Oh good job."))

#print(tweetscore("i like you"))

#print(tweetscore("birds can fly. i love you. i love that you hurt me"))

#print(tweetscore("i want to go home"))


#print(tweetscore("i hate him sooooo much"))

