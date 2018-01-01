import os 
import glob

import sys

import pickle

import dbm

import MeCab

from collections import Counter

import math

import re
term_docfreq = pickle.loads(open("term_docfreq.pkl","rb").read())
m = MeCab.Tagger("-Owakati")

max_tfidfs = {}
for name in glob.glob("parsed_dbms/16-parsed_*.dbm"):
  db = dbm.open(name)
  for key in db.keys():
    try:
      obj = pickle.loads(db[key])
    except Exception as ex:
      continue

    sub_terms = m.parse(obj["subtitle"]).strip().split()

    body_terms = dict(Counter(m.parse(obj["body"]).strip().split()))

    tfidf = {}
    for term, freq in body_terms.items():
      tfidf[term] = math.log(freq+1.0) / term_docfreq[term]

    for term, tfidf in sorted(tfidf.items(), key=lambda x:x[1]*-1):
      if max_tfidfs.get(term) is None:
        max_tfidfs[term] = 0
      max_tfidfs[term] = max([max_tfidfs[term], tfidf])
"""
数字を取り除き
top5000をインプットとして利用する
"""

use_terms = set()
for term, tfidf in sorted(max_tfidfs.items(), key=lambda x:x[1]*-1):
  if re.search(r"^\d{1,}$", term) is not None:
    continue
  print(term, tfidf)
  use_terms.add(term)
  if len(use_terms) >= 20000:
    break

open("use_terms.pkl", "wb").write( pickle.dumps(use_terms) )

