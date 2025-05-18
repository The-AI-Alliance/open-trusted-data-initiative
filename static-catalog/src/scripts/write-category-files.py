#!/usr/bin/env python
from datetime import datetime, timezone
import argparse, json, os, pathlib, psutil, re, shutil, subprocess, sys

today = datetime.today().strftime("%Y-%m-%d")

# Default output directories:
def_root_dir_json   = f'./data/json/processed/{today}'
def_categories_file = './data/reference/keyword-categories.json'

parser = argparse.ArgumentParser(
                    prog='write-category-files',
                    description='Writes dataset listing files by topics (keywords), JSON and markdown',
                    epilog='')
parser.add_argument('--json-dir',
                    help=f"Write the JSON and JavaScript files to this directory. (default: {def_root_dir_json})",
                    default=def_root_dir_json)
parser.add_argument('--cat-file', '--categories-file',
                    help=f"Read the categories and topics from this file. (default: {def_categories_file})",
                    default=def_categories_file)
parser.add_argument('-c', '--categories',
                    help=f"Process these categories and their subcategories and topics. (default: read from {def_categories_file})",
                    nargs="*")
parser.add_argument('-v', '--verbose',
                    help="Verbosity level for output. Higher numbers result in more details.",
                    type=int,
                    default=0) 
args = parser.parse_args(sys.argv[1:])

def make_directories(path: str, deletefirst=False):
  new_dir_path = pathlib.Path(path)
  if deletefirst and new_dir_path.exists():
    shutil.rmtree(path)
  
  try:
      new_dir_path.mkdir(parents=True)
      # if args.verbose > 0:
      #   print(f"Directory '{new_dir_path}' created successfully.")
  except FileExistsError:
      if args.verbose > 1:
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

# Adapted from https://btechgeeks.com/python-check-if-a-process-is-running-by-name-and-find-its-process-id-pid/
def is_process_running(processName: str) -> bool:
  # Checking if there is any running process that contains the given name processName.
  #Iterate over the all the running process
  for proc in psutil.process_iter():
    try:
      # Check if process name contains the given name string.
      if processName.lower() in proc.name().lower():
        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
      pass
  return False;

def make_title(dict) -> str:
  title = dict.get('title')
  if title == None:
    words = dict.get('keyword').split('-')
    title = ' '.join([word.capitalize() for word in words])
  return title

def make_var_name(str: str) -> str:
  return re.sub("""[-\\s,./|'"()]""", '_', str)

def print_metadata(keyword, title, alt_tags, like_clause, context, indent_count=0):
  if args.verbose > 0:
    print(f"""
{indent_count*'  '}Keyword:          {keyword}
{indent_count*'  '}Title:            {title}
""")
    if alt_tags:
      print(f"{indent_count*'  '}'alt' tags:       {alt_tags}")
    if like_clause:
      print(f"{indent_count*'  '}'like' clause:    {like_clause}")
    print(f"{indent_count*'  '}Context:          {context}")

def get_data(dict):
  """
  From the input dictionary, extract the keyword, title, and context, 
  which are returned. Optionally print the values (args.verbose > 0).
  We know that some keywords contain "'", which will mess up string 
  creation, e.g., for queries, so we also replace all occurrences with "\\'".
  """
  keyword = dict.get('keyword')
  if keyword == None: 
    error(f"'keyword' not found! ({dict.get('keyword')}). Keys = {dict.keys()}")
  title       = make_title(dict)
  alt_tags    = dict.get('alt_tags', [])
  like_clause = dict.get('like_clause')
  context     = dict.get('context', "")
  return keyword, title, alt_tags, like_clause, context

