import inspect
from sklearn.externals import joblib


def get_current_function_name():
    return inspect.stack()[1][3]


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


neg_words = {"never", "no", "nothing", "nowhere", "none", "none", "not", "haven't", "hasn't", "hadn't", "can't",
             "couldn't", "shouldn't", "won't", "wouldn't", "don't", "didn't", "isn't", "aren't", "ain't", "n't"}

punctuation = {'.', ':', ';', '!', '?'}
specialChar = '#@%^&()_=`{}:"|[]\;\',./\n\t\r '