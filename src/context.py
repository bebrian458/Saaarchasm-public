#courtesy from MathieuCliche

""" This class is a wrapper around the gensim LDA topic modeler. """

from gensim import corpora, models, similarities
import numpy as np
import nltk
import emoticonTranslator
from nltk.corpus import stopwords



class Context(object):
                                    #alpha is some hyper-paramater
    def __init__(self,num_contexts=100,alpha=1,model=None,dicttp=None):
        
        self.numContexts = num_contexts
        self.porter = nltk.PorterStemmer()
        self.alpha = alpha
        self.stop = stopwords.words('english')+['.','!','?','"','...','\\',"''",'[',']','~',"'m","'s",';',':','..','$']
        if model != None and dicttp != None:
            self.lda = models.ldamodel.LdaModel.load(model)
            self.dictionary =  corpora.Dictionary.load(dicttp)

    def fit(self,documents):
        
        documents_mod = [emoticonTranslator.replace_reg(sentence) for sentence in documents]
        tokens = [nltk.word_tokenize(sentence) for sentence in documents_mod]
        tokens = [[self.porter.stem(t.lower()) for t in sentence if t.lower() not in self.stop] for sentence in tokens]        
            
        self.dictionary = corpora.Dictionary(tokens)
        corpus = [self.dictionary.doc2bow(text) for text in tokens]
        self.lda = models.ldamodel.LdaModel(corpus,id2word=self.dictionary, num_topics=self.numContexts,alpha=self.alpha)
        
        self.lda.save('context.tp')
        self.dictionary.save('contexts_dict.tp')
        
    def get_topic(self,context_number):
        
        return self.lda.print_topic(context_number)
    
    def transform(self,sentence):
        
        sentence_mod = emoticonTranslator.replace_reg(sentence)
        tokens = nltk.word_tokenize(sentence_mod)
        tokens = [self.porter.stem(t.lower()) for t in tokens if t.lower() not in self.stop] 
        corpus_sentence = self.dictionary.doc2bow(tokens)
        
        return self.lda[corpus_sentence]  