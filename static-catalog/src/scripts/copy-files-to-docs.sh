#!/usr/bin/env zsh

# Should run from the project root directory. The following hack
# tries to handle running in the root or static-catalog directories.
DIR=$(dirname $0)
ROOT=$(echo $DIR | sed -e 's?/*src/scripts/*??')
SC_DIR="static-catalog"
[[ $ROOT =~ static-catalog ]] || SC_DIR="."

. $SC_DIR/src/scripts/common.sh

[[ -d "$SC_DIR" ]] || error "Run this script in the repo root directory."

ymd=$(date +"%Y-%m-%d")
def_js_source_root="$SC_DIR/data/json/processed"
def_js_source="$def_js_source_root/$ymd"
def_md_source_root="$SC_DIR/markdown/processed"
def_md_source="$def_md_source_root/$ymd"
def_js_target="$SC_DIR/../docs/files/data/catalog"
def_md_target="$SC_DIR/../docs"

help() {
  cat <<EOF
$SCRIPT [options]
where the options are:
-h | --help               Print this message and exit.
-n | --noop               Print the commands, but don't execute them.
-v | --verbose N          Print more verbose output about what is being done. 
                          N = to 5, where smaller values mean more output.
-y | --ymd YYYY-MM-DD     Instead of the YMD in $def_js_source, use the specified date.
--js-source SRC_DIR       Where to read the source JS files (default: $def_js_source)
--md-source SRC_DIR       Where to read the source markdown files (default: $def_md_source)
--js-target TARGET_DIR    Where to write the JS files (default: $def_js_target)
--md-target TARGET_DIR    Where to write the markdown files (default: $def_md_target)
EOF
}

js_source=$def_js_source
js_target=$def_js_target
md_source=$def_md_source
md_target=$def_md_target
while [[ $# -gt 0 ]]
do
  case $1 in
    -h|--help)
      help
      exit 0
      ;;
    -n|--noop)
      NOOP=info
      ;;
    -v|--verbose)
      shift
      set_log_level_by_number $1
      ;;
    -y|--ymd)
      shift
      js_source=$def_js_source_root/$1
      md_source=$def_md_source_root/$1
      ;;
    --js-source)
      shift
      js_source=$1
      ;;
    --js-target)
      shift
      js_target=$1
      ;;
    --md-source)
      shift
      md_source=$1
      ;;
    --md-target)
      shift
      md_target=$1
      ;;
    *)
      error "Unrecognized argument: $1"
      ;;
  esac
  shift
done

info "$SCRIPT:"
info "  JS source:       $js_source"
info "  JS target:       $js_target"
info "  Markdown source: $md_source"
info "  Markdown target: $md_target"

$NOOP rm -rf $js_target
$NOOP mkdir $js_target
$NOOP cp -r $js_source/* $js_target
$NOOP find $js_target -name '*.json' -exec rm {} \;

# DON'T delete $md_target, which is likely ../docs!
md_dirs=()
for d in $md_source/*
do
  d2=$(basename $d)
  md_dirs+=($d2)
  if [[ -n $d2 ]]
  then
    $NOOP rm -rf $md_target/$d2
    $NOOP cp -r $md_source/$d2 $md_target/$d2
  fi
done

info "In $js_target..."
info "Any non .js files in $js_target?"
$NOOP find $js_target -type f -not -name '*.js'
info "Directories under $js_target:"
$NOOP find $js_target -type d
info "Size of $js_target:"
$NOOP du -hs $js_target

for md_dir in $md_dirs
do
  md_tdir=$md_target/$md_dir
  info "In $md_tdir: ..."
  info "Any non .markdown files in $md_tdir?"
  $NOOP find $md_tdir -type f -not -name '*.markdown'
  info "Directories under $md_tdir:"
  $NOOP find $md_tdir -type d
  info "Size of $md_tdir:"
  $NOOP du -hs $md_tdir
done
