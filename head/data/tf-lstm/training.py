# Importing required modules
import json
import string
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, Flatten

# Importing the dataset
with open('intents.json') as intents:
    data = json.load(intents)

# Getting all the data to list
tags = []
patterns = []
responses = {}
for intent in data['intents']:
    responses[intent['tag']] = intent['responses']
    for lines in intent['patterns']:
        patterns.append(lines)
        tags.append(intent['tag'])

# Converting to dataframe
data = pd.DataFrame({"patterns": patterns,
                     "tags": tags})

# Removing punctuations
data['patterns'] = data['patterns'].apply(lambda wrd: [ltrs.lower() for ltrs in wrd if ltrs not in string.punctuation])
data['patterns'] = data['patterns'].apply(lambda wrd: ''.join(wrd))
data.to_csv('intents_processed.csv', index=False)

# Tokenize the data
tokenizer = Tokenizer(num_words=2000)
tokenizer.fit_on_texts(data['patterns'])
train = tokenizer.texts_to_sequences(data['patterns'])

# Apply padding
x_train = pad_sequences(train)

# Encoding the outputs
le = LabelEncoder()
y_train = le.fit_transform(data['tags'])

# Input length
input_shape = x_train.shape[1]

# Define vocabulary
vocabulary = len(tokenizer.word_index)
print("Number of unique words : ", vocabulary)
# Output length
output_length = le.classes_.shape[0]
print("Output length: ", output_length)

# Creating the model
i = Input(shape=(input_shape,))
x = Embedding(vocabulary + 1, 10)(i)
x = LSTM(10, return_sequences=True)(x)
x = Flatten()(x)
x = Dense(output_length, activation="softmax")(x)
model = Model(i, x)

# Compiling the model
model.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=['accuracy'])

# Training the model
train = model.fit(x_train, y_train, epochs=200)

# Saving the model
model.save("model.h5", train)
