import requests

import os

import glob

import concurrent.futures

import random
base = "http://toyokeizai.net/articles/-/{}"


def _map1(i):
  url = base.format(i)

  save_name = "htmls/" + url.replace("/", "_")

  if os.path.exists(save_name) is True:
    return None
  print(url)

  try:
    headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3248.0 Safari/537.36'}
    r = requests.get(url, headers=headers)
    #print(r.text)

    html = r.text

    open(save_name, "w").write( html )
  except Exception as ex:
    print(ex)

iss = [i for i in range(1, 203319)]
iss = random.sample(iss, len(iss))
with concurrent.futures.ProcessPoolExecutor(max_workers=32) as exe:
  exe.map(_map1, iss)
