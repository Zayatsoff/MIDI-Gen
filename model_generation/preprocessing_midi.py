from music21 import converter, instrument, note, chord
import os


def parse_midi(midi_path):
    """Parse a MIDI file into a dictionary format"""
    midi = converter.parse(midi_path)
    notes_to_parse = []

    try:  # file has instrument parts
        parts = instrument.partitionByInstrument(midi)
        if parts:  # if parts has instrument parts
            notes_to_parse = parts.parts[0].recurse()
        else:  # file has notes in a flat structure
            notes_to_parse = midi.flat.notes
    except:  # file has notes in a flat structure
        notes_to_parse = midi.flat.notes

    notes_dict = {"notes": [], "durations": [], "offsets": []}
    for element in notes_to_parse:
        if isinstance(element, note.Note):
            notes_dict["notes"].append(str(element.pitch))
            notes_dict["durations"].append(element.duration.quarterLength)
            notes_dict["offsets"].append(element.offset)
        elif isinstance(element, chord.Chord):
            notes_dict["notes"].append(".".join(str(n) for n in element.normalOrder))
            notes_dict["durations"].append(element.duration.quarterLength)
            notes_dict["offsets"].append(element.offset)

    return notes_dict


def process_midi_files_in_directory(directory_path):
    """Process all MIDI files in the given directory"""
    midi_dicts = []
    for file in os.listdir(directory_path):
        if file.endswith(".mid") or file.endswith(".midi"):
            path = os.path.join(directory_path, file)
            midi_dict = parse_midi(path)
            midi_dicts.append(midi_dict)
    return midi_dicts


# Example usage
midi_dicts = process_midi_files_in_directory("path_to_midi_files_directory")
