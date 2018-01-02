
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
    try:
      obj = pickle.loads(db[key])
    except KeyError as ex:
      continue
    except UnicodeDecodeError as ex:
      continue
    #print(obj)
    title = obj["title"]
    subtitle = obj["subtitle"]
    terms = m.parse(obj["body"]).strip()
    for term in set(terms.split()):
      if term_docfreq.get(term) is None:
        term_docfreq[term] = 0.0
      term_docfreq[term] += 1.0

open("term_docfreq.pkl", "wb").write( pickle.dumps(term_docfreq) )
