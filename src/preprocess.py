import os
import glob
import pickle

from music21 import converter, note, chord


MIDI_FOLDER = "data/midi"
OUTPUT_FILE = "data/notes.pkl"

# Start small so we can test everything first
MAX_FILES = 100


def extract_notes():

    notes = []

    # Search for MIDI files inside all subfolders
    midi_files = glob.glob(
        os.path.join(MIDI_FOLDER, "**", "*.mid"),
        recursive=True
    )

    midi_files += glob.glob(
        os.path.join(MIDI_FOLDER, "**", "*.midi"),
        recursive=True
    )

    print(f"Found {len(midi_files)} MIDI files.")

    # Only use first 100 for our first experiment
    midi_files = midi_files[:MAX_FILES]

    print(f"Processing {len(midi_files)} MIDI files...")

    for i, file in enumerate(midi_files):

        try:

            print(
                f"[{i + 1}/{len(midi_files)}] "
                f"Processing: {file}"
            )

            midi = converter.parse(file)

            elements = midi.flatten().notes

            for element in elements:

                # Single note
                # Single note
                if isinstance(element, note.Note):

                    notes.append(
                        str(element.pitch)
                    )

                # Chord
                elif isinstance(element, chord.Chord):

                    chord_notes = ".".join(
                        str(n)
                        for n in element.pitches
                    )

                    notes.append(chord_notes)

        except Exception as e:

            print(f"Could not process {file}")
            print(f"Error: {e}")

    print()
    print("=" * 50)
    print(
        f"Total musical events extracted: {len(notes)}"
    )
    print("=" * 50)

    # Save extracted notes
    with open(OUTPUT_FILE, "wb") as f:

        pickle.dump(notes, f)

    print(
        f"Saved extracted notes to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    extract_notes()