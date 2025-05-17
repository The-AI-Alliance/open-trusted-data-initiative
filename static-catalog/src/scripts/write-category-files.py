#!/usr/bin/env python
from datetime import datetime, timezone
import argparse, json, os, pathlib, shutil, subprocess, sys

today = datetime.today().strftime("%Y-%m-%d")

# Default output directories:
def_root_dir_md     = f'./markdown/processed/{today}'
def_root_dir_json   = f'./data/json/processed/{today}'
def_categories_file = './data/reference/keyword-categories.json'

parser = argparse.ArgumentParser(
                    prog='write-category-files',
                    description='Writes dataset listing files by topics (keywords), JSON and markdown',
                    epilog='')
parser.add_argument('--no-json',
                    help="Skip writing the JSON files.",
                    action='store_true')  # on/off flag
parser.add_argument('--no-markdown', '--no-md',
                    help="Skip writing the markdown files.",
                    action='store_true') 
parser.add_argument('--json-dir',
                    help=f"Write the JSON and JavaScript files to this directory. (default: {def_root_dir_json})",
                    default=def_root_dir_json)
parser.add_argument('--markdown-dir', '--md-dir',
                    help=f"Write the markdown files to this directory. (default: {def_root_dir_md})",
                    default=def_root_dir_md)
parser.add_argument('--categories',
                    help=f"Read the categories and topics from this file. (default: {def_categories_file})",
                    default=def_categories_file)
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

def load_json(filename: str):
  with open(filename) as f_in:
      return json.load(f_in)

def error(message: str):
  print(f"ERROR! {message}")
  sys.exit(1)

def make_title(dict) -> str:
  words = dict.get('name').split('-')
  alt   = ' '.join([word.capitalize() for word in words])
  return dict.get('title', alt)



# The categories are very high-level, with the "topics" in them somewhat
# arbitrary, but based on topics known to be in the data set. We use arrays
# for each topic to join together related topics, which will translate
# in WHERE keyword = 'a' OR keyword = 'b' ... query clauses.
# The extra "context" text is written as "content" to the generated markdown
# files that will be rendered before each table.
# For human-readable titles, etc., we convert a keyword like this:
#   foo-bar-baz ==> Foo Bar Baz
# For some topics, this is not the right thing to do, like acronyms,
# the "title" field in the JSON is used instead, when present.
# When a topic has a "like-clause" defined, it means the SQL query is constructed
# as "keyword LIKE '<like-clause>'" instead of "keyword = '<name>'". If defined,
# the "like-clause" has to include the appropriate "%" for desired query.
if args.verbose:
  print(f"Reading categories from {args.categories}...")

categories = load_json(args.categories)

for category in categories:
  category_name = category.get('name')
  if category_name == None: 
    error(f"category name not found! ({category.get('name')}) category keys = {category.keys()} category=\n{str(category)[:1000]}")
  category_title = make_title(category)
  category_context = category.get('context', "")
  subcategories = category.get('subcategories')
  if subcategories == None: 
    error(f"subcategories name not found for category {category_name}!")
  subcategory_names = [f"{make_title(sub)} (keyword: {sub.get('name')})" for sub in subcategories]
  if args.verbose:
    print(f"""
Category:      {category_name}
Title:         {category_title}
Context:       {category_context}
Subcategories: {subcategory_names}
""")
  continue
  
  base_dir_md   = f"{args.markdown_dir}/_{category}" # will be moved to "docs"
  base_dir_json = f"{args.json_dir}/{category}"
  if args.no_markdown == False:
    print(f"Writing markdown files to: {base_dir_md}")
    make_directories(base_dir_md, deletefirst=True)
  if args.no_json == False:
    print(f"Writing JSON and JavaScript files to: {base_dir_json}")
    make_directories(base_dir_json, deletefirst=True)
  
  for topics in categories[category]:
    if args.verbose:
      print(f"{category} -> {topics}")
    category_main_tag = topics[0]
    # Use a "special name", if defined or else just replace '-' with ' '
    # and capitalize the first letters of each word.
    category_name = special_names.get(
      category_main_tag, category_main_tag.replace('-', ' ').capitalize())

    if args.no_markdown == False:
      md_output_file = f"{base_dir_md}/{category_main_tag}.markdown"    
      # WARNING: do not put the --- on a new line after the """! It adds a blank line at
      # the top of the markdown file and Jekyll simply ignores the whole file and doesn't
      # render it!!
      md_content = f"""---
name: {category_name}
tag: {category_main_tag}
all-tags: {' '.join(topics)}
parent_tag: {category}
---
"""
      with open(md_output_file, 'w') as md_out:
        print(md_content, file=md_out)

    if args.no_json == False:
      query1      = "' OR keyword = '".join(topics)
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
    license_url,
    language,
    dataset_url,
    creator_name,
    creator_url,
    description
  FROM hf_expanded_metadata
  WHERE {cat_query}
) TO '{json_output}' (FORMAT json, ARRAY true);
"""
      try:
        # Open a new process with a pipe for stdin.
        command = 'zsh'
        # process = subprocess.Popen(command, stdin=subprocess.PIPE)
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
        print(f"Writing {js_output} for {category} category {category_main_tag}.")

      with open(json_output, 'r') as json:
        with open(js_output, 'w') as js:
          print(f"var data_for_{category_main_tag.replace('-', '_')} = ", file=js)
          for line in json:
            print(line.rstrip(), file=js)
          print(";", file=js)

