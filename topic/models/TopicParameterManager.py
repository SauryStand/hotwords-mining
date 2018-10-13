


class TopicParameterManager(object):
    def __init__(self,param):
        param = dict(param)
        for x,t in param.items():
            if param[x] == '':
                del param[x]

        self.mode = int(param.get('mode', 1))

        # ---------- LDA ------------
        self.LDA_k = int(param.get('LDA_k', 15))
        self.LDA_timeWindow = int(param.get('LDA_timeWindow', 30))