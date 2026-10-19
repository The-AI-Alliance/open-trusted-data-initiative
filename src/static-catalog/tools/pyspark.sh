#!/usr/bin/env zsh

pyspark -c spark.sql.parquet.enableVectorizedReader=false "$@"

