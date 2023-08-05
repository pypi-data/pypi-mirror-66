from chrombigram.chrombigram import Chrombigram, ChrombigramCounter
from chrombigram.utilities import getpcs_midi

import sys
import pprint

if __name__ == '__main__':
    pcss = getpcs_midi(sys.argv[1])
    counter = ChrombigramCounter()
    for pcs in pcss:
        chrombi = Chrombigram(pcs)
        counter.append(chrombi)
        print(chrombi, end=' ')
    # pprint.pprint(counter.chrombigram_dict)
