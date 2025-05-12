#!/usr/bin/env zsh

. src/scripts/common.sh

timestamp=$(now --ymd)
base=./data/json/processed/$timestamp/languages
for json_file in $base/*.json
do
  js_file=${json_file%on}
  language1=${js_file#$base/hf_}
  language=${language1%.js}
  echo "Writing $js_file for $language"
  echo "var data_for_$language = [" > $js_file
  first_line=true
  cat $json_file | while read line
  do
    if $first_line
    then
      first_line=false
    else
      printf ",\n" >> $js_file
    fi
    printf "%s" "$line" >> $js_file
  done
  echo "\n];" >> $js_file
done

ls -l $base
