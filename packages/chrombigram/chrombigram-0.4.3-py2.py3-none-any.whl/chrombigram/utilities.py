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
    THRESHOLD = 0.0
    t_elapsed = 0.0
    for msg in mid:
        t_elapsed += msg.time if hasattr(msg, 'time') else 0.0
        if msg.type == 'note_on' and msg.velocity > 0:
            if t_elapsed > THRESHOLD:
                # Create new slice
                if slic:
                    slices.append(slic)
                slic = [msg.note % 12]
                t_elapsed = 0.0
            else:
                # Append to current slice
                slic.append(msg.note % 12)
    # Add the last slice
    if slic:
        slices.append(slic)
    pcs = [frozenset(slic) for slic in slices]
    return pcs