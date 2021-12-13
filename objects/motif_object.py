class Motifs(object):
    def __init__(self, candidates: list = [], indexes: list = [], mdl_dev:list = [], k_list:list = []):
        self.reset()
        self.candidates = candidates
        self.indexes = indexes
        self.mdl_dev = mdl_dev
        self.k_list = k_list


    def reset(self):
        self.candidates = []
        self.indexes = []
        self.mdl_dev = []
        self.k_list = []


    def set_lists(self, k, candidate, index, mld):
        self.k_list.append(k)
        self.candidates.append(candidate)
        self.indexes.append(index)
        self.mdl_dev.append(mld)