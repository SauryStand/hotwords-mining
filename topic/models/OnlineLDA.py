# -*- coding:utf-8 -*-
#copy from hrwhisper

import codecs
import datetime
from collections import Counter
import itertools

import math
import numpy as np
import pymongo
from scipy.special import gammaln, psi
from Corpus import Corpus

def float_2_decimals(x):
    return int(x * 100 + 0.05) / 100.


def chunkize_serial(iterable, chunksize, as_numpy=True):
    """
    Return elements from the iterable in `chunksize`-ed lists. The last returned
    element may be smaller (if length of collection is not divisible by `chunksize`).

    chunkize_serial(range(10), 3)
        => [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """
    it = iter(iterable)
    while True:
        # convert each document to a 2d numpy array (~6x faster when transmitting
        # chunk data over the wire, in Pyro)
        if as_numpy:
            wrapped_chunk = [[np.array(doc) for doc in itertools.islice(it, int(chunksize))]]
        else:
            wrapped_chunk = [list(itertools.islice(it, int(chunksize)))]
        if not wrapped_chunk[0]: break
        # memory opt: wrap the chunk and then pop(), to avoid leaving behind a dangling reference
        yield wrapped_chunk.pop()


class OnlineLDA(object):
    """
    Implements online VB for LDA as described in (Hoffman et al. 2010).
    Base on Gensim and Hoffman's code.
    """
    # paran
    def __init__(self, corpus, K=10, C=0.5, tau0=1.0, kappa=0.5, iterations=50, passes=1,
                 gamma_threshold=0.001, chunk_size=3000):
        """
        Arguments:
        corpus: Corpus object. Saving tweets and words.
        K: Number of topics
        C: contribute factor
        tau0: A (positive) learning parameter that downweights early iterations
        kappa: Learning rate: exponential decay rate---should be between
             (0.5, 1.0] to guarantee asymptotic convergence.

        iteration:  inference maximum iteration number
        chunk_size: the size of chunk
        """
        self.corpus = corpus
        self._K = K
        self._W = len(self.corpus.vocab)
        self._D = len(corpus)
        self._alpha = 1.0 / self._K  # np.asarray([1.0 / self._K for _ in xrange(self._K)])  # 1.0 / K  #
        self._eta = 1.0 / self._K  # np.asarray([1.0 / self._K for _ in xrange(self._K)]).reshape((self._K, 1))
        self._C = C
        self._tau0 = tau0 + 1
        self._kappa = kappa
        self._updatect = 0
        self.gamma_threshold = gamma_threshold

        # Initialize the variational distribution q(beta|lambda)
        self._lambda = 1 * np.random.gamma(100., 1. / 100., (self._K, self._W))
        self._Elogbeta = dirichlet_expectation(self._lambda)
        self._expElogbeta = np.exp(self._Elogbeta)
        self.gamma = None

        self.iterations = iterations
        self.chunk_size = chunk_size
        self.passes = passes

        self.update()


    def inference(self, chunk):
        """
        Given a mini-batch of documents, estimates the parameters
        gamma controlling the variational distribution over the topic
        weights for each document in the mini-batch.

        Arguments:
        chunk:  List of documents. Each document must be represented
               as a string. (Word order is unimportant.) Any
               words not in the vocabulary will be ignored.

        Returns a tuple containing the estimated values of gamma,
        as well as sufficient statistics needed to update lambda.
        """
        # This is to handle the case where someone just hands us a single
        # document, not in a list.
        batchD = len(chunk)

        # Initialize the variational distribution q(theta|gamma) for
        # the mini-batch
        gamma = 1 * np.random.gamma(100., 1. / 100., (batchD, self._K))
        Elogtheta = dirichlet_expectation(gamma)
        expElogtheta = np.exp(Elogtheta)

        sstats = np.zeros(self._lambda.shape)
        # Now, for each document d update that document's gamma and phi
        for d, doc in enumerate(chunk):
            # These are mostly just shorthand (but might help cache locality)
            ids = [id for id, _ in doc]
            cts = np.array([cnt for _, cnt in doc])
            gammad = gamma[d, :]
            expElogthetad = expElogtheta[d, :]
            expElogbetad = self._expElogbeta[:, ids]  # beta : k * v
            # The optimal phi_{dwk} is proportional to
            # expElogthetad_k * expElogbetad_w. phinorm is the normalizer.
            phinorm = np.dot(expElogthetad, expElogbetad) + 1e-100  # 归一化因子，为什么选这个?
            # Iterate between gamma and phi until convergence
            for _ in xrange(self.iterations):
                lastgamma = gammad
                # We represent phi implicitly to save memory and time.
                # Substituting the value of the optimal phi back into
                # the update for gamma gives this update. Cf. Lee&Seung 2001.
                gammad = self._alpha + expElogthetad * np.dot(cts / phinorm, expElogbetad.T)
                Elogthetad = dirichlet_expectation(gammad)
                expElogthetad = np.exp(Elogthetad)
                phinorm = np.dot(expElogthetad, expElogbetad) + 1e-100
                # If gamma hasn't changed much, we're done.
                meanchange = np.mean(abs(gammad - lastgamma))
                if meanchange < self.gamma_threshold:
                    break
            gamma[d, :] = gammad
            # Contribution of document d to the expected sufficient
            # statistics for the M step.
            sstats[:, ids] += np.outer(expElogthetad.T, cts / phinorm)  # ?

            # This step finishes computing the sufficient statistics for the
            # M step, so that
            # sstats[k, w] = \sum_d n_{dw} * phi_{dwk}
            # = \sum_d n_{dw} * exp{Elogtheta_{dk} + Elogbeta_{kw}} / phinorm_{dw}.
        # 他这里先算 \sum_d n_{dw} * exp{Elogtheta_{dk}/ phinorm_{dw}. 最后 * beta 没有保存phi的结果，省内存和时间
        sstats = sstats * self._expElogbeta
        return gamma, sstats

    def do_e_step(self,chunk):
        # Do an E step to update gamma, phi | lambda for this
        # mini-batch. This also returns the information about phi that
        # we need to update lambda.
        gamma, states = self.inference(chunk)
        return gamma,states

    #todo


def float_2_decimals(x):
    return int(x * 100 + 0.05) / 100.


def dirichlet_expectation(alpha):
    """
        For a vector theta ~ Dir(alpha), computes E[log(theta)] given alpha.
    """
    if len(alpha.shape) == 1:
        return psi(alpha) - psi(np.sum(alpha))
    return psi(alpha) - psi(np.sum(alpha, 1))[:, np.newaxis]

def main():
    def get_data():
        client = pymongo.MongoClient()
        db = client.twitter4
        cursor = db.stream.aggregate([
            {'$match': {
                'date': {
                    '$gt': datetime.datetime(2015, 11, 13)
                }
            }},
            {'$sort': {'date': 1}},
            {'$project': {'text': 1, 'date': 1}},
        ])

        
if __name__ == '__main__':
    main()


