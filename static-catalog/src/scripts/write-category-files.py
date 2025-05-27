#!/usr/bin/env python
from datetime import datetime, timezone
import argparse, json, os, pathlib, psutil, re, shutil, subprocess, sys

today = datetime.today().strftime("%Y-%m-%d")

# Default output directories:
def_root_dir_json   = f'./data/json/processed/{today}'
def_root_dir_md     = f'./markdown/processed/{today}'
def_categories_file = './data/reference/keyword-categories.json'

parser = argparse.ArgumentParser(
                    prog='write-category-files',
                    description='Writes dataset listing files by topics (keywords), JSON and markdown',
                    epilog='')
parser.add_argument('--no-json',
                    help="Skip writing the JSON and JS files.",
                    action='store_true')  # on/off flag
parser.add_argument('--no-markdown', '--no-md',
                    help="Skip writing the markdown files.",
                    action='store_true') 
parser.add_argument('--json-dir',
                    help=f"Write the JSON and JavaScript files to this directory. (default: {def_root_dir_json})",
                    default=def_root_dir_json)
parser.add_argument('--markdown-dir',
                    help=f"Write the markdown files to this directory. (default: {def_root_dir_json})",
                    default=def_root_dir_md)
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
  return re.sub("""[-\\s,./|'"()]+""", '_', str)

def print_metadata(label, keyword, title, alt_keywords, like_clause, context, indent_count=0):
  if args.verbose > 0:
    alt_keywords_str = ''
    if alt_keywords and len(alt_keywords) > 0:
     alt_keywords_str = f", Alt keywords = {[kw['keyword'] for kw in alt_keywords]}"
    like_clause_str = ''
    if like_clause and len(like_clause) > 0:
      like_clause_str = f", 'like' clause = {like_clause}"
    context_str = ''
    if context and len(context) > 0:
      context_str = f", Context = {context}"
    print(f"{indent_count*'  '}{label}: Keyword = {keyword}, Title = {title}{alt_keywords_str}{context_str}{like_clause_str}")

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
  title        = make_title(dict)
  alt_keywords = dict.get('alt-keywords', [])
  like_clause  = dict.get('like-clause')
  context      = dict.get('context', "")
  return keyword, title, alt_keywords, like_clause, context

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

def write_all_categories_index_js_file(cat_file: str):
  """
  Writes a JS version of the input categories file into the same
  directory as that file. 
  """
  # Extract the full path without the extension. This approach doesn't
  # assume ".json" is the categories file name extension. It also 
  # correctly handles directories in the path with nested ".".
  js_file = os.path.splitext(cat_file)[0] + ".js"
  with open(cat_file, 'r') as index:
    with open(js_file, 'w') as js:
      print(f"const global_categories_index = ", file=js)
      for line in index:
        print(line.rstrip(), file=js)
      print(";", file=js)

def write_js_file(json_file, js_file, var_name):
  """
  Read the input JSON file and create and write a corresponding JS file.
  """
  with open(json_file, 'r') as json:
    with open(js_file, 'w') as js:
      print(f"const {var_name} = ", file=js)
      for line in json:
        print(line.rstrip(), file=js)
      print(";", file=js)

def write_topic_json_js(directory, keyword, title, parent_keyword, parent_title, ancestor_path, alt_keywords, like_clause, context):
  """
  Runs a duckdb query to extract the topic/keyword data and write it to a JSON file, 
  and then convert that file to a JavaScript file for importing into the web pages.
  Note: We don't write _all_ the keywords, because some lists are huge. The largest is ~8000!
  """
  ancestor_prefix = ancestor_path.replace('/', '_')
  query_prefix    = make_keyword_query(keyword, like_clause)
  query_suffix    = [f" OR {make_keyword_query(kw['keyword'], None)}" for kw in alt_keywords]
  kw_query        = f"{query_prefix}{' '.join(query_suffix)}"
  js_output       = f"{directory}/{make_var_name(keyword)}.js"
  json_output     = f"{js_output}on"
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
    description,
    5 AS first_N,
    keywords[0:5] AS first_N_keywords,
    len(keywords) > 5 AS keywords_longer_than_N
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

  write_js_file(json_output, js_output, 
    make_var_name(f'data_for_{ancestor_prefix}_{keyword}'))

