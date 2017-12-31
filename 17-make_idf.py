
import glob

import dbm

import pickle

import MeCab

from collections import Counter

m = MeCab.Tagger("-Owakati")

term_docfreq = {}
for name in glob.glob("parsed_dbms/16-parsed_*.dbm"):
  print(name)
  db = dbm.open(name)
  for key in db.keys():
    obj = pickle.loads(db[key])
    #print(obj)
    subtitle = obj["subtitle"]
    terms = m.parse(obj["body"]).strip()
    for term in set(terms.split()):
      if term_docfreq.get(term) is None:
        term_docfreq[term] = 0.0
      term_docfreq[term] += 1.0

open("term_docfreq.pkl", "wb").write( pickle.dumps(term_docfreq) )