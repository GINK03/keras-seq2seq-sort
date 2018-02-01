import pickle
import gzip
import numpy as np
import random
import os
import sys
import statistics
import glob
import re
import json
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model, load_model
from keras.layers import Lambda, Input, Activation, Dropout, Flatten, Dense, Reshape, merge
from keras.layers import Concatenate, Multiply, Conv1D, MaxPool1D, BatchNormalization, RepeatVector, GRU
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.normalization import BatchNormalization as BN
from keras.layers.core import Dropout
from keras.layers.noise import GaussianNoise as GN
from keras.optimizers import SGD, Adam, RMSprop
from keras import backend as K
from keras.layers.wrappers import Bidirectional as Bi
from keras.layers.wrappers import TimeDistributed as TD

input_tensor = Input( shape=(1, 3135) )

enc = input_tensor
enc = Flatten()(enc)
enc = RepeatVector(30)(enc)
enc = GRU(256, dropout=0.15, recurrent_dropout=0.1, return_sequences=True)(enc)
enc = TD(Dense(3000, activation='relu'))(enc)
enc = Dropout(0.25)(enc)

dec = Bi(GRU(512, dropout=0.30, recurrent_dropout=0.25, return_sequences=True))(enc)
dec = TD(Dense(3000, activation='relu'))(dec)
dec = Dropout(0.5)(dec)
dec = TD(Dense(3000, activation='relu'))(dec)
dec = Dropout(0.1)(dec)
decode  = TD(Dense(3135, activation='softmax'))(dec)


model = Model(inputs=input_tensor, outputs=decode)
model.compile(loss='categorical_crossentropy', optimizer='adam')

import pickle
import gzip
import numpy as np
import glob
import sys

if '--train' in sys.argv:
  char_index = json.loads(open('char_index.json').read())
  char_index["<EOS>"] = len(char_index)
  index_char = {index:char for char, index in char_index.items()}
 
  count = 0
  if '--resume' in sys.argv:
    model_file = sorted(glob.glob('models/*.h5')).pop() 
    print(model_file)
    model.load_weights(model_file)
  for i in range(500):
    X, y = [], []
    for name in random.sample(sorted(glob.glob("dataset/*"))[:50], 50):
      count += 1
      chunk = pickle.loads(gzip.decompress(open(name, "rb").read()))

      for outputs, inputs in chunk:
        X.append([inputs])
        y.append(outputs)

    X, y = np.array(X), np.array(y)

    batch_size = random.randint(64, 80)
    model.optimizer = random.choice([Adam(), SGD()])
    model.fit(X, y, epochs=100, batch_size=batch_size)
    if count%1 == 0:
      model.save_weights("models/{:09d}.h5".format(count))

if '--predict' in sys.argv:
  char_index = json.loads(open('char_index.json').read())
  char_index["<EOS>"] = len(char_index)
  index_char = {index:char for char, index in char_index.items()}
  model_file = sorted(glob.glob('models/000000350.h5')).pop() 
  print(model_file)
  model.load_weights(model_file)

  X, y = [], []
  chunk = pickle.loads(gzip.decompress(open(sorted(glob.glob("dataset/000000001.pkl.gz")).pop(), "rb").read()))
  for outputs, inputs in chunk:
    X.append([inputs])
    y.append(outputs)
  X, y = np.array(X), np.array(y)

  bs = []
  for xv in X.tolist():
    b = []
    for index, x in enumerate(xv[0]):
      #print(x)
      if x == 1.0:
        b.append( index_char[index] ) 
    bs.append( b )
  yps = model.predict(X)
  for yp, b in zip(yps.tolist(), bs):
    pred = "".join( [index_char[np.argmax(y)] for y in yp] )
    print(b)
    print(pred)
    print()
