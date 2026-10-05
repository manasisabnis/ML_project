import os
import glob
import numpy as np
from collections import Counter
from music21 import converter, note, chord
import matplotlib.pyplot as plt
OUTPUT_FOLDER = "output"

TEMPERATURES = [0.5, 0.8, 1.0, 1.3]


def calculate_entropy(pitches):
    "Calculate pitch entropy in bits."
    if not pitches:
        return 0.0

    counts = Counter(pitches)
    total = len(pitches)

    probabilities = np.array(
        [count / total for count in counts.values()]
    )

    return float(-np.sum(probabilities * np.log2(probabilities)))


def extract_events(midi_file):
    "Extract notes and chords from a MIDI file."
    score = converter.parse(midi_file)
    elements = score.flatten().notes

    events = []
    pitches = []
    chord_sizes = []

    for element in elements:

        if isinstance(element, note.Note):
            pitch = element.pitch.midi

            events.append({
                "type": "note",
                "pitches": [pitch]
            })

            pitches.append(pitch)

        elif isinstance(element, chord.Chord):
            chord_pitches = [
                p.midi for p in element.pitches
            ]

            events.append({
                "type": "chord",
                "pitches": chord_pitches
            })

            pitches.extend(chord_pitches)
            chord_sizes.append(len(chord_pitches))

    return score, events, pitches, chord_sizes


def calculate_in_key_fraction(pitches, key):
    "Calculate the fraction of pitches belonging to the detected key."
    if not pitches:
        return 0.0

    scale_pitch_classes = {
        p.pitchClass
        for p in key.getScale().getPitches()
    }

    in_key = sum(
        1 for pitch in pitches
        if pitch % 12 in scale_pitch_classes
    )

    return in_key / len(pitches)


def calculate_repeated_chords(events):
    " Count chord events that have appeared previously."
    chord_events = []

    for event in events:
        if event["type"] == "chord":
            chord_events.append(
                tuple(sorted(event["pitches"]))
            )

    if not chord_events:
        return 0

    counts = Counter(chord_events)

    repeated = sum(
        count - 1
        for count in counts.values()
        if count > 1
    )

    return repeated


def calculate_repeated_patterns(events, pattern_length=4):
    """
    Calculate the fraction of repeated consecutive
    event patterns.
    """

    if len(events) < pattern_length:
        return 0.0

    patterns = []

    for i in range(len(events) - pattern_length + 1):

        pattern = tuple(
            tuple(sorted(events[j]["pitches"]))
            for j in range(i, i + pattern_length)
        )

        patterns.append(pattern)

    counts = Counter(patterns)

    repeated_windows = sum(
        count
        for count in counts.values()
        if count > 1
    )

    return repeated_windows / len(patterns)


def analyze_file(midi_file):
    "Analyze one generated MIDI file."

    score, events, pitches, chord_sizes = extract_events(
        midi_file
    )

    if not events:
        return None

    number_of_events = len(events)

    total_pitches = len(pitches)

    notes_per_event = (
        total_pitches / number_of_events
    )

    chord_events = sum(
        1
        for event in events
        if event["type"] == "chord"
    )

    chord_percentage = (
        chord_events / number_of_events
    ) * 100

    largest_chord = (
        max(chord_sizes)
        if chord_sizes
        else 1
    )

    pitch_range = (
        max(pitches) - min(pitches)
        if pitches
        else 0
    )

    distinct_pitches = len(set(pitches))

    pitch_entropy = calculate_entropy(pitches)

    try:
        detected_key = score.analyze("key")
        key_name = detected_key.name

        in_key_fraction = calculate_in_key_fraction(
            pitches,
            detected_key
        )

    except Exception:
        key_name = "Unknown"
        in_key_fraction = 0.0

    repeated_chords = calculate_repeated_chords(
        events
    )

    repeated_patterns = calculate_repeated_patterns(
        events
    )

    return {
        "notes_per_event": notes_per_event,
        "chord_percentage": chord_percentage,
        "largest_chord": largest_chord,
        "pitch_range": pitch_range,
        "distinct_pitches": distinct_pitches,
        "pitch_entropy": pitch_entropy,
        "key": key_name,
        "in_key_fraction": in_key_fraction,
        "repeated_chords": repeated_chords,
        "repeated_4_event_patterns": repeated_patterns
    }


