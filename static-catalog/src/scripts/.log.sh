# Include this script in other scripts

source $(dirname $0)/.colors.sh

# Change LOG_LEVEL in a script or command line (LOG_LEVEL=0 foo.sh) to change the logging level.
declare -A LOG_LEVELS
LOG_LEVELS[TRACE]=0
LOG_LEVELS[DEBUG]=1
LOG_LEVELS[INFO]=2
LOG_LEVELS[WARN]=3
LOG_LEVELS[ERROR]=4
: ${LOG_LEVEL:=INFO}

# Read standard out and log the lines
stream_at_level() {
  level=$1; shift
  color=$1; shift
  while read line
  do
    log_at_level $level $color $line
  done
}

# This function MUST redirect to stderr, because it's called from other functions
# that write data to stdout
log_at_level() {
  level=$1; shift
  color=$1; shift
  let level_index=$LOG_LEVELS[$level]
  let ll=$LOG_LEVELS[$LOG_LEVEL]
  [[ $level_index -lt $ll ]] && return
  local message_format="\033[1;${color}m %-6s ($(script)) $(now): $@\033[0m\n"
  # local message_format="[${color}] %-6s ($(script)) $(now): $@[${color}]\n"
  printf $message_format $level 1>&2
}


stream_trace() {
  stream_at_level "TRACE" $BLUE
}
stream_debug() {
  stream_at_level "DEBUG" $LIGHT_CYAN
}
stream_info() {
  stream_at_level "INFO"  $GREEN
}
stream_warn() {
  stream_at_level "WARN"  $YELLOW
}

stream_error() {
  stream_at_level "ERROR" $RED
}

# pc() {   # for "print color"
#   echo -e "\033[1;${color}m${label} ($(script)): $@\033[0m"
# }

trace() {
  log_at_level "TRACE" $BLUE "$@"
}
debug() {
  log_at_level "DEBUG" $LIGHT_CYAN "$@"
}
info() {
  log_at_level "INFO"  $GREEN "$@"
}
warn() {
  log_at_level "WARN"  $YELLOW "$@"
}

log_error() {
  log_at_level "ERROR" $RED "$@"
}

help() {
  local_help | stream_info
}

# To suppress printing help, pass --no-help.
# To suppress exiting, e.g., because you intend to call error several times
# before quitting, pass --no-exit or --dont-exit for all but the last invocations.
# The default exit code is 1. If you want to exit with a different code, use
# --exit N.
error() {
  local show_help=true
  local do_exit=true
  local message=()
  local exit_code
  let exit_code=1
  while [[ $# -gt 0 ]]
  do
    case $1 in
      -n|--no-help)
        show_help=false
        ;;
      -d|--no-exit|--dont-exit)
        do_exit=false
        ;;
      -e|--exit)
        shift
        let exit_code=$1
        ;;
      *)
        message+=( "$1" )
        ;;
    esac
    shift
  done
  log_error "${message[@]}"
  $show_help && echo && help 
  $do_exit && exit $exit_code
}

# Suppress logging, except for warning.
quiet() {
  LOG_LEVEL=WARN
}
