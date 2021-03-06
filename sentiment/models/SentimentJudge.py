# -*- coding:utf-8 -*-


from scipy.sparse import csr_matrix
from sklearn import metrics
from sklearn.externals import joblib

class SentimentJudge(object):
    """
        Simple example:
            s = SentimentJudge()
            test_data = s.transform(_test_data)
            predicted = s.predict(test_data)
            print np.sum(predicted == _test_target), len(_test_target), np.mean(predicted == _test_target)
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.classifier = joblib.load('sentiment/models/models_save/classifier')
        self.ngram = joblib.load('sentiment/models/models_save/ngrams')
        self.lexicon = joblib.load('sentiment/models/models_save/lexicon')

    def predict(self, X):
        """
            Predict X is positive or negative
        :param X:
        :return: a numpy.ndarray. each row with "positive" or "negative"
        """
        return self.classifier.predict(X)


def main():

    clf = SentimentJudge()
    tweets, target = [], []
    with codecs.open('./data/test/2014-test-journal.tsv', "r", "utf-8") as f:
        for line in f.readlines():
            line = line.strip().split("\t")
            target.append(line[1])
            tweets.append(line[2])

    test_feature = clf.transform(tweets)
    predicted = clf.predict(test_feature)







if __name__ == '__main__':
    main()