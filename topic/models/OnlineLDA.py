
import codecs
import datetime
from collections import Counter
import itertools

import math
import numpy as np
import pymongo
from scipy.special import gammaln, psi
from Corpus import Corpus


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
    #do not change its config
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