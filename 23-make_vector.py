import json
import numpy as np
import sys
import gzip
import pickle
obj = json.loads(open("pair.json").read())

if "--step1" in sys.argv: # make char index
  title_char_index = {}
  bow_term_index = {}
  for url, val in obj.items():
    title, bow = val
    title = "".join(title)
    print(title, bow)

    for char in title:
      if title_char_index.get(char) is None:
        title_char_index[char] = len(title_char_index)
    
    for term in bow.keys():
      if bow_term_index.get(term) is None:
        bow_term_index[term] = len(bow_term_index)

  open("title_char_index.json", "w").write( json.dumps(title_char_index, ensure_ascii=False, indent=1) )
  open("bow_term_index.json", "w").write( json.dumps(bow_term_index, ensure_ascii=False, indent=1) )

if "--step2" in sys.argv:
  title_char_index = json.loads(open("title_char_index.json").read())
  bow_term_index = json.loads(open("bow_term_index.json").read())

  title_char_index["<EOS>"] = len(title_char_index)

  chunk, count = [], 0
  for url, val in obj.items():
    title, bow = val
    title = "".join(title)
    print(title, bow)

    output_base = []
    for i in range(0, 30): 
      ba = [0.0]*len(title_char_index)
      try:
        char = title[i]
        index = title_char_index[char]
        ba[i] = 1.0
      except IndexError as ex:
        ba[ title_char_index["<EOS>"] ] = 1.0
      output_base.append(ba)
    print(len(output_base)) 

    input_base = [0.0]*len(bow_term_index)
    for term, score in bow.items():
      print(term, score)
      input_base[ bow_term_index[term] ] = score

    chunk.append( (output_base, input_base) ) 
    print(len(chunk))
    if len(chunk) >= 1000:
      open("dataset/{:09d}.pkl.gz".format(count), 'wb').write( gzip.compress(pickle.dumps(chunk)) )
      count += 1
      chunk = []
  open("dataset/{:09d}.pkl.gz".format(count), 'wb').write( gzip.compress(pickle.dumps(chunk)) )

