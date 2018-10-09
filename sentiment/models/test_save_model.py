from sklearn import metrics
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression

def get_features(data, postags):
    """
    :param data: [str,str..]
    :param id2word: dict  word_id:word
    :param vocabulary: dict  word:word_id
    :return:
    """
    print 'create features...'
    data_feature = pre_process(data, postags)  # 这里data 每一行已经分词了
    print data_feature.shape
    return data_feature


def main():
    train_data, train_target, train_pos = read_train_data('2013')
    train_feature = get_features(train_data, train_pos)

    clf = LogisticRegression(C=0.01105)
    clf.fit(train_feature, train_target)


    ngram = Ngrams()
    lexicon = Lexicon()
    joblib.dump(clf, 'models_save/classifier')
    joblib.dump(ngram, 'models_save/ngrams')
    joblib.dump(lexicon, 'models_save/lexicon')

    for name, test_data, test_target, test_pos in read_all_test_data():
        #todo
        print '\n\n\n\n\n--------Now is {} --------\n\n'.format(name)
        test_feature = get_features(test_data, test_pos)
        predicted = clf.predict(test_feature)
        print "Classification report for  %s:\n%s\n" % (clf,
                                                        metrics)

if __name__ == '__main__':
    main()