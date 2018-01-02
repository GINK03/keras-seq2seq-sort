import bs4

import glob

import os

import dbm

import pickle

import re

import concurrent.futures


def _map(arr):
  key, names = arr
  db = dbm.open("parsed_dbms/16-parsed_{key:09d}.dbm".format(key=key), "c")
  for name in names:
    try:
      soup = bs4.BeautifulSoup(open(name).read(), "lxml")
      [s.extract() for s in soup('script')]
      
      title_parts = soup.find("div", {"class":"title-parts"})
      if title_parts is None:
        print(name.replace("_", "/"))
        continue

      title = title_parts.find("h1")
      
      subtitle = title_parts.find("h2")

      date = soup.find("meta", property="article:published_time")
      
      body = soup.find("div", {"id":"article-body-inner"})
      #print(name.replace("_","/"))
      key = name.split("/").pop().replace("_","/")
      val = { "title": title.text if title else None, 
              "subtitle": subtitle.text if subtitle else None,
              "date": date.get("content") if date else None,
              "body": body.text.strip() if body else None }
      db[ key ] = pickle.dumps(val)
    except Exception as ex:
      print(ex)

arrs = {}
for index, name in enumerate(glob.glob("htmls/*")):
  key = index%16
  if arrs.get(key) is None:
    arrs[key] = []
  arrs[key].append( name )
arrs = [(key, names) for key, names in arrs.items() ]
#_map(arrs[0])
#sys.exit()
with concurrent.futures.ProcessPoolExecutor(max_workers=16) as exe:
  exe.map(_map, arrs)
