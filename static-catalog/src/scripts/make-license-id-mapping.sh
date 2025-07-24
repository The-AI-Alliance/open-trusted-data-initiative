#!/usr/bin/env zsh
# This is a "one-time" script that creates a JSON file to map
# license ids, names, and choosealicense.com URLs.
# Must run from the static-catalog directory. 

. ./src/scripts/common.sh

ref=./data/reference
calcl=$ref/choosealicense.com/_licenses
output=$ref/license-id-name-mapping.json

help () {
	cat <<EOF
Generates $output to map license ids, names, and URLs.
Usage: $SCRIPT [options]
Options:
-h | --help         Show this message and exit.
-o | --output FILE  Write JSON to FILE instead of the default:
                      $output

This is a "one-time" script that creates a JSON file to map
license ids, names, and choosealicense.com URLs.
You must run this script in the static-catalog directory. 

EOF
}

while [ $# -gt 0 ]
do
	case $1 in
	-h|--help)
		help
		exit 0
		;;
	-o|--output)
		shift
		output=$1
		;;
	esac
	shift
done

[[ -d $ref ]] || error "reference data folder $ref not found"
[[ -d $calcl ]] || error "source data folder $calcl not found"

$NOOP rm -f $ref/license-id-name-mapping.json
$NOOP grep 'title:' $calcl/*.txt | \
	sed \
		-e 's?.*_licenses/??' \
		-e 's?\.txt??' \
		-e 's?"?\\"?g' \
		-e 's?title: ??' \
		-e 's?^\([^:]*\):\(.*\)$?{"id":"\1", "name":"\2", "url":"https://choosealicense.com/licenses/\1/"}?' \
		>> $output

echo "$output created:"
ls -al $output
head -5 $output
