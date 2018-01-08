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
from keras.optimizers import SGD, Adam
from keras import backend as K
from keras.layers.wrappers import Bidirectional as Bi
from keras.layers.wrappers import TimeDistributed as TD

def CBRD(inputs, filters=64, kernel_size=3, droprate=0.5):
  x = Conv1D(filters, kernel_size, padding='same',
            kernel_initializer='random_normal')(inputs)
  x = BatchNormalization()(x)
  x = Activation('relu')(x)
  return x

input_tensor = Input( shape=(10, 2000) )

enc = input_tensor
enc = Dense(1024, activation="relu")( enc )
enc = Flatten()(enc)
encode = Dense(4024, activation="relu")( enc )

dec = RepeatVector(30)(encode)
dec = Bi(GRU(2647, return_sequences=True))(dec)
dec = TD(Dense(2647, activation='relu'))(dec)
decode  = TD(Dense(2647, activation='softmax'))(dec)


model = Model(inputs=input_tensor, outputs=decode)
model.compile(loss='categorical_crossentropy', optimizer='adam')

import pickle
import gzip
import numpy as np
import glob
import sys

if '--train' in sys.argv:
  for i in range(500):
    print(i)
    for name in glob.glob("dataset/*"):
      chunk = pickle.loads(gzip.decompress(open(name, "rb").read()))

      X, y = [], []
      for outputs, inputs in chunk:
        inputs =  np.array(inputs)
        inputs = inputs.reshape( (10, 2000) )
        #print( inputs.shape )
        X.append(inputs)
        outputs = np.array(outputs) 
        #print(outputs.shape)
        y.append(outputs)

      X, y = np.array(X), np.array(y)

      batch_size = random.randint(3, 64)
      model.fit(X, y, epochs=1, batch_size=batch_size)
      #break
    model.save_weights("models/{:09d}.h5".format(i))

if '--predict' in sys.argv:
  model_file = sorted(glob.glob('models/*.h5')).pop() 
  print(model_file)
  model.load_weights(model_file)

  X, y = [], []
  chunk = pickle.loads(gzip.decompress(open("dataset/000000000.pkl.gz", "rb").read()))
  for outputs, inputs in chunk:
    inputs =  np.array(inputs)
    inputs = inputs.reshape( (10, 2000) )
