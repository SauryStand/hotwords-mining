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

def create_pos_file(path):
    reload(sys)
    sys.setdefaultencoding('utf8')
    print 'read data from', path
    temp_file_path = '../t.txt'
    with codecs.open(path, "r", "utf-8") as f:
        with codecs.open(temp_file_path, 'w+', "utf-8") as fw:
            data = f.readlines()
            for line in data:
                line = line.strip().split('\t')
                fw.write(line[-1] + '\n')

    cmd = ['java', '-jar', './ark-tweet-nlp-0.3.2.jar', '--no-confidence', temp_file_path]
    stdin = subprocess.PIPE
    stdout = subprocess.PIPE
    stderr = subprocess.PIPE
    p = subprocess.Popen(cmd, stdin=stdin, stdout=stdout, stderr=stderr)
    (stdout, stderr) = p.communicate()

    result = stdout.split('\r\n')
    with codecs.open(path + "_pos", "w+", "utf-8") as f:
        for i, line in enumerate(data):
            line = line.strip().split('\t')
            t = result[i].split('\t')
            tweet = t[0]
            pos = t[1]
            tags = line[2]
            f.write(tags + '\t' + tweet + '\t' + pos + '\n')