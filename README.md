
Generating Music with Machine Learning
About the Project

This project uses a Long Short-Term Memory (LSTM) neural network to learn patterns from piano music and generate new musical sequences.

The model is trained on MIDI files from the MAESTRO dataset. It learns to predict the next musical note or chord based on the previous 40 musical events.

The generated sequence is converted back into a MIDI file that can be played or downloaded.

The project also includes a Streamlit web interface that allows users to generate music interactively by selecting the sampling temperature and the number of musical events.

Repository
https://github.com/manasisabnis/ML_project

How It Works
MAESTRO MIDI Dataset
MIDI Preprocessing
Notes and Chords
Sequences of 40 Events
LSTM Model
Predict Next Musical Event
Temperature Sampling
Generated Music
MIDI File
Dataset
The project uses the MAESTRO MIDI dataset, which contains classical piano performances in MIDI format.

Due to computational constraints, 100 MIDI files were used for this project.

After preprocessing:

Dataset Detail	Value
MIDI files used	100
Musical events extracted	232,979
Unique musical events	51,692
Sequence length	40 events
The extracted musical events are stored in:

data/notes.pkl
Each musical event represents either an individual note or a chord. A chord containing multiple simultaneous pitches is treated as a single musical event.

Approach
The problem is treated as a next-event prediction task.

For each training example:

The previous 40 musical events are given as input.
The next musical event is used as the target.
Each unique musical event is mapped to an integer.
The LSTM learns patterns in these sequences.
During generation, the model repeatedly predicts the next event.
Temperature sampling is used to control the amount of variation in the generated sequence.
The generated events are converted back into a MIDI file.
Model
An LSTM was selected because music is sequential in nature. The next musical event can depend on the events that occurred previously.

Model Configuration
Parameter	Value
LSTM units	128
Sequence length	40
Dropout	0.3
Optimizer	Adam
Loss	Sparse Categorical Crossentropy
Epochs	10
Batch size	32
The model architecture is:

Input
  |
LSTM (128 units)
  |
Dropout (0.3)
  |
Dense Layer
  |
Softmax Output
The output layer predicts the probability of each possible musical event.

The trained model is saved as:

models/best_model.keras
The mapping between musical events and model indices is stored in:

models/note_mapping.pkl
Training
The model was trained for 10 epochs using the extracted musical sequences.

The training loss decreased from approximately 8.28 at the beginning of training to approximately 7.77 by the final epoch.

The training loss graph is available at:

output/training_loss.png
The training process uses ModelCheckpoint to save the best-performing model based on training loss.

Music Generation
After training, the LSTM generates music by repeatedly predicting the next musical event.

Temperature controls how the model samples from the predicted probability distribution.

Lower temperatures make the sampling more conservative, while higher temperatures allow more variation in the generated music.

Four temperature values were tested:

Temperature	Notes Generated	Unique Pitches	Pitch Range
0.5	248	39	33–82
0.8	264	57	33–99
1.0	347	67	30–99
1.3	498	70	26–101
These measurements were obtained from the generated MIDI files.

In general, increasing the temperature produced greater pitch variety and more complex chord events, while lower temperatures produced more conservative sequences.

The generated MIDI files are available in:

output/
Streamlit Application
The project includes a Streamlit interface for interactive music generation.

The application allows the user to:

Choose the sampling temperature
Choose the number of musical events to generate
Generate a new musical sequence
Download the generated MIDI file
To run the application:

./venv/bin/python -m streamlit run src/app.py

The application will provide a local URL in the terminal.

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
│   ├── generate.py
│   ├── preprocess.py
│   └── train.py
│
├── .gitignore
├── README.md
└── requirements.txt
What Each File Does
File	Purpose
preprocess.py	Extracts notes and chords from MIDI files
train.py	Builds and trains the LSTM model
generate.py	Generates new musical sequences and MIDI files
app.py	Runs the Streamlit interface
notes.pkl	Stores the extracted musical events
best_model.keras	Stores the trained LSTM model
note_mapping.pkl	Maps musical events to model indices
training_loss.png	Shows the training loss over the training epochs
Technologies Used
Python
TensorFlow
Keras
LSTM
Music21
NumPy
Matplotlib
Streamlit
MIDI
MAESTRO Dataset
How to Run
1. Clone the Repository
git clone https://github.com/manasisabnis/ML_project.git
cd ML_project

2. Create and Activate a Virtual Environment
python -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Run the Streamlit Application
The trained model and generated files are included in the repository.

python -m streamlit run src/app.py

The application will open using the local URL displayed in the terminal.

Optional: Preprocess the MIDI Dataset
If the MIDI dataset is available locally:

python src/preprocess.py

Optional: Train the Model
python src/train.py

Optional: Generate Music Directly
python src/generate.py

Project Deliverables
The repository contains the project code, trained model, generated MIDI files, and supporting documentation.

The final project documents include:

Two-page project write-up
Final review and demonstration presentation
Training loss graph
Generated MIDI files
Limitations
Only 100 MIDI files were used because of computational constraints.
The current representation mainly focuses on notes and chords.
Musical timing and other expressive properties are not fully represented.
The model was trained for only 10 epochs.
The model uses a 40-event context window.
The generated music has not been evaluated through a large-scale human listening study.
No validation split was used during the current training run.
Future Improvements
Train on a larger portion of the MAESTRO dataset.
Train the model for more epochs.
Use a validation split to evaluate generalization.
Experiment with different LSTM architectures.
Include rhythm, duration, and velocity information.
Use a longer context window.
Experiment with deeper LSTM architectures.
Explore Transformer-based music generation models.
Perform a formal human listening evaluation.
Conclusion
This project demonstrates how an LSTM neural network can learn sequential patterns from MIDI music and use those patterns to generate new musical sequences.

The trained model successfully generates MIDI files, and the temperature experiments show how changing the sampling temperature affects the variation and structure of the generated music.

The Streamlit interface provides an interactive way to select generation settings and download the resulting MIDI files.
