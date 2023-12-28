# Assuming midi_dicts is your list of dictionaries from Step 1
notes = [note for midi_dict in midi_dicts for note in midi_dict["notes"]]
# More processing will be needed for durations and offsets

# Create a mapping from notes to integers
unique_notes = sorted(list(set(notes)))
note_to_int = dict((note, number) for number, note in enumerate(unique_notes))

# Prepare input and output sequences
sequence_length = 100  # Length of each input sequence
network_input = []
network_output = []

for midi_dict in midi_dicts:
    for i in range(len(midi_dict["notes"]) - sequence_length):
        sequence_in = midi_dict["notes"][i : i + sequence_length]
        sequence_out = midi_dict["notes"][i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])
        network_output.append(note_to_int[sequence_out])

network_input = np.array(
    pad_sequences(network_input, maxlen=sequence_length, padding="pre")
)
network_output = to_categorical(network_output, num_classes=len(unique_notes))

# Split data into training and validation sets
from sklearn.model_selection import train_test_split

X_train, X_val, y_train, y_val = train_test_split(
    network_input, network_output, test_size=0.2, random_state=0
)

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=64, validation_data=(X_val, y_val))
