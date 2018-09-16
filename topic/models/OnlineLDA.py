
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