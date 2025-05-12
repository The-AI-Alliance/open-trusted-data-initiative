#!/usr/bin/env zsh
. src/scripts/common.sh

base=./data/json/$(now)
raw=./data/raw
out_spark=$base/spark

if [[ ! -d $raw ]] 
then
	echo "Directory $raw not found. Make sure you run this script from the static-catalog directory!"
	exit 1
fi

echo "Input data:  $raw"

# Must disable the VectorizedReader or else you might run out of memory!
echo "Running spark:"
cat <<EOF 
spark-submit \\
	-c spark.sql.parquet.enableVectorizedReader=false \\
	src/scripts/parquet-to-json.py \\
	--input $raw \\
	--output $out_spark
EOF
[[ -z $NOOP ]] && spark-submit \
	-c spark.sql.parquet.enableVectorizedReader=false \
	src/scripts/parquet-to-json.py \
	--input $raw \
	--output $out_spark

echo "Spark output data written to: $out_spark"
$NOOP ls -al $out_spark
