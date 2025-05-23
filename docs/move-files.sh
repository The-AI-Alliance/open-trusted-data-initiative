for d in ../docs/_language/_*
do 
	tip1=$(basename $d)
	tip=${tip1#_}
	echo $d, $tip
	find $d -name '*.markdown' | while read f
	do
		base=$(basename $f)
		ff=../docs/_language/${tip}_${base}
		echo "$f -> $ff"
		cp $f $ff
	done
done
