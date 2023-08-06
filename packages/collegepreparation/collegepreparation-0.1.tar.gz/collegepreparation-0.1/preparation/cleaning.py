
import spacy
#spacy.load('en')
from spacy.lang.en import English
eng_parser = English()
import nltk 
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer 
import random
import pandas as pd
from os import listdir, path
import re
from collections import Counter
import collections
from nltk.stem.wordnet import WordNetLemmatizer
from gensim.utils import lemmatize as lmm
import pattern
import gensim
import string
from gensim import corpora
import joblib
from datetime import datetime as dt
import os, sys 
import pyLDAvis.gensim
from gensim.models import CoherenceModel 
import pandas as pd  

class cleaning_utility():
    def __init__(self, 
        is_nltk,
        strict=False, 
        stop_words=None, 
        url_commonwords=['index', 'com', 'edu', 'www','http', 'https', 'org', 'html', 'htm', 'php', 'aspx', 'asp'], 
        process_options={
        "en":True, #handle english
        "rmstop": True, #remove stopwords
        "repspecial": True, #replace special characters with white space
        "reptechset": False, #replace tech set with white space. & % $
        "reprepetitive":True, #replace repetitive (3+) with one myyyyyyyyyy name is Trump
        "rmfreq":False, #remove frequent words
        "lemma": True, #lemmatize allowed_tags=re.compile('(NN|VB|JJ|RB)')
        "gensim_url_tags": re.compile('(NN|VB)'),
        "gensim_content_tags":re.compile('(NN|VB|JJ|RB)'),
        "nltk_url_tags":  [wordnet.VERB,wordnet.NOUN],
        "nltk_content_tags":[wordnet.VERB,wordnet.NOUN,wordnet.ADV,wordnet.ADJ]}): # POS part of speech . NN, VB, JJ, 
        """  
        
        posed=nltk.pos_tag(sentence)   
            en: use english
            rmstop: remove stop words
            repsepcial: replace special code with white space
            reptechset: replace tech set with space. tech set: '^|!#$~&%.-_'
            rmfreq: remove frequent words >95%
            reprepetitive: replace repetive (3+) with one
            gensim_url_tags
            gensim_content_tags
            nltk_url_tags
            nltk_content_tags
            strict: if true, only take alphanumeric
        """
        self.is_nltk=is_nltk
        self.url_commonwords=url_commonwords
        self.strict=strict
        if stop_words==None:
            self.stop_words=set(stopwords.words("english"))
        else:
            self.stop_words=stop_words
        self.process_options=process_options
        
        self.tech_set='^|!#$~&%.-_'
        self.special_cha=str(set(string.punctuation)-set(self.tech_set))
        self.pure_text_set=string.printable[0:62]+'.-_'
        
        self.trans_full=str.maketrans(string.punctuation, ' '*len(string.punctuation))
        self.tran_nontech=str.maketrans(self.special_cha, ' '*len(self.special_cha))
        self.freq_words=[]
        self.strict=strict
        self.lm_nltk=WordNetLemmatizer()
        
    def clean_word(self, word):
        """
            clean a single string. this is the first staging of cleaning, only handles special characters. 
            handles both single word and sentence(s)
        """   
        if self.strict==False:
            if self.process_options['en']==True:
                word=''.join([c if ord(c)>=32 and ord(c)<127 else '' for c in word ]) 
            if self.process_options['repspecial']==True:
                word=word.translate(self.trans_full) 
            if self.process_options['reptechset']==True:
                word=word.translate(self.tran_nontech) 
            if self.process_options['reprepetitive']==True:
                word=re.sub(r'([a-zA-Z])\1{2,}', r'\1', word) 
                word=re.sub(r'(\W)\1+', r'\1', word)    
        else:  
            word=re.sub(r'\s+', ' ',re.sub(r'[^A-Za-z0-9 ]+', ' ', word)) 
        return word
    
    def parse_sentence(self, sentence, return_type='list' ):
        """
            sentence: a string. 
            return type: sentence, list 
        """ 
        sentence=self.pre_process(sentence)   
        sentence=self.clean_word(sentence)  
        if self.process_options['lemma']==True:
            sentence=self.lemmatize_sentence(sentence, return_type='sentence', is_url=False) 
        if self.process_options['rmstop']==True:
            words=[w for w in sentence.split(' ') if w not in self.stop_words] 
        return words if return_type=='list' else ' '.join(words) 

    def parse_url(self, url, return_type='list'):
        """
            this is to parse url only. 
            url: take only alphanumeric and space
        """
        url=re.sub(r'\s+', ' ',re.sub(r'[^A-Za-z0-9 ]+', ' ', url))
        
        url=self.parse_sentence(url,return_type=return_type)
        
        if self.process_options['lemma']:
            if self.is_nltk==False:
                words=self.lemmatize_sentence(url, return_type='list', is_url=True)  
            else:  
                words=self.nltk_lemma_sentence(url, return_type='list', is_url=True)  
        else:
            words=url.split(' ')
        
        if self.process_options['rmstop']==True:
            words=[w for w in words if w not in self.stop_words]
                
        words=[w for w in words if w not in self.url_commonwords]
            
        return words if return_type=='list' else ' '.join(words) 
    
    
    def pre_process(self, text):
        """
            preprocess: replace URL with _url_ and twitter @someone with _twitterName_
        """
        trunks=text.split(' ')         
        new_trunk =[]
       
        for t in trunks:
            if re.match(r'.?http?:.+', t):
                 new_trunk.append('url')
            elif t.startswith('@'):
                new_trunk.append('twitterName')
            else:
                new_trunk.append(t) 
        return ' '.join(new_trunk) 
     
    ##################################################### lemmatize ################################################# 
    def lemmatize_sentence(self, sentence, return_type='list',is_url=False): #sentence: a string: they are coming to build 
        """
            sentence: e.g.: a quick brown fox jumps over lazy dog
            return_type: sentence or list
        """
        if not sentence:
            return
        if isinstance(sentence, list)==True: 
            sentence=' '.join([s for s in sentence]) 
        if self.is_nltk==False:  
            if is_url==True:
                out_text=lmm(sentence, allowed_tags=self.process_options['gensim_url_tags']) 
            else:
                out_text=lmm(sentence, allowed_tags=self.process_options['gensim_content_tags']) 
            if return_type=='sentence': 
                return ' '.join([t.decode('utf-8').split('/')[0] for t in out_text])  
            else:
                return [t.decode('utf-8').split('/')[0] for t in out_text] 
        else: #is_nltk ==True 
            return self.nltk_lemma_sentence(sentence, return_type=return_type, is_url=is_url)            
            
    ##################################################### NLTK Lemmatizer ################################################# 
    def nltk_get_wordnet_pos(self,pos):
        """
            return WORDNET POS compliance to WORDENT lemmatization (a,n,r,v). n, v 
        """
        if pos.startswith('J'):
            return wordnet.ADJ
        elif pos.startswith('V'):
            return wordnet.VERB
        elif pos.startswith('PR'):
            return wordnet.NOUN
        elif pos.startswith('N'):
            return wordnet.NOUN
        elif pos.startswith('R'):
            return wordnet.ADV
        else:# default pos in lemmatization is Noun
            return wordnet.ADJ

    def nltk_lemma_sentence(self, sentence, return_type='list', is_url=False): #tokens=['they','are', 'is', 'better', 'not', 'to', 'got', 'killed']
        """
            return_type: list. sentence
        """    
        if isinstance(sentence, str)==True:
            sentence=sentence.split()
          
        if is_url==True:
            words=[self.lm_nltk.lemmatize(p[0], self.nltk_get_wordnet_pos(p[1])) 
                         for p in posed if self.nltk_get_wordnet_pos(p[1]) in (self.process_options['nltk_url_tags'])]
        else: 
            words=[self.lm_nltk.lemmatize(p[0], self.nltk_get_wordnet_pos(p[1])) 
                         for p in posed if self.nltk_get_wordnet_pos(p[1]) in (self.process_options['nltk_content_tags'])]

        if return_type=='sentence':
            return ' '.join(words)
        return words 

