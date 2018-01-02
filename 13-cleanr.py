import glob

import re

import os
for name in glob.glob("htmls/*"):
  if re.search(r"^htmls/http:__toyokeizai.net_articles", name) is None:
    print(name)
    os.remove(name)

