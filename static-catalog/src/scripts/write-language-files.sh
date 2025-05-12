#!/usr/bin/env zsh

. src/scripts/common.sh

timestamp=$(now --ymd)
base=./data/json/processed/$timestamp/languages
mkdir -p $base
langs=(
  "arabic"
  "catalan"
  "chinese"
  "english"
  "french"
  "german"
  "hindi"
  "hungarian"
  "italian"
  "japanese"
  "korean"
  "portuguese"
  "russian"
  "spanish"
  "turkish"
  "vietnamese"
)
for lang in ${langs[@]}
do
  output=$base/hf_$lang.json
  cat <<EOF | duckdb croissant.duckdb
  COPY (
    SELECT 
      name,
      license,
      language,
      url,
      creator_name,
      creator_url,
      description
    FROM hf_languages
    WHERE language_keyword = '$lang'
  ) TO '$output';
EOF
  # printf "%15s: wc output = %s\n" "$lang" "$(wc $output)"
done
ls -al $base
