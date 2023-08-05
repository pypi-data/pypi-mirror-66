from chrombigram.chrombigram import Chrombigram
import music21

import sys

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
    for pc in scorepcs:
        print(Chrombigram(pc), end=' ')