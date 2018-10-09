import inspect
from sklearn.externals import joblib


def get_current_function_name():
    return inspect.stack()[1][3]


class Singleton(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(Singleton, self).__call__(*args,**kwargs)
        return self._instances[self]



neg_words = {"never", "no", "nothing", "nowhere", "none", "none", "not", "haven't", "hasn't", "hadn't", "can't",
             "couldn't", "shouldn't", "won't", "wouldn't", "don't", "didn't", "isn't", "aren't", "ain't", "n't"}

punctuation = {'.', ':', ';', '!', '?'}
specialChar = '#@%^&()_=`{}:"|[]\;\',./\n\t\r '



