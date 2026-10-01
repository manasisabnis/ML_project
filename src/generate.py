import pickle
import os
import numpy as np

from tensorflow.keras.models import load_model
from music21 import stream, note, chord


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_PATH = "models/best_model.keras"

MAPPING_PATH = "models/note_mapping.pkl"

OUTPUT_FOLDER = "output"

GENERATE_LENGTH = 200

TEMPERATURE = 0.8

OUTPUT_FILE = f"output/generated_temperature_{TEMPERATURE}.mid"


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading trained model...")

model = load_model(MODEL_PATH)

print("Model loaded successfully.")


# ============================================================
# LOAD NOTE MAPPING
# ============================================================

with open(MAPPING_PATH, "rb") as f:

    mapping = pickle.load(f)


note_to_int = mapping["note_to_int"]

int_to_note = mapping["int_to_note"]

sequence_length = mapping["sequence_length"]


n_vocab = len(note_to_int)


print(
    f"Vocabulary size: {n_vocab}"
)

print(
    f"Sequence length: {sequence_length}"
)


# ============================================================
# CREATE RANDOM SEED
# ============================================================

print()
print("Creating random seed...")

all_notes = list(note_to_int.keys())


start = np.random.randint(
    0,
    len(all_notes) - sequence_length
)


pattern = [
    note_to_int[n]
    for n in all_notes[
        start:start + sequence_length
    ]
]


# ============================================================
# TEMPERATURE SAMPLING
# ============================================================

def sample_with_temperature(
    prediction,
    temperature=1.0
):

    prediction = np.asarray(
        prediction
    ).astype("float64")

    # Prevent log(0)
    prediction = np.log(
        prediction + 1e-8
    )

    # Apply temperature
    prediction = (
        prediction /
        temperature
    )

    # Convert back to probabilities
    exp_prediction = np.exp(
        prediction
    )

    probabilities = (
        exp_prediction /
        np.sum(exp_prediction)
    )

    # Randomly select according to
    # probability distribution
    return np.random.choice(
        len(probabilities),
        p=probabilities
    )


# ============================================================
# GENERATE MUSIC
# ============================================================

print()
print(
    f"Generating {GENERATE_LENGTH} events..."
)

generated_notes = []


for i in range(
    GENERATE_LENGTH
):

    # Prepare input
    input_sequence = np.reshape(
        pattern,
        (
            1,
            sequence_length,
            1
        )
    )

    # Normalize exactly as during training
    input_sequence = (
        input_sequence /
        float(n_vocab)
    )

    # Predict next musical event
    prediction = model.predict(
        input_sequence,
        verbose=0
    )[0]

    # Sample prediction
    index = sample_with_temperature(
        prediction,
        TEMPERATURE
    )

    # Convert integer back to note
    result = int_to_note[index]

    generated_notes.append(
        result
    )

    # Add predicted note to sequence
    pattern.append(index)

    # Remove oldest note
    pattern = pattern[1:]

    if (i + 1) % 25 == 0:

        print(
            f"Generated {i + 1}/"
            f"{GENERATE_LENGTH}"
        )


# ============================================================
# CONVERT GENERATED EVENTS TO MIDI
# ============================================================

print()
print("Converting generated music to MIDI...")


output = stream.Stream()


for item in generated_notes:

    try:

        # -----------------------------
        # Chord
        # -----------------------------

        if "." in item:

            chord_notes = item.split(".")

            chord_obj = chord.Chord(
                chord_notes
            )

            output.append(
                chord_obj
        )
        # -----------------------------
        # Single note
        # -----------------------------

        else:

            new_note = note.Note(item)

            output.append(
                new_note
            )

    except Exception as e:

        print(
            f"Could not convert {item}: {e}"
        )


# ============================================================
# SAVE MIDI
# ============================================================

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


output.write(
    "midi",
    fp=OUTPUT_FILE
)


print()
print("=" * 50)
print("MUSIC GENERATION COMPLETE")
print("=" * 50)

print(
    f"Generated MIDI saved to:"
)

print(
    OUTPUT_FILE
)