""" The main function in this file, i.e. 'dialogue_act_features', takes a tweet and a topic modeler and returns
a dictionnary of features.  The feature extraction is composed of unigrams and bigrams,
a sentiment analysis, a part of speech counter, a capicalization counter and a topic vector."""

import nltk
import numpy as np
import string
from textblob import TextBlob
import emoticonTranslator

print('Loading files')
porter = nltk.PorterStemmer()
#sentiments = load_sent.load_sent_word_net()

def get_all_features(sentence,topic_modeler):
        
    features = {} #a dictionary of feature to how much it weighs
    
    grams_feature(features,sentence)
    sent_feature(features,sentence)
    pos_feature(features,sentence)
    cap_feature(features,sentence) #i LOVE basketball
    topic_feature(features,sentence,topic_modeler)
    
    return features
    
def grams_feature(features,sentence):
    normalized_sentence = emoticonTranslator.replace_reg(sentence)
    
    #Spell check
    #sentence_reg = TextBlob(sentence_reg)
    #sentence_reg = str(sentence_reg.correct())
    
    #super clean tokens to make unigrams and bigrams out of
    tokens = nltk.word_tokenize(normalized_sentence)
    tokens = [porter.stem(t.lower()) for t in tokens] #every element looks like ['i','feel','super','safe','here']
    bigrams = nltk.bigrams(tokens) # "generator object bigrams"

    bigrams = [tup[0]+' ' + tup[1] for tup in bigrams] #every element looks like ['i love', 'love it', 'it when'...]
    grams = tokens + bigrams #unigrams + bigrams
    for t in grams:
        features['contains(%s)' % t] = 1.0 #every unigram and bigram get to initially have equal weight
        
def sent_feature(features,sentence):
   
    sentence_sentiment = emoticonTranslator.replace_emo(sentence)
    tokens = nltk.word_tokenize(sentence_sentiment)
    tokens = [(t.lower()) for t in tokens] 
    
    
    #TextBlob sentiment analysis is free! polarity scores go from [-1,1] where -1 is negative sent and 1 is positive sent
    #subjectivity goes from [0,1] where 0 is objective and 1 is subjective
    try:
        blob = TextBlob("".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in tokens]).strip())
        features['Blob sentiment'] = blob.sentiment.polarity
        features['Blob subjectivity'] = blob.sentiment.subjectivity
    except:
        features['Blob sentiment'] = 0.0
        features['Blob subjectivity'] = 0.0
    
    #assumption that sarcasm has the feature of has polar sentiment across a string of words (e.g. a sentence)
    if len(tokens) == 1:
        tokens += ['.'] #just to ensure there is a second half
    f_half = tokens[0:len(tokens)/2]
    s_half = tokens[len(tokens)/2:]
    

     #TextBlob sentiment analysis
    try:
        blob = TextBlob("".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in f_half]).strip())
        
        features['Blob sentiment 1/2'] = blob.sentiment.polarity
        features['Blob subjectivity 1/2'] = blob.sentiment.subjectivity
    except:
        features['Blob sentiment 1/2'] = 0.0
        features['Blob subjectivity 1/2'] = 0.0
    try:
        blob = TextBlob("".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in s_half]).strip())
        features['Blob sentiment 2/2'] = blob.sentiment.polarity
        features['Blob subjectivity 2/2'] = blob.sentiment.subjectivity
    except:
        features['Blob sentiment 2/2'] = 0.0
        features['Blob subjectivity 2/2'] = 0.0
        
    #the variance/range of the two halves is decided to be a feature
    features['Blob Sentiment contrast 2'] = np.abs(features['Blob sentiment 1/2']-features['Blob sentiment 2/2'])

 

def pos_feature(features,sentence):
    
    sentence_pos = emoticonTranslator.replace_emo(sentence)
    tokens = nltk.word_tokenize(sentence_pos)
    tokens = [(t.lower()) for t in tokens] 

    pos_vector = nltk.pos_tag(tokens)
    vector = np.zeros(4)
    for j in range(len(tokens)):
            pos=pos_vector[j][1]
            if pos[0:2] == 'NN': #noun
                vector[0]+=1
            elif pos[0:2] == 'JJ': #adjective
                vector[1]+=1
            elif pos[0:2] == 'VB': #verb
                vector[2]+=1
            elif pos[0:2] == 'RB': #adverb
                vector[3]+=1

    pos_vector = vector
    for j in range(len(pos_vector)):
        features['POS' + str(j+1)] = pos_vector[j]
        
def cap_feature(features,sentence):
    counter = 0
    threshold = 5 #hyper-parameter of how many capital letters is considered "enough"
    for j in range(len(sentence)):
        counter += int(sentence[j].isupper())
    features['Capitalization'] = int(counter>=threshold)
    
def topic_feature(features,sentence,topic_modeler):
    
    topics = topic_modeler.transform(sentence)
    
    for j in range(len(topics)):
        features['Topic :' +str(topics[j][0])] = topics[j][1]
    
    