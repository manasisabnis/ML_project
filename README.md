# Generating Music with Machine Learning

A music generation project built using an LSTM (Long Short-Term Memory) neural network. The model is trained on piano MIDI data from the MAESTRO dataset and learns to predict the next musical note or chord based on previous musical events.

The generated musical sequence is converted into a MIDI file. A Streamlit web interface is also provided to generate music using different temperature values and sequence lengths.

## Dataset

The project uses the MAESTRO MIDI dataset containing classical piano performances.

Due to computational constraints, 100 MIDI files were used for training.

Dataset details:

- Musical events extracted: 232,979
- Unique musical events: 51,692
- Sequence length: 40 musical events

Each musical event can represent either a single note or a chord.

The extracted events are stored in:

```text
data/notes.pkl

Model
The project uses an LSTM neural network to learn sequential patterns in the musical data.
The model consists of:
- LSTM layer with 128 units
- Dropout layer with dropout rate 0.3
- Dense output layer with softmax activation
- Adam optimizer
- Sparse categorical crossentropy loss
- Batch size of 32
- 10 training epochs
The trained model is saved as:
models/best_model.keras

The musical event mapping is stored in:
models/note_mapping.pkl

How It Works
The process used by the project is:
1. MIDI files are loaded using Music21.
2. Notes and chords are extracted from the MIDI files.
3. Musical events are converted into integer representations.
4. Sequences of 40 events are created for training.
5. The LSTM predicts the next musical event.
6. During generation, the predicted event is sampled using a temperature value.
7. The generated events are converted back into a MIDI file.
Training
The model was trained for 10 epochs.
The training loss decreased from approximately 8.28 at the beginning of training to approximately 7.77 by the final epoch.
The training loss graph is saved at:
output/training_loss.png

Music Generation
Different temperature values were tested to observe their effect on the generated music.
Temperature	Notes Generated	Unique Pitches	Pitch Range
0.5	248	39	33–82
0.8	264	57	33–99
1.0	347	67	30–99
1.3	498	70	26–101


Lower temperature values produce more conservative sequences, while higher temperature values allow more variation in the generated music.
The generated MIDI files are stored in:
output/

Installation
Python is required to run the project.
Create a virtual environment:
python -m venv venv

Activate the virtual environment:
macOS / Linux
source venv/bin/activate

Windows
venv\Scripts\activate

Install the required packages:
pip install -r requirements.txt

Usage
Run the Streamlit Application
Run:
python -m streamlit run src/app.py

Then open the local URL shown in the terminal.
The Streamlit application allows the user to:
- Select the temperature
- Select the number of musical events
- Generate music
- Download the generated MIDI file
Generate Music Directly
To generate music without the Streamlit interface:
python src/generate.py

Train the Model
To train the model again:
python src/train.py

Preprocess MIDI Files
If the MIDI dataset is available locally, run:
python src/preprocess.py

Project Structure
ML_project/
│
├── data/
│   └── notes.pkl
│
├── models/
│   ├── best_model.keras
│   └── note_mapping.pkl
│
├── output/
│   ├── training_loss.png
│   ├── generated_temperature_0.5.mid
│   ├── generated_temperature_0.8.mid
│   ├── generated_temperature_1.0.mid
│   └── generated_temperature_1.3.mid
│
├── src/
│   ├── app.py
|   ├── analyse.py
│   ├── generate.py
│   ├── preprocess.py
│   └── train.py
|   
│
├── .gitignore
├── README.md
└── requirements.txt

Files
File	Description
preprocess.py	Extracts notes and chords from MIDI files
train.py	Builds and trains the LSTM model
generate.py	Generates new musical sequences and MIDI files
app.py	Runs the Streamlit application
notes.pkl	Stores extracted musical events
best_model.keras	Trained LSTM model
note_mapping.pkl	Mapping between musical events and integer indices
training_loss.png	Training loss graph


Technologies Used
- Python
- TensorFlow
- Keras
- LSTM
- Music21
- NumPy
- Matplotlib
- Streamlit
- MIDI
- MAESTRO Dataset
Limitations
- Only 100 MIDI files were used because of computational constraints.
- The current representation mainly focuses on notes and chords.
- Musical timing and other expressive properties are not fully represented.
- The model was trained for 10 epochs.
- The generated music has not been evaluated through a large-scale human listening study.
Future Improvements
- Train on more MIDI files.
- Train the model for more epochs.
- Include rhythm, duration and velocity information.
- Experiment with deeper LSTM architectures.
- Experiment with Transformer-based models.
- Perform a formal human evaluation of generated music.
Project Deliverables
The repository contains the project code, trained model, generated MIDI files, and project documentation.
The final review materials include:
- Two-page project write-up
- Final review presentation
- Training loss graph
- Generated MIDI files
References
- Stanford CS229 Project Report
- Stanford CS229 Project Poster
- MAESTRO Dataset
- Music21
- TensorFlow / Keras
