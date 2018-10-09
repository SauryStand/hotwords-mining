# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/5/6.
import inspect
from sklearn.externals import joblib
#from sentiment.models.tools.Lexicon import Ngrams

neg_words = {"never", "no", "nothing", "nowhere", "none", "none", "not", "haven't", "hasn't", "hadn't", "can't",
             "couldn't", "shouldn't", "won't", "wouldn't", "don't", "didn't", "isn't", "aren't", "ain't", "n't"}



class Ngrams(object):
    __metaclass__ = Singleton