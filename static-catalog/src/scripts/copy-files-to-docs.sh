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
  target="../docs/files/data/catalog/$group"
  rm -rf $target
  mkdir -p $target
  cp $source/*.js $target
done
for source in ./markdown/processed/$ymd/*
do
  group=$(basename $source)
  md_sources+=($group)
  echo "Markdown for group: $group"
  target="../docs/$group"
  rm -rf $target
  mkdir -p $target
  cp $source/*.markdown $target
done

echo "In ../docs/files/data/catalog/:"
for d in ${js_sources[@]}
do
  echo "../docs/files/data/catalog/$d:"
  ls -l ../docs/files/data/catalog/$d
done
echo
echo "In ../docs/_*"
for d in ${md_sources[@]}
do
  echo "../docs/$d:"
  ls -l ../docs/$d
done

