#!/usr/bin/env python
from datetime import datetime, timezone
import argparse, os, pathlib, shutil, subprocess, sys

today = datetime.today().strftime("%Y-%m-%d")

# The groups are very high-level, with the categories in them somewhat
# arbitrary, but based on tags known to be in the data set. We use arrays
# for the categories to join together related concepts, which will translate
# in WHERE keyword = 'a' OR keyword = 'b' ... query clauses.

groups = {
  "language": [
    ["arabic"],
    ["catalan"],
    ["chinese"],
    ["english"],
    ["french"],
    ["german"],
    ["hindi"],
    ["hungarian"],
    ["italian"],
    ["japanese"],
    ["korean"],
    ["portuguese"],
    ["russian"],
    ["spanish"],
    ["turkish"],
    ["vietnamese"],
  ],
  "modality": [
    ["audio"],
    [
      "classification", 
      "zero-shot-classification", 
      "image-classification", 
      "text-classification", 
      "multi-class-classification", 
      "multi-label-classification", 
      "tabular-classification",
      "topic-classification", 
      "token-classification",
      "text-scoring"
    ],
    [
      "benchmark",
      "benchmarks"
    ],
    ["crowdsourced"],
    [
      "evaluation",
      "eval"
    ],
    ["expert-generated"],
    ["feature-extraction"],
    [
      "image",
      "image-segmentation",
      "image-to-image",
      "object-detection",
    ],
    ["image-to-text"],
    [
      "language-modeling", 
      "llm"
    ],
    ["machine-generated"],
    ["multilingual"],
    ["multiple-choice"],
    ["music"],
    ["named-entity-recognition"],
    [
      "nlp",
      "natural-language-processing",
      "natural-language-inference",
    ],
    [
      "question-answering",
      "closed-domain-qa",
      "extractive-qa",
      "qna",
      "q-and-a",
      "multiple-choice-qa",
      "open-domain-qa",
      "table-question-answering",
      "visual-question-answering",
    ],
    ["reasoning"],
    ["sentence-similarity"],
    ["sentence-transformers"],
    ["sentiment-analysis"],
    [
      "speech-recognition",
      "automatic-speech-recognition"
    ],
    [
      "summarization",
      "news-articles-summarization"
    ],
    ["synthetic"],
    ["test"],
    ["text", "monolingual"],
    [
      "text-generation",
      "text2text-generation"
    ],
    [
      "text-retrieval",
      "document-retrieval"
    ],
    ["text-to-image"],
    ["text-to-speech"],
    ["translation"],
    ["video"],
  ],
  "domain": [
    ["art"],
    ["biology"],
    ["chemistry"],
    ["climate"],
    ["code"],
    ["finance"],
    ["geospatial"],
    ["legal"],
    ["math"],
    ["medical"],
    [
      "robotics", 
      "lerobot"
    ],
    ["science"],
    ["time-series"],
    ["tutorial"],
    [
      "web",
      "webdataset"
    ],
  ],
}

# Some of the tags shouldn't simply be capitalized, but converted to upper case, e.g., acronyms,
# or otherwise treated differently.
special_names = {
  'llm': 'LLM',
  'nlp': 'NLP',
  'qna': 'QnA',
  'q-and-a': 'Q and A',
  'webdataset': 'Web Dataset',
}

parser = argparse.ArgumentParser(
                    prog='write-group-files',
                    description='Writes dataset listing files by keywords, JSON and markdown',
                    epilog='')
parser.add_argument('--no-json',
                    help="Skip writing the JSON files.",
                    action='store_true')  # on/off flag
parser.add_argument('--no-markdown', '--no-md',
                    help="Skip writing the markdown files.",
                    action='store_true') 
parser.add_argument('-v', '--verbose',
                    help="Show verbose output",
                    action='store_true') 
args = parser.parse_args(sys.argv[1:])

def make_directories(path: str, deletefirst=False):
  new_dir_path = pathlib.Path(path)
  if deletefirst and new_dir_path.exists():
    shutil.rmtree(path)
  
  try:
      new_dir_path.mkdir(parents=True)
      if args.verbose:
        print(f"Directory '{new_dir_path}' created successfully.")
  except FileExistsError:
      if args.verbose:
        print(f"Directory '{new_dir_path}' already exists.")
  except OSError as e:
      print(f"Error creating directory: {e}")
      sys.exit(1)

for group in groups.keys():
  if args.verbose:
    print(f"Working on group: {group}")
  
  base_dir_md   = f"./markdown/processed/{today}/_{group}" # will be moved to "docs"
  base_dir_json = f"./data/json/processed/{today}/{group}"
  if args.no_markdown == False:
    make_directories(base_dir_md, deletefirst=True)
  if args.no_json == False:
    make_directories(base_dir_json, deletefirst=True)
  
  for category_tags in groups[group]:
    if args.verbose:
      print(f"{group} -> {category_tags}")
    category_main_tag = category_tags[0]
    # Use a "special name", if defined or else just replace '-' with ' '
    # and capitalize the first letters of each word.
    category_name = special_names.get(
      category_main_tag, category_main_tag.replace('-', ' ').capitalize())

    if args.no_markdown == False:
      md_output_file = f"{base_dir_md}/{category_main_tag}.markdown"    
      # WARNING: do not put the --- on a new line after the """. It adds a blank line at
      # the top of the markdown file and Jekyll simply ignores the whole file!
      md_content = f"""---
name: {category_name}
tag: {category_main_tag}
tags: {', '.join(category_tags)}
parent_tag: {group}
---
"""
      with open(md_output_file, 'w') as md_out:
        print(md_content, file=md_out)

    if args.no_json == False:
      query1      = "' OR keyword = '".join(category_tags)
      cat_query   = f"keyword = '{query1}'"
      json_output = f"{base_dir_json}/hf_{category_main_tag}.json"
      js_output   = f"{base_dir_json}/hf_{category_main_tag}.js"
      query = f"""
duckdb croissant.duckdb
COPY (
  SELECT 
    name,
    keyword,
    license,
    language,
    url,
    creator_name,
    creator_url,
    description
  FROM hf_expanded_metadata
  WHERE {cat_query}
) TO '{json_output}';
"""

      try:
        command = 'zsh'
        # Open a new process with a pipe for stdin.
        process = subprocess.Popen(command, stdin=subprocess.PIPE)
        encoded_string = query.encode('utf-8')
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
          shell=True, executable="/bin/zsh")

        # Communicate with the process. This sends data to stdin and returns data from stdout and stderr.
        output, error = process.communicate(input=encoded_string)

        if output and args.verbose:
            print(f"Output creating file {json_output}: ", output.decode('utf-8'))
        if error:
            print(f"Error  creating file {json_output}: ", error.decode('utf-8'))
            sys.exit(1)

      except Exception as e:
        print(f"An error occurred running the query to create file {json_output}: {e}")
        sys.exit(1)

      # Write the corresponding JS file required.
      if args.verbose:
        print(f"Writing {js_output} for {group} category {category_main_tag}.")

      with open(json_output, 'r') as json:
        with open(js_output, 'w') as js:
          print(f"var data_for_{group}_{category_main_tag} = [", file=js)
          comma=''
          for line in json:
            print(f"{comma}\n  {line.rstrip()}", end='', file=js)
            comma=','
          print("\n];", file=js)

