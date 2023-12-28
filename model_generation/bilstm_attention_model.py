import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Bidirectional,
    LSTM,
    Dense,
    Embedding,
    TimeDistributed,
)
from preprocessing_midi import process_midi_files_in_directory
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Bidirectional, LSTM, Dense, Embedding, Dropout
from tensorflow.keras import backend as K


# Define the Attention Layer
class AttentionLayer(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(
            name="attention_weight",
            shape=(input_shape[-1], 1),
            initializer="random_normal",
            trainable=True,
        )
        self.b = self.add_weight(
            name="attention_bias",
            shape=(input_shape[1], 1),
            initializer="zeros",
            trainable=True,
        )
        super(AttentionLayer, self).build(input_shape)

    def call(self, x):
        # Alignment scores. e = tanh(W.h + b)
        e = K.tanh(K.dot(x, self.W) + self.b)
        # Softmax to calculate attention weights
        a = K.softmax(e, axis=1)
        output = x * a
        # Sum over the sequence dimension to produce context vector
        return K.sum(output, axis=1)


# Model parameters
vocab_size = 1000  # Replace with vocabulary size
embedding_dim = 256
lstm_units = 128
max_sequence_len = 100  # Replace with sequence length

# Model definition
model = Sequential()
model.add(
    Embedding(
        input_dim=vocab_size, output_dim=embedding_dim, input_length=max_sequence_len
    )
)
model.add(Bidirectional(LSTM(lstm_units, return_sequences=True)))
model.add(AttentionLayer())
model.add(Dropout(0.5))
model.add(Dense(vocab_size, activation="softmax"))

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

model.summary()
