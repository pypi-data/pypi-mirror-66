import mido

def getpcs_music21(m21):
    allpcs = []
    for x in m21.chordify().flat.notes:
        pcs = []
        for n in x:
            pcs.append(n.pitch.pitchClass)
        pcs = frozenset(pcs)
        allpcs.append(pcs)
    return allpcs


def getpcs_midi(filename):
    """ Returns a list of notes from the note_on events of a MIDI file. """
    mid = mido.MidiFile(filename)
    slices = []
    slic = []
    for msg in mid:
        if msg.type == 'note_on' and msg.velocity > 0:
            # Add to the current slice
            if slic and msg.time == 0:
                slic.append(msg.note % 12)
            # Start a new slice
            else:
                if slic:
                    slices.append(slic)
                slic = [msg.note % 12]
    if slic:
        slices.append(slic)
    pcs = [frozenset(slic) for slic in slices]
    return pcs