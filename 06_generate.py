#generate tweets
# arguments
# [1] weights from 1st lstm
# [2] weights from 2nf lstm
# [3] impact of first lstm with two digits
# [4] vocabulary
# [5] seed

import numpy as np
import string
import random

from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation

#import arguments if run as standalone
if __name__ == "__main__":
    import sys
    model0File = sys.argv[1]
    model1File = sys.argv[2]
    impactRatio = float(sys.argv[3])
    vocabFile = sys.argv[4]
    seed = sys.argv[5]


    LAYER_COUNT = 4
    HIDDEN_LAYERS_DIM = 512

def init_lstm(model0File, model1File, impactRatio, vocabFile, seed):
    #determine how many chars to generate in maximum
    count = 280

    global lengthMax
    lengthMax = count - len(seed)

    # get vocabulary
    with open(vocabFile, "r") as f:
        vocab = f.read()

    global characters
    characters = sorted(list(set(vocab)))

    global VOCABULARY_SIZE
    VOCABULARY_SIZE = len(characters)
    global characters_to_ix
    characters_to_ix = {c:i for i,c in enumerate(characters)}


    global impactCounter
    impactCounter= []


    impactRatioAbs = int(impactRatio * lengthMax)
    for i in range(impactRatioAbs):
        impactCounter.append(0)
    for i in range(lengthMax-impactRatioAbs):
        impactCounter.append(1)

    random.shuffle(impactCounter)

    ####################
    global model0
    model0 = Sequential()
    for i in range(LAYER_COUNT):
        model0.add(
                LSTM(
                    HIDDEN_LAYERS_DIM, 
                    return_sequences=True if (i!=(LAYER_COUNT-1)) else False,
                    batch_input_shape=(1, 1, VOCABULARY_SIZE),
                    stateful=True
                )
            )
    model0.add(Dense(VOCABULARY_SIZE))
    model0.add(Activation('softmax'))
    model0.compile(loss='categorical_crossentropy', optimizer="adam")

    model0.load_weights(
        model0File
    )

    ###################
    global model1
    model1 = Sequential()
    for i in range(LAYER_COUNT):
        model1.add(
                LSTM(
                    HIDDEN_LAYERS_DIM, 
                    return_sequences=True if (i!=(LAYER_COUNT-1)) else False,
                    batch_input_shape=(1, 1, VOCABULARY_SIZE),
                    stateful=True
                )
            )
    model1.add(Dense(VOCABULARY_SIZE))
    model1.add(Activation('softmax'))
    model1.compile(loss='categorical_crossentropy', optimizer="adam")

    model1.load_weights(
        model1File
    )

def sample(preds, temperature=1.0):
    """Helper function to sample an index from a probability array"""
    # from fchollet/keras
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def predict_next_char(model, current_char, diversity=1.0):
    """Predict the next character from the current one"""
    x = np.zeros((1, 1, VOCABULARY_SIZE))
    x[:,:,characters_to_ix[current_char]] = 1
    y = model.predict(x, batch_size=1)
    next_char_ix = sample(y[0,:], temperature=diversity)
    next_char = characters[next_char_ix]
    return next_char

def generate_text(model0, model1, seed="I am", count=140):
    """Generate characters from a given seed"""
    model0.reset_states()
    model1.reset_states()

    next_char = [None] * 2

    print("\n\n")

    for s in seed[:-1]:
        next_char[0] = predict_next_char(model0, s)
        next_char[1] = predict_next_char(model1, s)
    current_char = seed[-1]

    sys.stdout.write("["+seed+"]")

    for i in range(lengthMax):
        next_char[0] = predict_next_char(model0, current_char, diversity=0.5)
        next_char[1] = predict_next_char(model1, current_char, diversity=0.5)
        current_char = next_char[impactCounter[i]]
        if (current_char=="ß"):
            compare = ""
            for j in range(len(seed)+2):
                compare += " "
            for j in range(i):
                compare += str(impactCounter[j])
            print("\n"+compare)
            break
        sys.stdout.write(current_char)

    print("\n\n")

if __name__ == "__main__":
    init_lstm(model0File, model1File, impactRatio, vocabFile, seed)
    generate_text(
        model0,model1,
        seed=seed
    )