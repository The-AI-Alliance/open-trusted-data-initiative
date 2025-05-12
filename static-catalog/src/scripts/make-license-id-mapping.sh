#!/usr/bin/env zsh

base=$HOME/projects/ai-alliance/choosealicense.com
rm -f data/reference/license-id-name-mapping.json
grep 'title:' $base/_licenses/*.txt | \
	sed \
		-e 's?.*_licenses/??' \
		-e 's?\.txt??' \
		-e 's?"?\\"?g' \
		-e 's?title: ??' \
		-e 's?^\([^:]*\):\(.*\)$?{"id":"\1", "name":"\2", "url":"https://choosealicense.com/licenses/\1/"}?' \
		>> data/reference/license-id-name-mapping.json

ls -al data/reference/license-id-name-mapping.json
head -5 data/reference/license-id-name-mapping.json
