
from chrombigram.precomputed import chrombigram_sets

class Chrombigram(object):
    chrombigram_str = {}

    @classmethod
    def _compute_chrombigram_str(cls):
        for chrombi in chrombigram_sets:
            s = str(chrombi)
            # Converting pitch classes 10 and 11 into single characters
            s = s.replace('10', 'A').replace('11', 'B')
            # Adding a letter to the empty set, just to identify rests in MusicXML/Humdrum
            # (doesn't apply to MIDI files)
            s = s.replace('()', 'X')
            s = ''.join(pc for pc in s if pc in '0123456789ABX')
            cls.chrombigram_str[chrombi] = s

    def __init__(self, pcset):
        if not self.chrombigram_str:
            self._compute_chrombigram_str()
        pcset = frozenset(pcset)
        if pcset in self.chrombigram_str:
            self.pcset = pcset
        else:
            self.pcset = frozenset({})

    def __str__(self):
        return self.chrombigram_str[self.pcset]