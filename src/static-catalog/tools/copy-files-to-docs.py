#!/usr/bin/env python

import argparse
import glob
import os
import pathlib
import subprocess
import shutil
import sys
from typing import Any

from common import (
    error,
    info,
    make_directories,
    warning,
)

parser = argparse.ArgumentParser(
    prog="copy-files-to-docs",
    description="Copies the JS and JSON catalog files to the website directory.",
    epilog="",
)
parser.add_argument(
    "-v",
    "--verbose",
    help="Verbosity level for output. Higher numbers result in more details.",
    type=int,
    default=0,
)

parser.add_argument(
    "--js-source",
    help="Source directory for the JS and JSON files.",
    required=True,
)
parser.add_argument(
    "--js-target",
    help="Target directory under the website root directory for the JS and JSON files.",
    required=True,
)

parser.add_argument(
    "--md-source",
    "--markdown-source",
    help="Source directory for the markdown files.",
    required=True,
)
parser.add_argument(
    "--md-target",
    "--markdown-target",
    help="Target directory for the markdown files directories. Defaults to 'docs'.",
    default='docs',
)

args = parser.parse_args(sys.argv[1:])

js_source_path = pathlib.Path(args.js_source)
if not js_source_path.exists():
    error(f"The source directory for the JS and JSON files, {js_source_path}, wasn't found.")

md_source_path = pathlib.Path(args.md_source)
if not md_source_path.exists():
    error(f"The source directory for the markdown files, {md_source_path}, wasn't found.")

js_target_path = pathlib.Path(args.js_target)
md_target_path = pathlib.Path(args.md_target)

# Remove the existing JS target path, but DON'T delete the markdown target path,
# which is likely .../docs!
def rmtree_onerror(func, path, exec_info):
  if exec_info[0] is FileNotFoundError:
    info(f"Ignoring missing path: {path}")
    return
  elif exec_info[0] is PermissionError:
    warning(f"Failed to remove protected path: {path}")
  raise exec_info[1]

if js_target_path.exists():
  shutil.rmtree(js_target_path, onerror=rmtree_onerror)

# Create the JS target path directory, which should now not exist.
#js_target_path.mkdir(parents=True)

# Copy just the .js files, not the .json files to the target.
shutil.copytree(js_source_path, js_target_path, ignore=shutil.ignore_patterns('*.json'))

# Create the markdown target path directory, which probably already exists!
md_target_path.mkdir(parents=True, exist_ok=True)

# Copy the directories for the markdown files to the website root directory.
new_markdown_dirs = []
for d in glob.iglob(args.md_source+'/*'):
  src=pathlib.Path(d)
  old=pathlib.Path(md_target_path, src.stem)
  new_markdown_dirs.append(src.stem)
  shutil.rmtree(old, onerror=rmtree_onerror)
  src.copy_into(md_target_path)


info(f"JavaScript files in {js_target_path}:")
info("  Directories:")
for f in glob.iglob(args.js_target+"/**", recursive=True):
  fp = pathlib.Path(f)
  if fp.is_dir():
    info("    "+f)
info("  Any non .js files?")
for f in glob.iglob(args.js_target+"/**", recursive=True):
  fp = pathlib.Path(f)
  if fp.is_file() and fp.suffix != '.js':
    info("    "+f)

info("")
info(f"Markdown files in {new_markdown_dirs} under {md_target_path}:")
info("  Directories:")
for d in new_markdown_dirs:
  for f in glob.iglob(f"{args.md_target}/{d}/**", recursive=True):
    fp = pathlib.Path(f)
    if fp.is_dir():
      info("    "+f)
info("  Any non .md or .markdown files?")
for d in new_markdown_dirs:
  for f in glob.iglob(f"{args.md_target}/{d}/**", recursive=True):
    fp = pathlib.Path(f)
    if fp.is_file() and fp.suffix != '.md' and fp.suffix != '.markdown':
      info("    "+f)

