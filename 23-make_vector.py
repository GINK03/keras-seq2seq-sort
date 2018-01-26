import json
import numpy as np
import sys
import gzip
import pickle

obj = json.loads(open("pair.json").read())

if "--step1" in sys.argv: # make char index
  char_index = {}
  for url, val in obj.items():
    title, boc = val
    title = "".join(title)
    print(title, boc)

    for char in title:
      if char_index.get(char) is None:
        char_index[char] = len(char_index)
    
  open("char_index.json", "w").write( json.dumps(char_index, ensure_ascii=False, indent=1) )

if "--step2" in sys.argv:
  char_index = json.loads(open("char_index.json").read())

  char_index["<EOS>"] = len(char_index)
  index_char = {index:char for char, index in char_index.items()}
  chunk, count = [], 0
  titles = set() 
  for url, val in obj.items():
    title, boc = val
    title = "".join(title)
    if title in titles:
      continue
    titles.add( title )
    print(title, boc)

    output_base = []
    for i in range(0, 30): 
      ba = [0.0]*len(char_index)
      try:
        char = title[i]
        #print("scan", char)
        index = char_index[char]
        ba[index] = 1.0
      except IndexError as ex:
        ba[ char_index["<EOS>"] ] = 1.0
      #print( index_char[ np.argmax(ba) ] )
      output_base.append(ba)
    #print(len(output_base)) 
    #print( title )
    print( [index_char[np.argmax(o)] for o in output_base] )

    input_base = [0.0]*len(char_index)
    for char,freq in boc.items():
      input_base[ char_index[char] ] = freq

    chunk.append( (output_base, input_base) ) 
    if len(chunk) >= 7000:
      open("dataset/{:09d}.pkl.gz".format(count), 'wb').write( gzip.compress(pickle.dumps(chunk)) )
      count += 1
      chunk = []
      break 
  #open("dataset/{:09d}.pkl.gz".format(count), 'wb').write( gzip.compress(pickle.dumps(chunk)) )

