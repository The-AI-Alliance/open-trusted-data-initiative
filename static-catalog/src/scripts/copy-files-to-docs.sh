#!/usr/bin/env zsh
# run from the static-catalog directory!!

. src/scripts/common.sh

ymd=$(date +"%Y-%m-%d")
js_sources=()
md_sources=()
for source in ./data/json/processed/$ymd/*
do
  group=$(basename $source)
  js_sources+=($group)
  echo "JS for group: $group"
  cat_dir="../docs/files/data/catalog"
  target="$cat_dir/$group"
  rm -rf $target
  mkdir -p $target
  cp -r $source $cat_dir
  find $target -name '*.json' -exec rm {} \;
done

echo "In ../docs/files/data/catalog/:"
find ../docs/files/data/catalog/ -ls
done
find ../docs/files/data/catalog -type d

