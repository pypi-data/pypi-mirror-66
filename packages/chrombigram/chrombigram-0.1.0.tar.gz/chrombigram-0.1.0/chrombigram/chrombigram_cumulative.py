
from chrombigram.precomputed import chrombigram_sets
import numpy as np

class ChrombigramCumulative(object):
    def __init__(self):
        self.clean()

    def clean(self):
        self.chrombigram_dict = {k: 0 for k in chrombigram_sets}

    def append(self, pcset):
        if pcset in self.chrombigram_dict:
            self.chrombigram_dict[pcset] += 1

    def get_as_box_array(self):
        arr = list(self.chrombigram_dict.values())
        arr = np.array(arr).reshape(64, -1)
        return arr
