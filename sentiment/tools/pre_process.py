import codecs
import re
from collections import Counter
import sys
import subprocess
from scipy.sparse import csr_matrix

def pos_process(data):
    # TODO use tempfile module
    temp_file_path = './t.txt'
    with codecs.open(temp_file_path, 'w+', "utf-8") as fw:
        for line in data:
            line = line.strip().split('\t')
            fw.write(line[-1].replace('\n', ' ').replace('\r', ' ') + '\n')

    cmd = ['java', '-jar', 'sentiment/models/tools/ark-tweet-nlp-0.3.2.jar', '--no-confidence', temp_file_path]

    stdout = subprocess.check_output(cmd, stderr=subprocess.STDOUT)

    # stdin = subprocess.PIPE
    # stdout = subprocess.PIPE
    # stderr = subprocess.PIPE
    # p = subprocess.Popen(cmd, stdin=stdin, stdout=stdout, stderr=stderr)
    # (stdout, stderr) = p.communicate()
    # print stderr

    result = stdout.split('\r\n')
    tweets, pos_tags = [], []
    for i in xrange(len(result)):
        t = result[i].split('\t')
        if t and len(t) > 1:
            tweets.append(t[0])
            pos_tags.append(t[1])
    return tweets, pos_tags

'''
Regular expression
'''
def remove_useless_info(words, pos_tag):
    # 删除非英文单词、URL、用户提及
    temp = zip(words, pos_tag)
    temp = filter(lambda x: re.match(r'([a-zA-z0-9 \+\?\.\*\^\$\(\)\[\]\{\}\|\\/:;\'\"><,#@!~`%&-_=])+$', x[0]), temp)
    temp = filter(lambda x: x[1] != 'U' and x[1] != '@' and not x[0].startswith('@'), temp)
    words = [t[0] for t in temp]
    pos_tag = [t[1] for t in temp]
    return words, pos_tag