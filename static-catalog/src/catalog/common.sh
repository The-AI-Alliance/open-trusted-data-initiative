# Common utilities for zsh scripts
# Source this script AFTER defining optional variables:
#   NOOP      Just echo, but don't execute commands (when commands are prefixed with $NOOP)
#   SCRIPT    Name of the running script. Defaults to $(basename $0)
#   ROOT_DIR  Name of the running script. Defaults to $(dirname $0)

# Other support scripts:
source $(dirname $0)/.util.sh  # this imports .colors.sh and .log.sh

: ${NOOP:=}
export NOOP

: ${SCRIPT:=$(script)}
: ${ROOTDIR:=$(dirname $0)}

# Some scripts use the lower-case alternatives instead.
: ${script:=$SCRIPT}
: ${rootdir:=$ROOTDIR}

# Find and return a list of files (without directories) in the input
# directories, recursively, where the first argument is an escaped file
# name glob. Use findFiles for more flexible options and "nicer" error
# reporting and continuation. 
findFilesInDirectories() {
  fileglob="$1"
  shift
  for d in "$@"
  do
    find "$d" -type f -name "$fileglob"
  done
}

# Find files in the list of input files and directories, where the latter
# are searched recursively. The following invocations is required:
#   findFiles find_args -- file1 [file2 ...]
# where the "find_args" are eventually passed to "find(1)". However, if one
# or both of "-regex" or "-iregex" are seen, then the "-E" option will also
# be used automatically (for extended regexs).
# If no matches are found in one of the directories or the file or directory
# doesn't exist, a warning is printed, but it keeps on going. The found files
# are printed to stdout.
findFiles() {
  find_regex=
  find_args=()
  while [[ $# -gt 0 ]]
  do
    case $1 in
      --)
        shift
        break
        ;;
      -*regex)
        find_args+=("$1")
        find_regex="-E"
        ;;
      *)
        find_args+=("$1")
        ;;
    esac
    shift
  done

  shift
  files=()
  for fd in "$@"
  do
    if [[ -d "$fd" ]]
    then
      new_files=($(find $find_regex "$fd" "${find_args[@]}"))
      if [[ ${#new_files[@]} -eq 0 ]]
      then
        warn "No files matching \"${find_args[@]}\" found in directory \"$fd\". Ignoring..."
      else
        files+=( "${new_files[@]}" )
      fi
    elif [[ -f "$fd" ]]
    then
      files+=("$fd")
    else
      warn "Directory \"$fd\" does not exist! Ignoring..."
    fi
  done
  echo "${files[@]}"
}

# Very crude imlpementation of a "map" function over an array.
# All it supports is passing a format string that is used to
# format each element and print the new array of strings.
# To capture the output as an array, use:
# my_array=($(map fmt input_array))
# However, every space-spearated word will be a separate array entry,
# meaning that my_array=($(map "--foo %s" 1 2 3)) will return a 
# six-element array, not three. :(
map_str() {
  fmt="$1"
  shift
  for s in "$@"
  do
    printf "$fmt" "$s"
  done
}

with_separator() {
  separator=$1
  shift
  result=""
  for s in "$@"
  do
    [[ -n "$result" ]] && result+=$separator
    result+="$s"
  done
  echo "$result"
}

check_commands() {
  not_found=()
  for cmd in "$@"
  do
    command -v $cmd > /dev/null || not_found+=($cmd)
  done
  [[ ${#not_found[@]} -eq 0 ]] || \
    error "The following required commands were not found: ${not_found[@]}"
}