def make_alt_keywords_str(alt_keywords, delim=' '):
  if alt_keywords and len(alt_keywords):
    return delim.join([k['keyword'] for k in alt_keywords])
  else:
    return ''

def make_md_link(dict, mid_path, css_class="", use_hash=False):
  hash=''
  if use_hash:
    hash='#'
  css_class_str = ''
  if len(css_class) > 0:
    css_class_str=f'{{:class="{css_class}"}}'
  return f'[{make_title(dict)}]({{{{site.baseurl}}}}/{mid_path}/{hash}{dict["keyword"]}){css_class_str}'

def write_category_markdown(
  directory, 
  keyword, 
  title, 
  parent_keyword, 
  parent_title, 
  grand_parent_keyword, 
  grand_parent_title, 
  alt_keywords, 
  context,
  subcategories, 
  topics):
  md_output_file = f"{directory}/{keyword}.markdown"    
  with open(md_output_file, 'w') as md_out:
    alt_tags_str = make_alt_keywords_str(alt_keywords, delim='|')
    # WARNING: do not put the --- on a new line after the """! It adds a blank line at
    # the top of the markdown file and Jekyll simply ignores the whole file and doesn't
    # render it!!
    cleaned_keyword  = make_var_name(keyword)
    md_content_start = f"""---
name: {title}
tag: {keyword}
cleaned_tag: {cleaned_keyword}
parent_tag: {parent_keyword}
parent_title: {parent_title}
grand_parent_tag: {grand_parent_keyword}
grand_parent_title: {grand_parent_title}
alt_tags: {alt_tags_str}
subcategories: {'|'.join([s['keyword'] for s in subcategories])}
---

<div>
{context}
</div>

"""
    print(md_content_start, file=md_out)

    if subcategories and len(subcategories) > 0:
      subs_links_btns = [make_md_link(s, f'{parent_keyword}/{cleaned_keyword}', css_class="category-btn") for s in subcategories]
      print("#### Subcategories\n", file=md_out)
      print(' '.join(subs_links_btns), file=md_out)
      print('\n')

    if topics and len(topics) > 0:
      topics_links_btns = [make_md_link(t, f'{parent_keyword}/{cleaned_keyword}', css_class="topic-btn", use_hash=True) for t in topics]
      print("#### Keywords", file=md_out)
      print(' '.join(topics_links_btns), file=md_out)

def write_topic_markdown(
    directory, 
    keyword, 
    title, 
    parent_keyword, 
    parent_title, 
    grand_parent_keyword, 
    grand_parent_title, 
    ancestor_path, 
    alt_keywords, 
    like_clause, 
    context):
  ancestor_prefix  = ancestor_path.replace('/', '_')
  cleaned_keyword  = make_var_name(keyword)
  md_output_file   = f"{directory}/{ancestor_prefix}_{cleaned_keyword}.markdown"    
  alt_tags_str     = make_alt_keywords_str(alt_keywords)
  alt_keywords_str = make_alt_keywords_str(alt_keywords, delim="|")
  # WARNING: do not put the --- on a new line after the """! It adds a blank line at
  # the top of the markdown file and Jekyll simply ignores the whole file and doesn't
  # render it!!
  md_content = f"""---
name: {title}
tag: {keyword}
cleaned_tag: {cleaned_keyword}
parent_tag: {parent_keyword}
parent_title: {parent_title}
grand_parent_tag: {grand_parent_keyword}
grand_parent_title: {grand_parent_title}
alt_tags: {alt_tags_str}
---

{{% include data-table-template.html 
  keyword="{keyword}" 
  cleaned_keyword="{cleaned_keyword}" 
  title="{title}"
  ancestor_path="{ancestor_path}" 
  parent_title = "{parent_title}"
  grand_parent_title = "{grand_parent_title}"
  alt_keywords="{alt_keywords_str}"
  context="{context}"
%}}
"""
  with open(md_output_file, 'w') as md_out:
    print(md_content, file=md_out)

