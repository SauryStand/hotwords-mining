# -*- coding:utf-8 -*-

import codecs
import subprocess
import sys


def create_pos_file(path):
    reload(sys)
    sys.setdefaultencoding('utf8')
    print('read data from', path)
    temp_file_path = '../t.txt'
    with codecs.open(path, "r", "utf-8") as f:
        with codecs.open(temp_file_path,'w+','utf-8') as fw:
            data = f.readline()
            for line in data:
                line = line.strip().split('\t')
                fw.write(line[-1] + '\n')

    cmd = ['java', '-jar', './ark-tweet-nlp-0.3.2.jar', '--no-confidence', temp_file_path]
    stdin = subprocess.PIPE
    stdout = subprocess.PIPE
    stderr = subprocess.PIPE
    p = subprocess.Popen(cmd,stdin=stdin,stdout=stdout,stderr=stderr)
    (stdout,stderr) = p.communicate()
    result = stdout.split('\r\n')
    with codecs.open(path + "_pos","w+","utf-8") as f:
        for i,line in enumerate(data):
            line = line.strip().split('\t')
            t = result[i].split('\t')
            tweet = t[0]
            pos = t[1]
            tags = line[2]
            f.write(tags + '\t' + tweet + '\t' + pos + '\n')
