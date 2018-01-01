import requests

import concurrent.futures

import bs4

import json

import os

import random

import sys

import gzip

import pickle

import copy

import re
def url_fix(urls):
  furls = set()
  for url in urls:
    try:
      if url[0] == '/':
        url = 'http://toyokeizai.net' + url
        furls.add(url)
        continue
    except Exception:
      continue
    if 'javascript' in url:
      continue
    if 'http://toyokeizai.net/' not in url:
      continue
    furls.add(url)
  return furls

def map1(arr):
  index, url = arr
  save_name = 'htmls/' + url.replace('/', '_')
  '''max length 128'''
  save_name = save_name[:128]
  if re.search(r"^http://toyokeizai.net", url) is None:
    return set()
  if os.path.exists(save_name) is True:
    return set()
  print( 'now url', url ) 
  headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
  try:
    r = requests.get(url, headers=headers)
  except Exception as ex:
    print(ex)
    return set()
  html = r.text
  #print(html)
  try:
    open( save_name, 'w' ).write( html )  
  except OSError as ex:
    print(ex)
    return set()
  try:
    soup = bs4.BeautifulSoup(r.text)
    urls = set()
    for a in soup.find_all('a', href=True):
      url = a['href']
      urls.add(url)
    return url_fix(urls)
  except Exception as ex:
    print(ex)
    return set()

urls = {'http://toyokeizai.net/'}
if '--resume' in sys.argv:
  urls = pickle.loads(gzip.decompress(open('urls.pkl.gz', 'rb').read()))

while True:
  arrs = [(index,url) for index,url in enumerate(urls)]
  random.shuffle(arrs)
  
  nexts = set()
  with concurrent.futures.ProcessPoolExecutor(max_workers=24) as exe:
    for urls in exe.map(map1, arrs):
      for url in urls:
        nexts.add(url)
  #for arr in arrs:
  #  for url in map1(arr):
  #    nexts.add(url) 
  print(nexts)
  urls = copy.copy(nexts)
  #sys.exit()
