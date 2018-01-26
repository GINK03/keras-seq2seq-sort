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

def CBRD(inputs, filters=64, kernel_size=3, droprate=0.5):
  x = Conv1D(filters, kernel_size, padding='same',
            kernel_initializer='random_normal')(inputs)
  x = BatchNormalization()(x)
  x = Activation('relu')(x)
  return x

input_tensor = Input( shape=(1, 3135) )

enc = input_tensor
enc = Flatten()(enc)
enc = Dense(3135, activation='relu')(enc)
enc = RepeatVector(30)(enc)

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

class epoch:
  def __init__(self):
    self.stat = [50, 30, 20, 10, 1]
  def get(self):
    try:  
      return self.stat.pop(0)
    except Exception as ex:
      return 1

if '--train' in sys.argv:
  char_index = json.loads(open('char_index.json').read())
  char_index["<EOS>"] = len(char_index)
  index_char = {index:char for char, index in char_index.items()}
 
  count = 0
  ep = epoch()
  if '--resume' in sys.argv:
    model_file = sorted(glob.glob('models/*.h5')).pop() 
    print(model_file)
    model.load_weights(model_file)
  for i in range(500):
    for name in sorted(glob.glob("dataset/*"))[:1]:
      count += 1
      chunk = pickle.loads(gzip.decompress(open(name, "rb").read()))

      X, y = [], []
      for outputs, inputs in chunk:
        X.append([inputs])
        y.append(outputs)

        # pred = [index_char[np.argmax(ip)] for ip in outputs]
        # print(pred)
      X, y = np.array(X), np.array(y)

      batch_size = random.randint(64, 80)
      model.optimizer = random.choice([Adam()])
      model.fit(X, y, epochs=50, batch_size=batch_size)
    if count%1 == 0:
      model.save_weights("models/{:09d}.h5".format(count))

if '--predict' in sys.argv:
  char_index = json.loads(open('char_index.json').read())
  char_index["<EOS>"] = len(char_index)
  index_char = {index:char for char, index in char_index.items()}
  model_file = sorted(glob.glob('models/*.h5')).pop() 
  print(model_file)
  model.load_weights(model_file)

  X, y = [], []
  chunk = pickle.loads(gzip.decompress(open("dataset/000000000.pkl.gz", "rb").read()))
  for outputs, inputs in chunk:
    X.append([inputs])
    y.append(outputs)
  X, y = np.array(X), np.array(y)
  yps = model.predict(X)
  for yp in yps.tolist():
    pred = "".join( [index_char[np.argmax(y)] for y in yp] )
    print(pred)
