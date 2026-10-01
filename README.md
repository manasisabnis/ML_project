Generating Music with Machine Learning 🎵

#About the Project

This project uses a Long Short Term Memory neural network to learn patterns from piano music and generate new musical sequences.

The model is trained on MIDI files from the MAESTRO dataset. It learns to predict the next musical note or chord based on the previous 40 musical events.

The generated sequence is converted back into a MIDI file that can be played or downloaded.

The project also includes a Streamlit web interface for generating music interactively.

How It Works:
MAESTRO MIDI Dataset
MIDI Preprocessing
Notes & Chords
Sequences of 40 Events
LSTM Model
Predict Next Musical Event
Temperature Sampling
Generated Music
MIDI File

Dataset
We used the MAESTRO MIDI dataset, which contains piano performances in MIDI format.
For this project, we used 100 MIDI files due to computational constraints.
After preprocessing:
- Musical events extracted: 232,979
- Unique musical events: 51,692
- Sequence length: 40 events
The extracted data is stored in:
data/notes.pkl

Model
We use an LSTM (Long Short-Term Memory) network because music is sequential — the next musical event can depend on what came before it.
Model configuration
Parameter	Value
LSTM units	128
Sequence length	40
Dropout	0.3
Optimizer	Adam
Loss	Sparse Categorical Crossentropy
Epochs	10
Batch size	32


The trained model is saved as:
models/best_model.keras

Training
The model was trained for 10 epochs.
The training loss decreased from approximately 8.28 at the beginning to approximately 7.77 by the final epoch.
The training loss graph is available at:
output/training_loss.png

Music Generation
After training, the model generates music by repeatedly predicting the next musical event.
We experimented with different temperature values to observe how sampling affects the generated music.
Temperature	Notes Generated	Unique Pitches	Pitch Range
0.5	248	39	33–82
0.8	264	57	33–99
1.0	347	67	30–99
1.3	498	70	26–101


In general, lower temperatures produce more conservative sequences, while higher temperatures allow more variation in the generated music.
The generated MIDI files are available in:
output/

Streamlit App
The project includes a simple Streamlit interface where the user can:
- Choose the sampling temperature
- Choose the number of musical events
- Generate music
- Download the generated MIDI file
Run the application with:
./venv/bin/python -m streamlit run src/app.py

Then open the local URL shown in the terminal.
Project Structure
ML/
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
│   ├── generate.py
│   ├── preprocess.py
│   └── train.py
│
├── .gitignore
├── README.md
└── requirements.txt

What each file does
File	Purpose
preprocess.py	Extracts notes and chords from MIDI files
train.py	Builds and trains the LSTM model
generate.py	Generates new MIDI music
app.py	Runs the Streamlit interface
notes.pkl	Stores extracted musical events
best_model.keras	Trained LSTM model
note_mapping.pkl	Maps musical events to model indices
training_loss.png	Training loss visualization


Technologies Used
Python
TensorFlow / Keras
LSTM
Music21
NumPy
Matplotlib
Streamlit
MIDI
MAESTRO Dataset
How to Run
1. Clone the repository
git clone <repository-url>
cd ML

2. Create and activate the virtual environment
python -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Preprocess the dataset
python src/preprocess.py

5. Train the model
python src/train.py

6. Generate music
python src/generate.py

7. Run the Streamlit application
python -m streamlit run src/app.py

Limitations
- Only 100 MIDI files were used because of computational constraints.
- The current representation mainly focuses on notes and chords.
- Musical timing and other expressive properties are not fully represented.
- The model was trained for 10 epochs.
- The generated music has not been evaluated through a large-scale human listening study.
Future Improvements
- Train on more MIDI files.
- Train for longer and experiment with different LSTM architectures.
- Include rhythm, duration and velocity information.
- Experiment with deeper LSTMs and Transformer-based models.
- Perform a formal human evaluation of the generated music.
Conclusion
This project demonstrates how an LSTM can learn sequential patterns from MIDI music and use those patterns to generate new musical sequences.
The trained model successfully generates playable MIDI files, and the temperature experiments show how changing the sampling temperature affects the variation of the generated music.
The Streamlit interface makes the trained model easy to interact with and allows users to generate and download their own music.
References
- Stanford CS229 Project Report
- Stanford CS229 Project Poster
- MAESTRO Dataset
- Music21
- TensorFlow