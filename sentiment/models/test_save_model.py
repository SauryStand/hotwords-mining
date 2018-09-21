

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