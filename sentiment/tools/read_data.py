import codecs
import subprocess
import sys
from sentiment.models.tools.Lexicon import Ngrams

def read_data(path):
    """
        return tweets_list and tags_list  for given path
    :param path: the file path eg:    c:\\a.txt
    :return: tweets_list,tags_list
    """
    print 'read data from', path

    tweets, tags, pos = [], [], []
    with codecs.open(path + '_pos', "r", "utf-8") as f:
        for line in f.readlines():
            line = line.strip().split("\t")
            tags.append(line[0])
            tweets.append(line[1])
            pos.append(line[2])
    return tweets, tags, pos