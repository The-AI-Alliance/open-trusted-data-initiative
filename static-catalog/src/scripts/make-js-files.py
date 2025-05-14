#!/usr/bin/env python

from datetime import datetime
import glob, os, re
from pathlib import Path

timestamp = datetime.now().strftime("%Y-%m-%d")
base = f"./data/json/processed/{timestamp}/"
groups = ...
for group in groups:
  json_files = glob.glob(f"{base}/{group}/hf_*.json")

  for json_file in json_files:
    dir = os.path.dirname(json_file)
    file_base = Path(json_file).stem
    js_file = f"{dir}/{file_base}.js"
    category = file_base[3:]

    print(f"Writing {js_file} for {group} category {category}.")

    with open(json_file, 'r') as json:
      with open(js_file, 'w') as js:
        print(f"var data_for_{group}_{category} = [", file=js)
        comma=''
        for line in json:
          print(f"{comma}\n  {line.rstrip()}", end='', file=js)
          comma=','
        print("\n];", file=js)
