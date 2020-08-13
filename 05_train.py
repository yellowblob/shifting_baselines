#train an char based lstm

import sys
import numpy as np
#import multi_gpu
import string

from keras.models import Sequential
from keras.layers import LSTM, Dropout, Activation, Dense


N_GPU = 1 # you can experiment with more GPUs, it gets interesting with a high SEQUENCE_LEN
SEQUENCE_LEN = 60
BATCH_SIZE = 512
EPOCHS = 100
HIDDEN_LAYERS_DIM = 512
LAYER_COUNT = 4
DROPOUT = 0.2

filename = sys.argv[1]

# load ascii text, first argument training second one validation data
with open(filename, "r") as f:
    text_train = f.read()
with open(sys.argv[2], "r") as f:
    text_val = f.read()
with open(sys.argv[3], "r") as f:
    vocab = f.read()

raw_text = text_train + text_val

# create mapping of unique chars to integers, and a reverse mapping
characters = sorted(list(set(vocab)))

# summarize the loaded data
n_chars = len(raw_text)
print("Total Characters: ", n_chars)

VOCABULARY_SIZE = len(characters)
characters_to_ix = {c:i for i,c in enumerate(characters)}
print("vocabulary len = %d" % VOCABULARY_SIZE)
print(characters)

def describe_batch(X, y, samples=3):
    """Describe in a human-readable format some samples from a batch"""
    for i in range(samples):
        sentence = ""
        for s in range(SEQUENCE_LEN):
            sentence += characters[X[i,s,:].argmax()]
        next_char = characters[y[i,:].argmax()]
        
        print("sample #%d: ...%s -> '%s'" % (
            i,
            sentence[-20:],
            next_char
        ))

def batch_generator(text, count):
    """Generate batches for training"""
    while True: # keras wants that for reasons
        for batch_ix in range(count):
            X = np.zeros((BATCH_SIZE, SEQUENCE_LEN, VOCABULARY_SIZE))
            y = np.zeros((BATCH_SIZE, VOCABULARY_SIZE))

            batch_offset = BATCH_SIZE * batch_ix

            for sample_ix in range(BATCH_SIZE):
                sample_start = batch_offset + sample_ix
                for s in range(SEQUENCE_LEN):
                    X[sample_ix, s, characters_to_ix[text[sample_start+s]]] = 1
                y[sample_ix, characters_to_ix[text[sample_start+s+1]]]=1

            yield X, y

def build_model(gpu_count=1):
    """Build a Keras sequential model for training the char-rnn"""
    model = Sequential()
    for i in range(LAYER_COUNT):
        model.add(
            LSTM(
                HIDDEN_LAYERS_DIM, 
                return_sequences=True if (i!=(LAYER_COUNT-1)) else False,
                input_shape=(SEQUENCE_LEN, VOCABULARY_SIZE),
            )
        )
        model.add(Dropout(DROPOUT))
    
    model.add(Dense(VOCABULARY_SIZE))
    model.add(Activation('softmax'))
    
    if gpu_count>1:
        model = multi_gpu.make_parallel(model, gpu_count)
    
    model.compile(loss='categorical_crossentropy', optimizer="adam")
    return model


text_train_len = len(text_train)
text_val_len = len(text_val)
print("Total of %d characters" % (text_train_len + text_val_len))

for ix, (X,y) in enumerate(batch_generator(text_train, count=1)):
    # describe some samples from the first batch
    describe_batch(X, y, samples=5)
    break

training_model = build_model(gpu_count=N_GPU)

train_batch_count = (text_train_len - SEQUENCE_LEN) // BATCH_SIZE
val_batch_count = (text_val_len - SEQUENCE_LEN) // BATCH_SIZE
print("training batch count: %d" % train_batch_count)
print("validation batch count: %d" % val_batch_count)

filename = filename[:filename.find("_")]

# checkpoint
from keras.callbacks import ModelCheckpoint, EarlyStopping
filepath = "./%s_%d-gpu_BS-%d_%d-%s_dp%.2f_%dS_epoch{epoch:02d}-loss{loss:.4f}-val-loss{val_loss:.4f}_weights" % (
    filename,
    N_GPU,
    BATCH_SIZE,
    LAYER_COUNT,
    HIDDEN_LAYERS_DIM,
    DROPOUT,
    SEQUENCE_LEN
)
checkpoint = ModelCheckpoint(
    filepath,
    save_weights_only=True
)
# early stopping
early_stopping = EarlyStopping(monitor='val_loss', patience=5)

callbacks_list = [checkpoint, early_stopping]

history = training_model.fit_generator(
    batch_generator(text_train, count=train_batch_count),
    train_batch_count,
    max_queue_size=1, # no more than one queued batch in RAM
    epochs=EPOCHS,
    callbacks=callbacks_list,
    validation_data=batch_generator(text_val, count=val_batch_count),
    validation_steps=val_batch_count,
    initial_epoch=0
)