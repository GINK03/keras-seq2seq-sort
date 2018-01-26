import os 
import glob

import sys

import pickle

import dbm

from collections import Counter

import math

import re

import json
term_docfreq = pickle.loads(open("term_docfreq.pkl","rb").read())
use_terms = pickle.loads(open("use_terms.pkl", "rb").read())

pair = {} #dbm.open("pair.dbm", "c")
for name in glob.glob("parsed_dbms/*.dbm"):
  db = dbm.open(name)
  for key in db.keys():
    try:
      obj = pickle.loads(db[key])
    except Exception as ex:
      continue
    if obj["title"] is None:
      continue
    chars = dict(Counter(list(obj["title"])))
    title = list(obj["title"])

    pair[key.decode()] = [title, chars]
    print(key.decode())

open("pair.json", "w").write( json.dumps(pair, indent=1, ensure_ascii=False) )

