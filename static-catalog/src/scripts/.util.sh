#set -euo pipefail

source $(dirname $0)/.log.sh

script() {
  if [[ -n $ZSH_ARGZERO ]] 
  then
    echo $ZSH_ARGZERO
  else
    echo $0
  fi
}

# Audible beep.
beep() { 
  echo "\a" 
}
beeps() { beep; beep }

# Time stamp formats suitable for using in a file or directory name.
ymd_hms_format="%Y-%m-%d_%H-%M-%S"
ymd_format="%Y-%m-%d"

# Return the current time using ymd_hms_format, "%Y%m%d-%H%M%S",
# unless --ymd is pased as an argument, in which case ymd_format, "%Y%m%d",
# is used. Both formats are suitable for use in file or directory names.
# Works on MacOS and Linux.
# usage ts=$(now) or ymd=$(now --ymd)
# Pass optional strings to be appended to the result, e.g., 
#  ts=$(now foo bar)
# returns "20240826-161829-foo-bar"
now() {
  format=$ymd_hms_format
  appendix=
  while [[ $# -gt 0 ]]
  do
    case $1 in
      --ymd)
        format=$ymd_format
        ;;
      *)
        appendix="$appendix-$1"
        ;;
    esac
    shift
  done
  dt=$(date +"$format")
  echo "$dt$appendix"
}

# Return the second-granularity time stamp when the input arguments
# were last modified. Useful for the backup method below.
# Works on MacOS and Linux.
# usage: times=( $(modified_timestamp path1 ...) )
modified_timestamp() {
  for f in "$@"
  do
    if [[ $(uname) =~ Darwin ]]
    then
      stat -f "%Sm" -t "$ymd_hms_format" "$f"
    else
      stat -c%y "$f" | sed -e 's/[ \+]/-/g'
    fi
  done
}

# Portable way of getting the full path to the input argument.
# Uses realpath if installed. On MacOS, install coreutils.
# Works on MacOS and Linux.
# usage: paths=( $(fullpath path1 ...) )
fullpath() {
  which -s realpath && realpath "$@" && return
  for f in "$@"
  do
    # From https://stackoverflow.com/a/3915420/14262258
    echo "$(cd "$(dirname "$f")"; pwd -P)/$(basename "$f")"
  done
}


# Move a file or directory to a new path, which is the current path
# with "-timestamp" appended, where "timestamp" will correspond to 
# the last time the directory was modified. This is useful when you 
# want to preserve earlier work that would be overwritten otherwise.
# usage: backup_dirs path "optional info message"
backup_path() {
  path="$1"
  shift
  message=("$@")
  if [[ -d "$path" ]]
  then
    ts=$(modified_timestamp $path)
    bkup=$path-$ts
    info "${message[@]} path $path. Backing up to $bkup"
    $NOOP mv "$path" "$bkup"
  fi
}
