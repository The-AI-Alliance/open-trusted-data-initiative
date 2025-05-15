#!/usr/bin/env zsh
. src/scripts/common.sh

help() {
    cat <<EOF
Usage: $0 [-h|--help] [-n|--noop] [-s|--start M[:N]] [-p|--pos|--position M[:N]] [filename1 ...]
Where:
-h | --help                        Print this message and exit.
-n | --noop                        Print the commands, but do nothing. (Or use "NOOP=info $0 ...")
-s | --start | --start-line M[:N]  Print N lines starting at line M, counting from 1. If M specified, but not N, then prints
                                   from M to the end of the file (default: prints the whole file).
-p | --pos | --position M[:N]      Print N characters starting at position M, counting from 1. If M specified, but not N, 
                                   then prints from M to the end of the line (default: prints the whole line).
filename1 ...                      Input files (default: read from stdin).

Hence, with no flags, it works like cat...
EOF
}

pos_substr=
let start_line=0
let num_lines=-1
num_lines_exp=
filenames=()
print_exp="{print NR \": \" \$0}"
while [[ $# -gt 0 ]]
do
	case $1 in
		-h|--h*)
			help
			exit 0
			;;
		-n|--noop)
			NOOP=info
			;;
		-p|--pos*)
			shift
			m=$(echo $1 | cut -d : -f 1)
			n=$(echo $1 | cut -d : -f 2)
			if [[ $m = $1 ]]
			then
				print_exp="{print NR \": \" substr(\$0, $m)}"
			else
				print_exp="{print NR \": \" substr(\$0, $m, $n)}"
			fi
			;;
		-s|--start*)
			shift
			let start_line=$(echo $1 | cut -d : -f 1)
			num_lines=$(echo $1 | cut -d : -f 2)  # will == $1 if $1 DOESN'T have ":N"
			if [[ $start_line != $1 ]] && [[ $num_lines != $1 ]]
			then
				num_lines_exp="&& NR<start+num_lines"
			fi
			;;
		-*)
			error "Unrecognized option: $1"
			;;
		*)
			filenames+=("$1")
			;;
	esac
	shift
done

$NOOP awk -v start=$start_line -v num_lines=$num_lines "NR>=start $num_lines_exp $print_exp" "${filenames[@]}"
