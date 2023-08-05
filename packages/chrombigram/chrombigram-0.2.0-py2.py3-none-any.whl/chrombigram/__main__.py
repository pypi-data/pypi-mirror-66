from chrombigram.chrombigram import Chrombigram, ChrombigramCounter
import music21

import sys
import pprint

def getpcs_music21(m21):
    allpcs = []
    for x in m21.chordify().flat.notes:
        pcs = []
        for n in x:
            pcs.append(n.pitch.pitchClass)
        pcs = frozenset(pcs)
        allpcs.append(pcs)
    return allpcs

if __name__ == '__main__':
    score = music21.converter.parse(sys.argv[1])
    scorepcs = getpcs_music21(score)
    counter = ChrombigramCounter()
    for pc in scorepcs:
        chrombi = Chrombigram(pc)
        counter.append(chrombi)
        # print(chrombi, end=' ')
    pprint.pprint(counter.chrombigram_dict)