def make_keyword_query(keyword, like_clause):
  """
  Normally just return the string 'keyword = {keyword}', but if
  the like_clause is not None, then return 'keyword LIKE {like_clause}',
  _or_ if the keyword contains "problematic" characters, like "'", 
  then convert those characters to "%" and return 'keyword LIKE {fixed}'.
  """
  query = ''
  if like_clause:
    query = f"keyword LIKE '{like_clause}'"
  elif "'" in keyword:
    fixed = keyword.replace("'", "%")
    query = f"keyword LIKE '{fixed}'"
  else:
    query = f"keyword = '{keyword}'"
  return query

def process_topic(directory, parent_keyword, topic, indent_count=0):
  keyword, title, alt_tags, like_clause, context = \
    get_data(topic)
  print_metadata(keyword, title, alt_tags, like_clause, context, indent_count)

  query_prefix = make_keyword_query(keyword, like_clause)
  query_suffix = [f"OR {make_keyword_query(kw, None)}" for kw in alt_tags]
  kw_query    = f"{query_prefix}{' '.join(query_suffix)}"
  js_output   = f"{directory}/hf_{make_var_name(keyword)}.js"
  json_output = f"{js_output}on"
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
  WHERE {kw_query}
) TO '{json_output}' (FORMAT json, ARRAY true);
"""
  if args.verbose > 1:
    print(f"Running query: {query}")

  try:
    # Open a new process with a pipe for stdin.
    command = 'zsh'
    # process = subprocess.Popen(command, stdin=subprocess.PIPE)
    encoded_string = query.encode('utf-8')
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
      shell=True, executable="/bin/zsh")

    # Communicate with the process. This sends data to stdin and returns data from stdout and stderr.
    output, error = process.communicate(input=encoded_string)

    if args.verbose > 1 and output:
      print(f"Output from creating file {json_output}: ", output.decode('utf-8'))
    if error:
      print(f"Error creating file {json_output}: ", error.decode('utf-8'))
      sys.exit(1)

  except Exception as e:
    print(f"An error occurred running the query to create the file {json_output}: {e}")
    sys.exit(1)
  
  # Write the corresponding JS file required.
  with open(json_output, 'r') as json:
    with open(js_output, 'w') as js:
      var_name = make_var_name(f'data_for_{parent_keyword}_{keyword}')
      print(f"var {var_name} = ", file=js)
      for line in json:
        print(line.rstrip(), file=js)
      print(";", file=js)

if __name__ == "__main__":

  if is_process_running('duckdb'):
    error("It appears that 'duckdb' is already running. Please stop it then rerun this script.")

  # The high-level categories and subcategories are somewhat arbitrary.
  # The "topics" are found in the data set. We use arrays
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
  if args.verbose > 0:
    print(f"Reading data from file: {args.cat_file}")
  categories = load_json(args.cat_file)

  categories_list = args.categories
  user_specified_categories = len(categories_list) > 0
  if user_specified_categories and args.verbose > 0:
      print(f"Processing only the user-specified categories: {', '.join(categories_list)}")

  for category in categories:
    category_keyword, category_title, category_alt_tags, category_like_clause, category_context = \
      get_data(category)
    if user_specified_categories and category_keyword not in categories_list:
      continue

    print_metadata(category_keyword, category_title, category_alt_tags, category_like_clause, category_context, indent_count=0)

    category_dir = f"{args.json_dir}/{make_var_name(category_keyword)}"
    make_directories(category_dir, deletefirst=True)

    for topic in category.get('topics', []):
      process_topic(category_dir, category_keyword, topic, indent_count=1)

    for subcategory in category.get('subcategories', []):
      subcategory_keyword, subcategory_title, subcategory_alt_tags, subcategory_like_clause, subcategory_context = \
        get_data(subcategory)
      print_metadata(subcategory_keyword, subcategory_title, subcategory_alt_tags, subcategory_like_clause, subcategory_context, indent_count=1)

      subcategory_dir = f"{category_dir}/{make_var_name(subcategory_keyword)}"
      make_directories(subcategory_dir, deletefirst=False)

      for topic in subcategory.get('topics', []):
        process_topic(subcategory_dir, f'{category_keyword}-{subcategory_keyword}', topic)
