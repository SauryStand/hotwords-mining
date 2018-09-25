# -*- coding:utf-8 -*-


from scipy.sparse import csr_matrix

class SentimentJudge(object):
    """
        Simple example:
            s = SentimentJudge()
            test_data = s.transform(_test_data)
            predicted = s.predict(test_data)
            print np.sum(predicted == _test_target), len(_test_target), np.mean(predicted == _test_target)
    """
    __metaclass__ = Singleton




def main():
    clf = SentimentJudge()







if __name__ == '__main__':
    main()