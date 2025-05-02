#!/usr/bin/env zsh

# This script is a tool to generate the "boilerplate" Jekyll collection files
# representing the top-level categories of datasets.

declare -A tags
tags=(
  [language]="english, japanese, korean, arabic"
  [domain]="molecular-discovery, time-series, automation"
  [modality]="text, video, image, audio, multimedia"
)

write_file() {
  category=$1
  shift
  tag=$1
  lower_name="$(echo $tag | sed -e 's/-/ /g')"
  name="${(C)lower_name}"
  cat <<EOF
---
name: $name
tag: $tag
parent_tag: $category
---

The following datasets contain predominantly $name $category text.

| Name | URL | Comments |
| :--- | :-- | :------- |
| TODO | |

EOF
}


for category in ${(k)tags}
do
  echo "$category:"
  cat_dir="docs/_$category"
  rm -rf $cat_dir
  mkdir $cat_dir
  cat_tags=($(eval echo ${tags[$category]//, / }))
  for tag in "${cat_tags[@]}"
  do
    echo "  $tag"
    write_file $category $tag > $cat_dir/$tag.markdown
  done
done