def process_topic(topic, parent_keyword, parent_title, grand_parent_keyword, grand_parent_title, ancestor_path, md_dir, json_dir, indent_count=0):
  keyword, title, alt_keywords, like_clause, context = \
    get_data(topic)
  print_metadata("Topic", keyword, title, alt_keywords, like_clause, context, indent_count)
  if args.no_markdown == False:
    write_topic_markdown(md_dir, keyword, title, parent_keyword, parent_title, grand_parent_keyword, grand_parent_title, ancestor_path, alt_keywords, like_clause, context)
  if args.no_json == False:
    write_topic_json_js(json_dir, keyword, title, parent_keyword, parent_title, ancestor_path, alt_keywords, like_clause, context)

if __name__ == "__main__":

  if is_process_running('duckdb'):
    error("It appears that 'duckdb' is already running. Please stop it then rerun this script.")

  print("\n**** NOTE: This program runs for several minutes! (Invoke with '-v 1' to see progress.) ****\n")

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

  if args.no_markdown == False:
    make_directories(args.markdown_dir, deletefirst=True)
  if args.no_json == False:
    make_directories(args.json_dir, deletefirst=True)
  # We aren't currently using this:
  # write_all_categories_index_js_file(args.cat_file)

  categories_list = args.categories
  user_specified_categories = categories_list and len(categories_list) > 0
  if user_specified_categories and args.verbose > 0:
      print(f"Processing only the user-specified categories: {', '.join(categories_list)}")

  for category in categories:
    category_keyword, category_title, category_alt_keywords, category_like_clause, category_context = \
      get_data(category)
    if user_specified_categories and category_keyword not in categories_list:
      continue

    print_metadata("Category", category_keyword, category_title, category_alt_keywords, category_like_clause, category_context, indent_count=0)

    category_var_name = make_var_name(category_keyword)
    category_path     = category_var_name
    category_md_dir   = f"{args.markdown_dir}/_{category_var_name}" # will be moved to "docs"
    category_json_dir = f"{args.json_dir}/{category_var_name}"
    if args.no_markdown == False:
      make_directories(category_md_dir,   deletefirst=False)
    if args.no_json == False:
      make_directories(category_json_dir, deletefirst=False)

    category_topics = category.get('topics', [])
    category_subcategories = category.get('subcategories', [])

    if args.no_markdown == False:
      write_category_markdown(category_md_dir, category_keyword, category_title, 'catalog', 'Catalog', None, None, category_alt_keywords, category_context,
      category_subcategories, category_topics)

    for topic in category_topics:
      process_topic(topic, category_var_name, category_title, category_keyword, None, category_path, category_md_dir, category_json_dir, indent_count=1)

    for subcategory in category_subcategories:
      subcategory_keyword, subcategory_title, subcategory_alt_keywords, subcategory_like_clause, subcategory_context = \
        get_data(subcategory)
      print_metadata("Subcategory", subcategory_keyword, subcategory_title, subcategory_alt_keywords, subcategory_like_clause, subcategory_context, indent_count=1)

      subcategory_var_name = make_var_name(subcategory_keyword)
      subcategory_key      = subcategory_var_name
      ancestor_path        = f"{category_path}/{subcategory_var_name}"
      subcategory_md_dir   = category_md_dir # same as category -- hack.
      subcategory_json_dir = f"{category_json_dir}/{subcategory_var_name}"
      if args.no_markdown == False:
        make_directories(subcategory_md_dir, deletefirst=False)
      if args.no_json == False:
        make_directories(subcategory_json_dir, deletefirst=False)

      for topic in subcategory.get('topics', []):
        process_topic(topic, subcategory_key, subcategory_title, category_keyword, category_title, ancestor_path, subcategory_md_dir, subcategory_json_dir, indent_count=2)
