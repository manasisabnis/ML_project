import pickle
import os
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint
NOTES_FILE = "data/notes.pkl"

MODEL_FOLDER = "models"

MODEL_FILE = "models/best_model.keras"

MAPPING_FILE = "models/note_mapping.pkl"

SEQUENCE_LENGTH = 40

EPOCHS = 10

BATCH_SIZE = 32

LSTM_UNITS = 128

print("Loading extracted notes...")

with open(NOTES_FILE, "rb") as f:
    notes = pickle.load(f)

print(f"Total musical events: {len(notes)}")
unique_notes = sorted(set(notes))

print(
    f"Number of unique musical events: "
    f"{len(unique_notes)}"
)


note_to_int = {
    note: number
    for number, note in enumerate(unique_notes)
}

int_to_note = {
    number: note
    for number, note in enumerate(unique_notes)
}

n_vocab = len(unique_notes)
print("Creating training sequences...")

network_input = []
network_output = []


for i in range(
    len(notes) - SEQUENCE_LENGTH
):

    sequence = notes[
        i:i + SEQUENCE_LENGTH
    ]

    target = notes[
        i + SEQUENCE_LENGTH
    ]

    network_input.append(
        [
            note_to_int[n]
            for n in sequence
        ]
    )

    network_output.append(
        note_to_int[target]
    )


network_input = np.array(
    network_input,
    dtype=np.int32
)

network_output = np.array(
    network_output,
    dtype=np.int32
)


print(
    f"Number of training sequences: "
    f"{len(network_input)}"
)
network_input = np.reshape(
    network_input,
    (
        len(network_input),
        SEQUENCE_LENGTH,
        1
    )
)


# Normalize

network_input = (
    network_input /
    float(n_vocab)
)
print("Building LSTM model...")


model = Sequential(
    [
        Input(
            shape=(
                SEQUENCE_LENGTH,
                1
            )
        ),

        LSTM(
            LSTM_UNITS
        ),

        Dropout(
            0.3
        ),

        Dense(
            n_vocab,
            activation="softmax"
        )
    ]
)

model.compile(
    loss="sparse_categorical_crossentropy",
    optimizer="adam"
)


print()
print("Model architecture:")

model.summary()

os.makedirs(
    MODEL_FOLDER,
    exist_ok=True
)
checkpoint = ModelCheckpoint(
    MODEL_FILE,
    monitor="loss",
    save_best_only=True,
    mode="min"
)

print()
print("Starting training...")
print()


history = model.fit(
    network_input,
    network_output,

    epochs=EPOCHS,

    batch_size=BATCH_SIZE,

    callbacks=[
        checkpoint
    ],

    shuffle=True
)

import matplotlib.pyplot as plt

os.makedirs("output", exist_ok=True)

plt.figure(figsize=(8, 5))

plt.plot(
    history.history["loss"],
    label="Training Loss"
)

plt.title("LSTM Training Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "output/training_loss.png"
)

plt.close()

print("Training loss graph saved to: output/training_loss.png")
with open(
    MAPPING_FILE,
    "wb"
) as f:

    pickle.dump(
        {
            "note_to_int": note_to_int,
            "int_to_note": int_to_note,
            "sequence_length": SEQUENCE_LENGTH
        },
        f
    )

print()
print("=" * 50)
print("TRAINING COMPLETED")
print("=" * 50)

print(
    f"Model saved to: {MODEL_FILE}"
)

print(
    f"Mapping saved to: {MAPPING_FILE}"
)