def main():
    print()

    results = []

    for temperature in TEMPERATURES:

        filename = (
            f"generated_temperature_{temperature}.mid"
        )

        filepath = os.path.join(
            OUTPUT_FOLDER,
            filename
        )

        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            continue

        print(f"Analyzing temperature {temperature}...")

        metrics = analyze_file(filepath)

        if metrics is None:
            print("No musical events found.")
            continue

        metrics["temperature"] = temperature
        results.append(metrics)
    for result in results:

        print()
        print(
            f"Temperature: {result['temperature']}"
        )

        print(
            f"Notes per event: "
            f"{result['notes_per_event']:.2f}"
        )

        print(
            f"Chord events: "
            f"{result['chord_percentage']:.0f}%"
        )

        print(
            f"Largest chord: "
            f"{result['largest_chord']} notes"
        )

        print(
            f"Pitch range: "
            f"{result['pitch_range']} semitones"
        )

        print(
            f"Distinct pitches: "
            f"{result['distinct_pitches']}"
        )

        print(
            f"Pitch entropy: "
            f"{result['pitch_entropy']:.2f} bits"
        )

        print(
            f"Best-fit key: "
            f"{result['key']}"
        )

        print(
            f"In-key fraction: "
            f"{result['in_key_fraction']:.2f}"
        )

        print(
            f"Repeated chord events: "
            f"{result['repeated_chords']}"
        )

        print(
            f"Repeated 4-event patterns: "
            f"{result['repeated_4_event_patterns']:.2f}"
        )

    print()
    temperatures = [
        result["temperature"]
        for result in results
    ]

    chord_percentages = [
        result["chord_percentage"]
        for result in results
    ]

    distinct_pitches = [
        result["distinct_pitches"]
        for result in results
    ]

    pitch_ranges = [
        result["pitch_range"]
        for result in results
    ]

    pitch_entropies = [
        result["pitch_entropy"]
        for result in results
    ]

    in_key_fractions = [
        result["in_key_fraction"] * 100
        for result in results
    ]

    # Chord percentage vs temperature
    plt.figure(figsize=(7, 5))
    plt.plot(
        temperatures,
        chord_percentages,
        marker="o"
    )
    plt.xlabel("Temperature")
    plt.ylabel("Chord Events (%)")
    plt.title("Effect of Temperature on Chord Density")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(
        "output/chord_density_vs_temperature.png",
        dpi=300
    )
    plt.close()

    # Distinct pitches vs temperature
    plt.figure(figsize=(7, 5))
    plt.plot(
        temperatures,
        distinct_pitches,
        marker="o"
    )
    plt.xlabel("Temperature")
    plt.ylabel("Distinct Pitches")
    plt.title("Effect of Temperature on Pitch Diversity")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(
        "output/pitch_diversity_vs_temperature.png",
        dpi=300
    )
    plt.close()

    # Pitch range vs temperature
    plt.figure(figsize=(7, 5))
    plt.plot(
        temperatures,
        pitch_ranges,
        marker="o"
    )
    plt.xlabel("Temperature")
    plt.ylabel("Pitch Range (semitones)")
    plt.title("Effect of Temperature on Pitch Range")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(
        "output/pitch_range_vs_temperature.png",
        dpi=300
    )
    plt.close()

    # Pitch entropy vs temperature
    plt.figure(figsize=(7, 5))
    plt.plot(
        temperatures,
        pitch_entropies,
        marker="o"
    )
    plt.xlabel("Temperature")
    plt.ylabel("Pitch Entropy (bits)")
    plt.title("Effect of Temperature on Pitch Entropy")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(
        "output/pitch_entropy_vs_temperature.png",
        dpi=300
    )
    plt.close()

    # In-key fraction vs temperature
    plt.figure(figsize=(7, 5))
    plt.plot(
        temperatures,
        in_key_fractions,
        marker="o"
    )
    plt.xlabel("Temperature")
    plt.ylabel("In-Key Notes (%)")
    plt.title("Effect of Temperature on Tonal Consistency")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(
        "output/in_key_fraction_vs_temperature.png",
        dpi=300
    )
    plt.close()

    print()
    print("Graphs saved to output/")


if __name__ == "__main__":
    main()