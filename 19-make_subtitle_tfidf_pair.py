import os 
import glob

import sys

import pickle

import dbm

import MeCab

from collections import Counter

import math

import re

import json
term_docfreq = pickle.loads(open("term_docfreq.pkl","rb").read())
use_terms = pickle.loads(open("use_terms.pkl", "rb").read())

m = MeCab.Tagger("-Owakati")

max_tfidfs = {}

pair = {} #dbm.open("pair.dbm", "c")
for name in glob.glob("parsed_dbms/16-parsed_*.dbm"):
  db = dbm.open(name)
  for key in db.keys():
    obj = pickle.loads(db[key])

    sub_terms = m.parse(obj["subtitle"]).strip().split()

    body_terms = { term:freq for term, freq in dict(Counter(m.parse(obj["body"]).strip().split())).items() if term in use_terms }

    tfidf = {}
    for term, freq in body_terms.items():
      tfidf[term] = math.log(freq+1.0) / term_docfreq[term]
    if tfidf == {}:
      continue

    pair[key.decode()] = [sub_terms, tfidf]

open("pair.json", "w").write( json.dumps(pair, indent=2, ensure_ascii=False) )
