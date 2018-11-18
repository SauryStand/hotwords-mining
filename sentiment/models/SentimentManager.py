# -*- coding:utf-8 -*-
import numpy as np
from sentiment.models.SentimentJudge import SentimentJudge

def get_result_info(predicted, target, tweets, total_tweet, return_sample_tweets_nums):
    """
    :param predicted:
    :param target:
    :param tweets: np.array  [str,str]
    :param total_tweet:
    :param return_sample_tweets_nums:
    :return:
    """
    c = predicted == target