# README on Processing Hugging Face Metadata

Dean Wampler, May 11, 2025

> **NOTE:** This is a condensed version of the long `duckdb-notes.md` file, plus other notes, where Dean experimented with DuckDB, Spark, and other tools. This file covers the commands that worked.

## Introduction

We start with the metadata files created by Joe Olson's nightly job that queries Hugging Face for Croissant metadata. The format of those files is Parquet with a flat schema, with one column containing the entire JSON document for the metadata. Parsing that metadata proved difficult, because of deep "escape quoting". It was necessary to put together a set of tools to extract this metadata and load it into  [DuckDB](https://duckdb.org) for further analysis and processing.

We start with what most people need to see, the commands to rebuild the catalog data for the website, then discuss in detail how we "got here".

## Rebuilding the Catalog

Ask Dean Wampler for help, if needed.

Steps:

* Parse a snapshot of data gathered from Hugging Face (short description TBD; see the rest of this README for details!)
* `cd static-catalog` where most of the following work is done:
* Update `data/reference/keyword-categories.json` with any changes to the hierarchy or keywords.
* Run `src/scripts/write-category-files.py`. 
  * It starts with a _shebang_, `/usr/bin/env python`, so you don't need to do `python src/...`. Try the `--help` option. Use `--verbose` to see what's happening. This script takes about 30 seconds to run. It writes one markdown file _for each topic_ under `markdown/processed/YYYY-MM-DD`. It writes one JavaScript and one JSON file _for each topic_ under `data/json/processed/YYYY-MM-DD`. 
* Run `src/scripts/copy-files-to-docs.sh` to copy the files created.
* Commit the changes and push upstream!

Notes:
* The markdown files copied to `../docs` (i.e., `../docs` is relative to our current working directory, `static-catalog`) correspond to _collections_ defined in `../docs/_config.yaml`; there is a subfolder for each collection, currently `_language`, `_domain`, and `_modality` (the `_` is required)
* The JavaScript files are copied to `../docs/files/data/catalog`. They contain the static data, defined as JS arrays of objects. 
* The markdown and JSON directory hierarchies are _different_. The markdown files need to be flat, only _collection_ subfolders (currently `_language`, `_domain`, and `_modality`). We tried making hierarchical directories here, but this isn't supported by Jekyll/Liquid. In contrast, the JavaScript files written to `../docs/files/data/catalog` are hierarchical, because they use our own convention and are handled appropriately by the JavaScript code used (see `../docs/_includes/data_table_template.html`). 

The rest of this README covers how to parse the raw data into usable JSON. It doesn't cover editing of `static-catalog/data/reference/keyword-categories.json`, which was created manually!!

## Initial Setup

Get a copy of the Parquet files with the Croissant metadata and use it as follows. Let's assume those Parquet files are in the current directory:

```shell
mkdir -p data/raw
mv *.parquet data/raw
mkdir -p data/json
```

## Python Dependencies

You'll need these packages. PySpark is discussed next.

```shell
pip install py4j pyspark psutil
```

## Starting with Spark

We start with [PySpark](https://spark.apache.org) to do the initial conversion from Parquet to JSON. In fact, this step could be done with DuckDB. 

Follow the installation instructions for Spark. The PySpark codeused is in `src/scripts/parquet-to-json.py` and it is invoked by `src/scripts/parquet-to-json.sh`. which reads the data from `./data/raw` and writes the results to `.data/json/<timestamp>/*.json` files (one file per _partition_). One script run executed this command:

```shell
spark-submit -c spark.sql.parquet.enableVectorizedReader=false \ 
  src/scripts/parquet-to-json.py \ 
  --input ./data/raw \ 
  --output ./data/json/2025-05-10_16-02-30/spark
```

The output JSON files have single-line JSON docs. Basically _JSONL_ format, but the partitions aren't structured as arrays of JSON objects. Fortunately DuckDB handles this fine.

Here is what a line looks like in this file:

```json
{"croissant":"{\"@context\":{\"@language\":\"en\",...}}"}
```

In other words, one _field_ named `croissant`, and an ugly, nested JSON string with lots of escapes for `"`, etc. This we need to extract and successfully _unescape_ to create the JSON records we want. 

The Spark code includes this SQL `WHERE` clauses, `WHERE response_reason = 'OK'`. It turns out there are a total of 332988 records in the Parquet data, which means there are that many datasets hosted at Hugging Face (at the time this data was gathers), but only 261495 of them have Croissant data. The rest of the records are discarded.

At this point, Dean started using DuckDB because of its good support for JSON, but he found that further cleaning of the JSON files is necessary first, like extracting the value for the `croissant` column and "unquoting" at least the top-level quotes for strings, as discussed next.

## Using `jq` and `sed` 

This is the ugly part; to proceed some nasty regex hacking using `sed` was done to transform the JSON files to a more usable format. This is always an approach that is fraught with peril! 

TLDR: This approach successfully cleaned up all but 19 of > 260K JSON records, which was more than good enough. The remaining 19 records were discarded.

Here is the sequence of transformations that produce usable JSON for loading into DuckDB. First, for convenience, copy the Spark output partition files to a convenient place with shorter names:

```shell
rm -rf ./data/json/temp
mkdir ./data/json/temp
for f in ./data/json/2025-05-10_16-02-30/spark/*.json
do 
  base=$(basename $f)
  number=$(echo $base | cut -d - -f 2)
  target=./data/json/temp/$number.json
  echo cp $f $target
  cp $f $target
done
```

```shell
$ ll ./data/json/temp
total 5672552
drwxr-xr-x  7 me  staff   224B May 10 16:26 ./
drwxr-xr-x@ 7 me  staff   224B May 10 16:26 ../
-rw-r--r--@ 1 me  staff     0B May 10 16:26 00000.json
-rw-r--r--@ 1 me  staff   1.1G May 10 16:26 00001.json
-rw-r--r--@ 1 me  staff   759M May 10 16:26 00004.json
-rw-r--r--@ 1 me  staff   685M May 10 16:26 00006.json
-rw-r--r--@ 1 me  staff   225M May 10 16:26 00007.json
```

Next, use `jq` to extract the JSON string for the single field, `croissant`. (This could probably also be done with Spark or DuckDB...). Pass the `jq` output through a `sed` command with three regex replacements to do the following:

1. The output rows are surrounded with `"..."`. Use two replacements for the beginning and the end of the string to remove the double quotes.
2. Replace all `\"` with `"`, but don't match on `\\"`, which are for _nested_ quotes. In other words, replace all the top-level escaped quotes. For example, `{\"foo\":\"1 \\"2\\" 3\"}` should become `{"foo":"1 \\"2\\" 3"}`. (Arguably, the `\\"2\\"` should become `\"2\"`, but we'll pursue this later, if necessary.)

```shell
jq .croissant ./data/json/sample/*.json | sed -e 's/^"//'  -e 's/"$//' -e 's/\([^\\]\)\\"/\1"/g' > dequoted-1.json
wc dequoted-1.json
```

`wc` prints `261495 52099629 2604796536 dequoted-1.json`.

Use of DuckDB will be discussed shortly, but the process Dean followed at this point was to attempt to load this JSON file as a table, see what corrupt JSON DuckDB detected, then fix those errors by adding more regex replacements to the `sed` command. The first round went like this:

Try to a create a table in DuckDB:

```sql
CREATE OR REPLACE TABLE hf_croissant AS
  FROM (
    SELECT *
    FROM read_ndjson_objects('dequoted-1.json')
  );
```

```
Malformed JSON in file "dequoted-1.json", at byte 5824 in line 271: unexpected character.
```

Because the lines can be very long, Dean found it useful to write a shell script that could print a range of lines and only a specified range of character positions within those lines, called `src/scripts/print-lines.sh`. Use the `--help` option to see how to use it. In what follows, we won't show the invocations used as Dean worked through the malformed records, but here is an example invocation for an error on line 270, where `270:1` means print one line starting at 270, and print `100` characters from position `5800` (i.e., a range around the reported error around `5850`), in `dequoted-1.json`: 

```shell
$ src/scripts/print-lines.sh --start 270:1 --pos 5800:100 dequoted-1.json
-sa-4.0/","sameAs":"\","url":"https://huggingface.co/datasets/chenghao/sec-material-contracts"}
```

The problem here is the `\` in `"sameAs":"\","url"`. Note that DuckDB reported the error on line `271`, but the error is actually on is line `270`, which is what `awk`, which is used in `print-lines.sh`, reports.

After many rounds of detecting these errors and attempting to fix them with `sed`, this is the final `sed` command we will use, where the `dequoted-5.json` was the output file used. We'll keep that name for consistency with `duckdb-notes.md`, where you'll see that dean actually went three more steps, to `dequoted-8.json`, but after "5", he was just adding very specific fixes for individual lines. Only a few bad lines were left, so it was better to just discard them at this point.

```shell
$ jq .croissant ./data/json/sample/*.json | \
  sed -e 's/^"//'  -e 's/"$//' -e 's/\\"\\"/""/g' -e 's/\([^\\]\)\\"/\1"/g' -e 's/"\\\\\\"/"/g' -e 's/\\\\""/"/g' -e 's/\([:,]\)\s*"\\[\\]*"/\1""/g' > dequoted-5.json
```

> **NOTE:** This command takes about _four minutes_ to run on an Apple Studio with an M1 Max!

Finally, use `src/scripts/parse-json.py` to look for lines that don't parse correctly and remove them, creating a JSON dataset we can successfully import into DuckDB. It also prints all bad lines found and statistics about the results:

```shell
$ src/scripts/parse-json.py --verbose --input dequoted-5.json --output filtered-5.json
...
Error statistics:
             file:    total    bad        %
  dequoted-5.json:   261479     19   0.007%
output file: filtered-5.json
```

Great! Only 19 out of 261479 or 0.007%. Now, we'll load this data into DuckDB. (For the record, with the addition `sed` replacements omitted here, I got down to 16 bad records, but 19 is plenty good enough.)

What if Dean had skipped all the `sed` hacking and just used this script?

```shell
$ src/scripts/parse-json.py --verbose --input dequoted-1.json --output filtered-1.json
...
Error statistics:
             file:    total    bad        %
  dequoted-1.json:   258212   3283   1.271%
output file: filtered-1.json
```

Discarding 1% of the records would not have been that bad. It would have saved a lot of time...

## Using DuckDB

Finally, we are ready to use [DuckDB](https://duckdb.org), which has good support for JSON.

Install the [DuckDB](https://duckdb.org) CLI tools and Python library. See the [documentation](https://duckdb.org/docs/stable/) for details.

Use this command to install the tools, including the `duckdb` CLI:

```shell
curl https://install.duckdb.org | sh
```

Optionally, install the Python library, but it is not used in what follows:

```shell
pip install duckdb
```

## Using the JSON Support in the `duckdb` CLI

The JSON processing functions are [documented here](https://duckdb.org/docs/stable/data/json/json_functions.html).

In the `duckdb` CLI, you install the `json` module.

Start the CLI `duckdb`. In this case, a persistent database `croissant.duckdb` was used. This is highly recommended, otherwise everything is just in memory and lost when you exit the CLI:

```shell
duckdb croissant.duckdb
```

> **WARNING:** The `croissant.duckdb` file can easily grow to GBs in size!

At the `D` prompt (which will often be omitted in what follows, except when showing output...) type the following:

```
install 'json';
load 'json';
```

These commands don't need to be repeated in subsequent sessions.

> **TIP:** Use `.quit` to exit `duckdb`.

Now create the table!

```sql
CREATE OR REPLACE TABLE hf_croissant AS
  FROM (
    SELECT *
    FROM read_ndjson_objects('filtered-5.json')
  );
```

This should be successful, printing this:
```
100% ▕████████████████████████████████████████████████████████████▏
```

Let's have a look. Again, `D` is the prompt which you should omit:

```sql
D DESCRIBE hf_croissant;
┌─────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│ column_name │ column_type │  null   │   key   │ default │  extra  │
│   varchar   │   varchar   │ varchar │ varchar │ varchar │ varchar │
├─────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ json        │ JSON        │ YES     │ NULL    │ NULL    │ NULL    │
└─────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘
D SELECT * FROM hf_croissant LIMIT 2;
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                         json                                                         │
│                                                         json                                                         │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ {"@context": {"@language": "en", "@vocab": "https://schema.org/", "citeAs": "cr:citeAs", "column": "cr:column", "c…  │
│ {"@context": {"@language": "en", "@vocab": "https://schema.org/", "citeAs": "cr:citeAs", "column": "cr:column", "c…  │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
D SELECT json_valid(json) as valid FROM hf_croissant WHERE valid = 'false';
┌─────────┐
│  valid  │
│ boolean │
├─────────┤
│ 0 rows  │
└─────────┘
D SELECT json_keys(json) FROM hf_croissant LIMIT 1;
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                json_keys("json")                                                 │
│                                                    varchar[]                                                     │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [@context, @type, distribution, recordSet, conformsTo, name, description, alternateName, creator, keywords, url] │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
D SELECT count(*) FROM hf_croissant;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│    261495    │
└──────────────┘
```

> **NOTE:** It's not clear why this count is 261495, while the output of our filter script is 261479. 

## Extracting the Metadata Fields We Need

Now we can use use DuckDB's [JSON support](https://duckdb.org/docs/stable/data/json/overview.html) to extract the fields we want into new tables. 

This [blog post](https://rpbouman.blogspot.com/2024/12/duckdb-bag-of-tricks-reading-json-data.html) about working with JSON in DuckDB was very informative.

First, here is a query to grab a set of fields needed for our purposes:

```sql
WITH metadata AS (
  SELECT  json->>'$.name'            AS name,
          json->>'$.description'     AS description,
          json->>'$.url'             AS url,
          json->>'$.license'         AS license,
          json->>'$.keywords[*]'     AS keywords,
          json->'$."@context"'       AS context,
          json->'$.creator'          AS creator,
  FROM    hf_croissant
)
SELECT    name,
          description,
          license,
          context->>'$."@language"'  AS language,
          url,
          keywords,
          creator->>'$.name'         AS creator_name,
          creator->>'$.url'          AS creator_url,
FROM      metadata
WHERE     license NOT NULL 
LIMIT     5;
```

> **NOTE:** Using `json->>'$.keywords[*]' AS keywords` extracts `keywords` as a `VARCHAR` array. Without the `[*]`, `keywords` would just be a `VARCHAR` and much less useful below.

Here is what we get:

```
┌──────────────────────┬──────────────────────┬──────────────────────┬───┬──────────────────┬──────────────────────┐
│         name         │     description      │       license        │ … │   creator_name   │     creator_url      │
│       varchar        │       varchar        │       varchar        │   │     varchar      │       varchar        │
├──────────────────────┼──────────────────────┼──────────────────────┼───┼──────────────────┼──────────────────────┤
│ new03                │ \n\t\n\t\t\n\t\n\t…  │ https://choosealic…  │ … │ joey_fullname    │ https://huggingfac…  │
│ silvervoz            │ iansousa12/silverv…  │ https://choosealic…  │ … │ Ian Sousa        │ https://huggingfac…  │
│ test-codegen-basel…  │ echodrift/test-cod…  │ https://choosealic…  │ … │ Thieu Luu        │ https://huggingfac…  │
│ silvervoz2           │ iansousa12/silverv…  │ https://choosealic…  │ … │ Ian Sousa        │ https://huggingfac…  │
│ New_York_Times_Top…  │ dstefa/New_York_Ti…  │ https://choosealic…  │ … │ Dimos Stefanidis │ https://huggingfac…  │
├──────────────────────┴──────────────────────┴──────────────────────┴───┴──────────────────┴──────────────────────┤
│ 5 rows                                                                                       8 columns (5 shown) │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

The `->>` extracts the value as a basic type, like `VARCHAR`, while `->` extracts the content as a `JSON` object. The later is used for nested structures. There are alternative ways of writing these constructs. See the [docs](https://duckdb.org/docs/stable/data/json/overview.html).

Also, note that records without a license field are removed, which leaves only about 60K records (see below), although some of the removed records do list the license in their keywords.

Now create a metadata table, called `hf_metadata1`. We'll create a _final_ `hf_metadata` table shortly.:

```sql
CREATE OR REPLACE TABLE hf_metadata1 AS
  WITH metadata AS (
    SELECT  json->>'$.name'            AS name,
            json->>'$.description'     AS description,
            json->>'$.url'             AS dataset_url,
            json->>'$.license'         AS license,
            json->>'$.keywords[*]'     AS keywords,
            json->'$."@context"'       AS context,
            json->'$.creator'          AS creator,
    FROM    hf_croissant
  )
  SELECT    name,
            description,
            license,
            context->>'$."@language"'  AS language,
            dataset_url,
            keywords,
            creator->>'$.name'         AS creator_name,
            creator->>'$.url'          AS creator_url,
  FROM      metadata
  WHERE     license NOT NULL;
```

```sql
D DESCRIBE hf_metadata1;
┌──────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│ column_name  │ column_type │  null   │   key   │ default │  extra  │
│   varchar    │   varchar   │ varchar │ varchar │ varchar │ varchar │
├──────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ name         │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ description  │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ license      │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ language     │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ dataset_url  │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ keywords     │ VARCHAR[]   │ YES     │ NULL    │ NULL    │ NULL    │
│ creator_name │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ creator_url  │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
└──────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘D SELECT count(*) FROM hf_metadata1;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│    60107     │
└──────────────┘
```
> **NOTE:** To investigate datasets with `NULL` licenses, I later created `hf_metadata1_with_null_licenses`, where the `WHERE license IS NULL` clause was removed, and similarly `hf_metadata_with_all_licenses`, using modifications to the query below used to create `hf-metadata`. See the discussion there.

### Licenses

So, only 60K out of 261K records (23%) have a license! Not great. Let's see what those licenses are. First, let's tell `duckdb` to not truncate the output at the default of 40 rows. (Only ~75 lines are needed for the next query):

```sql
.maxrows 1234
```

```sql
SELECT license, count(license) AS count
FROM hf_metadata1 GROUP BY license ORDER BY count DESC NULLS FIRST;
```

Apache and MIT (popular with academics) are the most common licenses:

```
┌────────────────────────────────────────────────────────────────┬───────┐
│                            license                             │ count │
│                            varchar                             │ int64 │
├────────────────────────────────────────────────────────────────┼───────┤
│ https://choosealicense.com/licenses/apache-2.0/                │ 19822 │
│ https://choosealicense.com/licenses/mit/                       │ 16916 │
│ https://choosealicense.com/licenses/openrail/                  │  4567 │
│ https://choosealicense.com/licenses/cc-by-4.0/                 │  3547 │
│ https://choosealicense.com/licenses/unknown/                   │  1940 │
│ https://choosealicense.com/licenses/cc-by-sa-4.0/              │  1589 │
│ https://choosealicense.com/licenses/other/                     │  1543 │
│ https://choosealicense.com/licenses/cc-by-nc-4.0/              │  1244 │
│ https://choosealicense.com/licenses/cc-by-nc-sa-4.0/           │  1070 │
│ https://choosealicense.com/licenses/cc0-1.0/                   │  1032 │
│ https://choosealicense.com/licenses/cc/                        │   837 │
│ https://choosealicense.com/licenses/cc-by-nc-nd-4.0/           │   530 │
│ https://choosealicense.com/licenses/odc-by/                    │   518 │
│ https://choosealicense.com/licenses/gpl-3.0/                   │   513 │
│ https://choosealicense.com/licenses/cc-by-sa-3.0/              │   457 │
│ https://choosealicense.com/licenses/gpl/                       │   421 │
│ https://choosealicense.com/licenses/afl-3.0/                   │   386 │
│ https://choosealicense.com/licenses/creativeml-openrail-m/     │   281 │
│ https://choosealicense.com/licenses/llama2/                    │   211 │
│ https://choosealicense.com/licenses/llama3/                    │   178 │
│ https://choosealicense.com/licenses/wtfpl/                     │   156 │
│ https://choosealicense.com/licenses/cc-by-3.0/                 │   154 │
│ https://choosealicense.com/licenses/agpl-3.0/                  │   151 │
│ https://choosealicense.com/licenses/llama3.1/                  │   144 │
│ https://choosealicense.com/licenses/cc-by-2.0/                 │   137 │
│ https://choosealicense.com/licenses/bsd/                       │   130 │
│ https://choosealicense.com/licenses/unlicense/                 │   127 │
│ https://choosealicense.com/licenses/cc-by-nc-2.0/              │   117 │
│ https://choosealicense.com/licenses/undefined/                 │    99 │
│ https://choosealicense.com/licenses/cc-by-nd-4.0/              │    97 │
│ https://choosealicense.com/licenses/artistic-2.0/              │    84 │
│ https://choosealicense.com/licenses/bsd-3-clause/              │    84 │
│ https://choosealicense.com/licenses/llama3.2/                  │    77 │
│ https://choosealicense.com/licenses/odbl/                      │    75 │
│ https://choosealicense.com/licenses/cdla-permissive-2.0/       │    62 │
│ https://choosealicense.com/licenses/pddl/                      │    59 │
│ https://choosealicense.com/licenses/cc-by-nc-sa-3.0/           │    58 │
│ https://choosealicense.com/licenses/c-uda/                     │    54 │
│ https://choosealicense.com/licenses/gpl-2.0/                   │    54 │
│ https://choosealicense.com/licenses/openrail++/                │    52 │
│ https://choosealicense.com/licenses/cdla-sharing-1.0/          │    51 │
│ https://choosealicense.com/licenses/bigscience-openrail-m/     │    51 │
│ https://choosealicense.com/licenses/cc-by-nc-3.0/              │    49 │
│ https://choosealicense.com/licenses/bsd-2-clause/              │    32 │
│ https://choosealicense.com/licenses/llama3.3/                  │    31 │
│ https://choosealicense.com/licenses/cc-by-nc-sa-2.0/           │    28 │
│ https://choosealicense.com/licenses/mpl-2.0/                   │    24 │
│ https://choosealicense.com/licenses/eupl-1.1/                  │    24 │
│ https://choosealicense.com/licenses/lgpl-3.0/                  │    23 │
│ https://choosealicense.com/licenses/cc-by-nc-nd-3.0/           │    22 │
│ https://choosealicense.com/licenses/bigcode-openrail-m/        │    22 │
│ https://choosealicense.com/licenses/gemma/                     │    20 │
│ https://choosealicense.com/licenses/cc-by-2.5/                 │    20 │
│ https://choosealicense.com/licenses/gfdl/                      │    19 │
│ https://choosealicense.com/licenses/etalab-2.0/                │    17 │
│ https://choosealicense.com/licenses/bigscience-bloom-rail-1.0/ │    13 │
│ https://choosealicense.com/licenses/ecl-2.0/                   │    12 │
│ https://choosealicense.com/licenses/ms-pl/                     │    12 │
│ https://choosealicense.com/licenses/bsd-3-clause-clear/        │    11 │
│ https://choosealicense.com/licenses/postgresql/                │     8 │
│ https://choosealicense.com/licenses/bsl-1.0/                   │     8 │
│ https://choosealicense.com/licenses/lgpl/                      │     7 │
│ https://choosealicense.com/licenses/cdla-permissive-1.0/       │     7 │
│ https://choosealicense.com/licenses/osl-3.0/                   │     6 │
│ https://choosealicense.com/licenses/lgpl-2.1/                  │     5 │
│ https://choosealicense.com/licenses/apple-amlr/                │     4 │
│ https://choosealicense.com/licenses/isc/                       │     2 │
│ https://choosealicense.com/licenses/epl-2.0/                   │     1 │
│ https://choosealicense.com/licenses/epl-1.0/                   │     1 │
│ https://choosealicense.com/licenses/ofl-1.1/                   │     1 │
│ https://choosealicense.com/licenses/lgpl-lr/                   │     1 │
│ https://choosealicense.com/licenses/zlib/                      │     1 │
│ https://choosealicense.com/licenses/deepfloyd-if-license/      │     1 │
├────────────────────────────────────────────────────────────────┴───────┤
│ 73 rows                                                      2 columns │
└────────────────────────────────────────────────────────────────────────┘
```

(There are no `NULLS`, but it's generally useful to have...)

Let's create a table of unique licenses. To do this, we need a convenient way to map the license ids in the URL to names. We extracted this information from the `choosealicense` [GitHub repo](https://github.com/github/choosealicense.com/tree/gh-pages/_licenses), specifically the [`_licenses`](https://github.com/github/choosealicense.com/tree/gh-pages/_licenses) directory. A JSON file was created here with `src/scripts/make-license-id-mapping.sh` from the `_licenses` files and written to `./data/reference/license-id-name-mapping.json`.

```sql
CREATE OR REPLACE TABLE hf_licenses AS
SELECT * FROM read_json('data/reference/license-id-name-mapping.json');
```

```sql
D SELECT * FROM hf_licenses LIMIT 5;
┌──────────────┬────────────────────────────────────────┬──────────────────────────────────────────────────┐
│      id      │                  name                  │                       url                        │
│   varchar    │                varchar                 │                     varchar                      │
├──────────────┼────────────────────────────────────────┼──────────────────────────────────────────────────┤
│ 0bsd         │ BSD Zero Clause License                │ https://choosealicense.com/licenses/0bsd         │
│ afl-3.0      │ Academic Free License v3.0             │ https://choosealicense.com/licenses/afl-3.0      │
│ agpl-3.0     │ GNU Affero General Public License v3.0 │ https://choosealicense.com/licenses/agpl-3.0     │
│ apache-2.0   │ Apache License 2.0                     │ https://choosealicense.com/licenses/apache-2.0   │
│ artistic-2.0 │ Artistic License 2.0                   │ https://choosealicense.com/licenses/artistic-2.0 │
└──────────────┴────────────────────────────────────────┴──────────────────────────────────────────────────┘
```

Now, let's join this this to `hf_metadata1` to create `hf_metadata`:

```sql
CREATE OR REPLACE TABLE hf_metadata AS 
  SELECT 
    hfm.name          AS name,
    hfm.description   AS description,
    lic.name          AS license,
    lic.id            AS license_id,
    hfm.license       AS license_url,
    hfm.language      AS language,
    hfm.dataset_url   AS dataset_url,
    hfm.keywords      AS keywords,
    hfm.creator_name  AS creator_name,
    hfm.creator_url   AS creator_url
  FROM hf_metadata1 hfm
  JOIN hf_licenses  lic
  ON hfm.license = lic.url;
```

```sql
D DESCRIBE hf_metadata;
┌──────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│ column_name  │ column_type │  null   │   key   │ default │  extra  │
│   varchar    │   varchar   │ varchar │ varchar │ varchar │ varchar │
├──────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ name         │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ description  │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ license      │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ license_id   │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ license_url  │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ language     │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ dataset_url  │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ keywords     │ VARCHAR[]   │ YES     │ NULL    │ NULL    │ NULL    │
│ creator_name │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ creator_url  │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
├──────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┤
│ 10 rows                                                  6 columns │
└────────────────────────────────────────────────────────────────────┘
```

```sql
SELECT license, count(license) AS count
FROM hf_metadata GROUP BY license ORDER BY count DESC;
```
```
┌────────────────────────────────────────────────────────────┬───────┐
│                          license                           │ count │
│                          varchar                           │ int64 │
├────────────────────────────────────────────────────────────┼───────┤
│ Apache License 2.0                                         │ 19821 │
│ MIT License                                                │ 16916 │
│ Creative Commons Attribution 4.0 International             │  3547 │
│ Creative Commons Attribution Share Alike 4.0 International │  1589 │
│ Creative Commons Zero v1.0 Universal                       │  1032 │
│ GNU General Public License v3.0                            │   513 │
│ Academic Free License v3.0                                 │   386 │
│ "Do What The F*ck You Want To Public License"              │   156 │
│ GNU Affero General Public License v3.0                     │   151 │
│ The Unlicense                                              │   127 │
│ BSD 3-Clause "New" or "Revised" License                    │    84 │
│ Artistic License 2.0                                       │    84 │
│ GNU General Public License v2.0                            │    54 │
│ BSD 2-Clause "Simplified" License                          │    32 │
│ Mozilla Public License 2.0                                 │    24 │
│ European Union Public License 1.1                          │    24 │
│ GNU Lesser General Public License v3.0                     │    23 │
│ Educational Community License v2.0                         │    12 │
│ Microsoft Public License                                   │    12 │
│ BSD 3-Clause Clear License                                 │    11 │
│ PostgreSQL License                                         │     8 │
│ Boost Software License 1.0                                 │     8 │
│ Open Software License 3.0                                  │     6 │
│ GNU Lesser General Public License v2.1                     │     5 │
│ ISC License                                                │     2 │
│ SIL Open Font License 1.1                                  │     1 │
│ zlib License                                               │     1 │
│ Eclipse Public License 2.0                                 │     1 │
│ Eclipse Public License 1.0                                 │     1 │
├────────────────────────────────────────────────────────────┴───────┤
│ 29 rows                                                  2 columns │
└────────────────────────────────────────────────────────────────────┘
```

But notice this:

```sql
D SELECT count() FROM hf_metadata;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│    44631     │
└──────────────┘
```

So, we lost more records, about 15K! It turns out there are a lot of URLs in the metadata for non-existing pages at [choosealicense.com](https://choosealicense.com/licenses). Many seem legitimate, but poorly specified.

```sql
COPY (SELECT 
  hfm.name          AS name,
  lic.name          AS license,
  lic.id            AS license_id,
  hfm.license       AS license_url,
FROM hf_metadata1 hfm
LEFT JOIN hf_licenses  lic
ON hfm.license = lic.url) TO 'toss.json' (FORMAT json, ARRAY true);

SELECT 
  lic.id            AS license_id,
  hfm.license       AS license_url,
FROM hf_metadata1 hfm
LEFT JOIN hf_licenses  lic
ON hfm.license = lic.url
WHERE lic.url IS NULL;
```

The second query reports 15.4K rows!

```sql
WITH lics AS (
  SELECT 
    lic.id            AS license_id,
    hfm.license       AS license_url,
  FROM hf_metadata1 hfm
  LEFT JOIN hf_licenses  lic
  ON hfm.license = lic.url
  WHERE lic.url IS NULL
  )
SELECT license_url, count(license_url) AS count
FROM lics
GROUP BY license_url
ORDER BY count DESC;
```
```
┌────────────────────────────────────────────────────────────────┬───────┐
│                          license_url                           │ count │
│                            varchar                             │ int64 │
├────────────────────────────────────────────────────────────────┼───────┤
│ https://choosealicense.com/licenses/openrail/                  │  4567 │
│ https://choosealicense.com/licenses/unknown/                   │  1940 │
│ https://choosealicense.com/licenses/other/                     │  1543 │
│ https://choosealicense.com/licenses/cc-by-nc-4.0/              │  1245 │
│ https://choosealicense.com/licenses/cc-by-nc-sa-4.0/           │  1070 │
│ https://choosealicense.com/licenses/cc/                        │   837 │
│ https://choosealicense.com/licenses/cc-by-nc-nd-4.0/           │   530 │
│ https://choosealicense.com/licenses/odc-by/                    │   518 │
│ https://choosealicense.com/licenses/cc-by-sa-3.0/              │   457 │
│ https://choosealicense.com/licenses/gpl/                       │   421 │
│ https://choosealicense.com/licenses/creativeml-openrail-m/     │   281 │
│ https://choosealicense.com/licenses/llama2/                    │   211 │
│ https://choosealicense.com/licenses/llama3/                    │   178 │
│ https://choosealicense.com/licenses/cc-by-3.0/                 │   154 │
│ https://choosealicense.com/licenses/llama3.1/                  │   144 │
│ https://choosealicense.com/licenses/cc-by-2.0/                 │   137 │
│ https://choosealicense.com/licenses/bsd/                       │   130 │
│ https://choosealicense.com/licenses/cc-by-nc-2.0/              │   117 │
│ https://choosealicense.com/licenses/undefined/                 │    99 │
│ https://choosealicense.com/licenses/cc-by-nd-4.0/              │    97 │
│                         ·                                      │     · │
│                         ·                                      │     · │
│                         ·                                      │     · │
│ https://choosealicense.com/licenses/cc-by-nc-sa-3.0/           │    58 │
│ https://choosealicense.com/licenses/c-uda/                     │    54 │
│ https://choosealicense.com/licenses/openrail++/                │    52 │
│ https://choosealicense.com/licenses/cdla-sharing-1.0/          │    51 │
│ https://choosealicense.com/licenses/bigscience-openrail-m/     │    51 │
│ https://choosealicense.com/licenses/cc-by-nc-3.0/              │    49 │
│ https://choosealicense.com/licenses/llama3.3/                  │    31 │
│ https://choosealicense.com/licenses/cc-by-nc-sa-2.0/           │    28 │
│ https://choosealicense.com/licenses/cc-by-nc-nd-3.0/           │    22 │
│ https://choosealicense.com/licenses/bigcode-openrail-m/        │    22 │
│ https://choosealicense.com/licenses/gemma/                     │    20 │
│ https://choosealicense.com/licenses/cc-by-2.5/                 │    20 │
│ https://choosealicense.com/licenses/gfdl/                      │    19 │
│ https://choosealicense.com/licenses/etalab-2.0/                │    17 │
│ https://choosealicense.com/licenses/bigscience-bloom-rail-1.0/ │    13 │
│ https://choosealicense.com/licenses/cdla-permissive-1.0/       │     7 │
│ https://choosealicense.com/licenses/lgpl/                      │     7 │
│ https://choosealicense.com/licenses/apple-amlr/                │     4 │
│ https://choosealicense.com/licenses/deepfloyd-if-license/      │     1 │
│ https://choosealicense.com/licenses/lgpl-lr/                   │     1 │
├────────────────────────────────────────────────────────────────┴───────┤
│ 44 rows (40 shown)                                           2 columns │
└────────────────────────────────────────────────────────────────────────┘
```

Okay, for now, we will reject the datasets with invalid URLs for the licenses, even though some clearly intend to reference legitimate license sources.

#### Keeping "Bad" Licenses

As discussed above, we later created a second set of tables that kept the "bad" licenses, for further analysis. Using the same query to create `hf_metadata`, but with `hf_metadata1_with_null_licenses` instead of `hf_metadata1` and a `LEFT JOIN` with `hf_licenses`, instead of just `JOIN`:

```sql
CREATE OR REPLACE TABLE hf_metadata_with_all_licenses AS 
  SELECT 
    hfm.name          AS name,
    hfm.description   AS description,
    lic.name          AS license,
    lic.id            AS license_id,
    hfm.license       AS license_url,
    hfm.language      AS language,
    hfm.dataset_url   AS dataset_url,
    hfm.keywords      AS keywords,
    hfm.creator_name  AS creator_name,
    hfm.creator_url   AS creator_url
  FROM hf_metadata1_with_null_licenses hfm
  LEFT JOIN hf_licenses lic
  ON hfm.license = lic.url;
```

This table has 261495, as we would expect. 

### Languages

Let's look at `language` and `keywords`:

```sql
SELECT language, count(language) AS count
FROM hf_metadata GROUP BY language ORDER BY count DESC NULLS FIRST;
```
```
┌──────────┬───────┐
│ language │ count │
│ varchar  │ int64 │
├──────────┼───────┤
│ en       │ 44631 │
└──────────┴───────┘
```

Okay, so _every_ dataset is marked English!! This is not what we were hoping for, but it turns out other languages are at least partially covered, which we can see in the keywords.

```sql
SELECT keywords FROM hf_metadata LIMIT 10;
```
```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                       keywords                                                       │
│                                                      varchar[]                                                       │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [apache-2.0, 100K - 1M, parquet, Text, Datasets, pandas, Croissant, Polars, 🇺🇸 Region: US]                           │
│ [mit, 10K - 100K, parquet, Text, Datasets, pandas, Croissant, Polars, 🇺🇸 Region: US]                                 │
│ [mit, 100K - 1M, csv, Text, Datasets, pandas, Croissant, Polars, 🇺🇸 Region: US]                                      │
│ [question-answering, text-generation, English, apache-2.0, 1M - 10M, parquet, Text, Datasets, Dask, Croissant, Pol…  │
│ [question-answering, Russian, gpl-3.0, < 1K, csv, Text, Datasets, pandas, Croissant, Polars, 🇺🇸 Region: US, legal]   │
│ [mit, < 1K, csv, Tabular, Datasets, pandas, Croissant, Polars, 🇺🇸 Region: US]                                        │
│ [mit, 10K - 100K, csv, Text, Datasets, pandas, Croissant, Polars, 🇺🇸 Region: US]                                     │
│ [mit, < 1K, csv, Tabular, Datasets, pandas, Croissant, Polars, 🇺🇸 Region: US]                                        │
│ [apache-2.0, < 1K, parquet, Text, Datasets, pandas, Croissant, Polars, 🇺🇸 Region: US]                                │
│ [mit, 100K - 1M, json, Tabular, Datasets, pandas, Croissant, Polars, 🇺🇸 Region: US, Imitation Learning, Expert Traj…  │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                       10 rows                                                        │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Let's _unnest_ them:

```sql
SELECT unnest(keywords) AS keyword FROM hf_metadata LIMIT 10;
```
```
┌───────────────┐
│    keyword    │
│    varchar    │
├───────────────┤
│ apache-2.0    │
│ 100K - 1M     │
│ parquet       │
│ Text          │
│ Datasets      │
│ pandas        │
│ Croissant     │
│ Polars        │
│ 🇺🇸 Region: US │
│ mit           │
├───────────────┤
│    10 rows    │
└───────────────┘
```

Let's create a table of unique keywords:

```sql
CREATE OR REPLACE TABLE hf_keywords AS 
  WITH ks AS (
    SELECT trim(lower(unnest(keywords))) AS keyword
    FROM hf_metadata
  )
  SELECT keyword, count(keyword) AS count
  FROM ks
  WHERE keyword <> '""' AND length(keyword) > 0
  GROUP BY keyword;
```

Note that we convert the keywords to lower case and trim whitespace, _which needs to be done before the `GROUP BY` is performed_, then filter out apparent `""` and empty keywords.

```sql
D DESCRIBE hf_keywords;
┌─────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│ column_name │ column_type │  null   │   key   │ default │  extra  │
│   varchar   │   varchar   │ varchar │ varchar │ varchar │ varchar │
├─────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ keyword     │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ count       │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
└─────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘
D SELECT count() FROM hf_keywords;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│    19129     │
└──────────────┘
D SELECT * FROM hf_keywords ORDER BY count DESC NULLS FIRST LIMIT 100;
┌──────────────────────────────┬───────┐
│           keyword            │ count │
│           varchar            │ int64 │
├──────────────────────────────┼───────┤
│ 🇺🇸 region: us                │ 44614 │
│ croissant                    │ 39476 │
│ datasets                     │ 39450 │
│ text                         │ 35865 │
│ polars                       │ 33350 │
│ pandas                       │ 27411 │
│ apache-2.0                   │ 19824 │
│ mit                          │ 16917 │
│ parquet                      │ 15242 │
│ < 1k                         │ 13149 │
│ english                      │ 11334 │
│ json                         │ 11050 │
│ 1k - 10k                     │ 10955 │
│ 10k - 100k                   │  8140 │
│ csv                          │  7845 │
│ tabular                      │  6922 │
│ dask                         │  6706 │
│ image                        │  6040 │
│ text-generation              │  5259 │
│ 100k - 1m                    │  4530 │
│     ·                        │    ·  │
│     ·                        │    ·  │
│     ·                        │    ·  │
│ portuguese                   │   404 │
│ legal                        │   399 │
│ document-retrieval           │   389 │
│ afl-3.0                      │   386 │
│ italian                      │   375 │
│ table-question-answering     │   371 │
│ turkish                      │   363 │
│ visual-question-answering    │   347 │
│ finance                      │   327 │
│ sentence-transformers        │   324 │
│ hindi                        │   323 │
│ vietnamese                   │   311 │
│ machine-generated            │   309 │
│ mteb                         │   301 │
│ indonesian                   │   297 │
│ 10k<n<100k                   │   291 │
│ automatic-speech-recognition │   281 │
│ dutch                        │   278 │
│ chemistry                    │   271 │
│ zero-shot-classification     │   270 │
├──────────────────────────────┴───────┤
│ 100 rows (40 shown)        2 columns │
└──────────────────────────────────────┘
```

So there are other languages present! 

> **NOTE:** Look at the number of references to a few arXiv papers! We'll explore this below.

Let's see which languages we can find. 

### Languages

Let's save the keywords to a file to search for language entries with other tools (not shown here):

```sql
COPY (SELECT keyword, count FROM hf_keywords ORDER BY keyword) TO 'hf_keywords.csv';
```

```shell
$ head -10 hf_keywords.csv
head -10 hf_keywords.csv
keyword,count
#bert,1
#intent,1
'are'are,2
'auhelawa,4
'finance,1
/,17
0,4
0-bad,8
0-deepfake,1
```

There are some funky entries here...

Now, we need a list of the world's languages in a convenient format. Here are two JSON-formatted lists: [one](https://gist.github.com/jrnk/8eb57b065ea0b098d571), which claims to be an ISO list, and [two](https://gist.github.com/rglover/23d9d10d788c87e7fc5f5d7d8629633f). Even though the second list has more entries, ~240 vs. ~180, let's use the ISO list, saved to the file `data/reference/ISO-639-1-language.json`:

```sql
CREATE OR REPLACE TABLE iso_languages AS
  WITH langs AS (
    SELECT * FROM read_json('data/reference/ISO-639-1-language.json')
  )
  SELECT code, lower(name) AS name
  FROM langs;
```

The names are converted to lower case, so joins can be performed with the `keywords` table.

```sql
D DESCRIBE iso_languages;
┌─────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│ column_name │ column_type │  null   │   key   │ default │  extra  │
│   varchar   │   varchar   │ varchar │ varchar │ varchar │ varchar │
├─────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ code        │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ name        │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
└─────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘
D SELECT count() FROM iso_languages;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│     184      │
└──────────────┘
D SELECT * FROM iso_languages LIMIT 10;
┌─────────┬───────────┐
│  code   │   name    │
│ varchar │  varchar  │
├─────────┼───────────┤
│ aa      │ afar      │
│ ab      │ abkhazian │
│ ae      │ avestan   │
│ af      │ afrikaans │
│ ak      │ akan      │
│ am      │ amharic   │
│ an      │ aragonese │
│ ar      │ arabic    │
│ as      │ assamese  │
│ av      │ avaric    │
├─────────┴───────────┤
│ 10 rows   2 columns │
└─────────────────────┘
```

The input entries were in alphabetical order...

Now, let's see what we can find using just the language codes:

```sql
SELECT   ks.keyword, ks.count, ls.code, ls.name 
FROM     hf_keywords   ks
JOIN     iso_languages ls
ON       ks.keyword = ls.code
ORDER BY ks.count DESC;
```

```
┌─────────┬───────┬─────────┬───────────────────────┐
│ keyword │ count │  code   │         name          │
│ varchar │ int64 │ varchar │        varchar        │
├─────────┼───────┼─────────┼───────────────────────┤
│ cv      │    11 │ cv      │ chuvash               │
│ ko      │     9 │ ko      │ korean                │
│ ga      │     8 │ ga      │ irish                 │
│ it      │     7 │ it      │ italian               │
│ tt      │     7 │ tt      │ tatar                 │
│ mt      │     6 │ mt      │ maltese               │
│ en      │     6 │ en      │ english               │
│ ru      │     6 │ ru      │ russian               │
│ ml      │     6 │ ml      │ malayalam             │
│ ho      │     4 │ ho      │ hiri motu             │
│ cs      │     4 │ cs      │ czech                 │
│ uz      │     4 │ uz      │ uzbek                 │
│ tr      │     4 │ tr      │ turkish               │
│ fr      │     4 │ fr      │ french                │
│ ik      │     3 │ ik      │ inupiaq               │
│ wa      │     3 │ wa      │ walloon               │
│ eu      │     3 │ eu      │ basque                │
│ ja      │     3 │ ja      │ japanese              │
│ ha      │     3 │ ha      │ hausa                 │
│ pt      │     3 │ pt      │ portuguese            │
│ ·       │     · │ ·       │     ·                 │
│ ·       │     · │ ·       │     ·                 │
│ ·       │     · │ ·       │     ·                 │
│ uk      │     2 │ uk      │ ukrainian             │
│ hu      │     2 │ hu      │ hungarian             │
│ sa      │     2 │ sa      │ sanskrit              │
│ es      │     2 │ es      │ spanish; castilian    │
│ hi      │     2 │ hi      │ hindi                 │
│ fi      │     2 │ fi      │ finnish               │
│ eo      │     2 │ eo      │ esperanto             │
│ ar      │     2 │ ar      │ arabic                │
│ na      │     1 │ na      │ nauru                 │
│ el      │     1 │ el      │ greek, modern (1453-) │
│ no      │     1 │ no      │ norwegian             │
│ rm      │     1 │ rm      │ romansh               │
│ lv      │     1 │ lv      │ latvian               │
│ to      │     1 │ to      │ tonga (tonga islands) │
│ sq      │     1 │ sq      │ albanian              │
│ kg      │     1 │ kg      │ kongo                 │
│ zh      │     1 │ zh      │ chinese               │
│ kr      │     1 │ kr      │ kanuri                │
│ tg      │     1 │ tg      │ tajik                 │
│ mk      │     1 │ mk      │ macedonian            │
├─────────┴───────┴─────────┴───────────────────────┤
│ 44 rows (40 shown)                      4 columns │
└───────────────────────────────────────────────────┘
```

Lots of languages, but not a lot of datasets.

Now search for some of the languages seen in the keywords (e.g., browsing the `hf_keywords.csv` created above):

```sql
SELECT keyword, count
FROM hf_keywords WHERE keyword IN (
  'arabic',
  'aragonese',
  'aymara',
  'catalan',
  'chinese', 
  'english',
  'french', 
  'german',
  'hindi', 
  'hungarian',
  'italian',
  'japanese',
  'javanese',
  'korean',
  'nyanja',
  'portuguese', 
  'russian',
  'spanish',
  'turkish', 
  'vietnamese', 
  'volapük',
  'xhosa',
  )
ORDER BY count DESC NULLS FIRST;
```

```
┌────────────┬───────┐
│  keyword   │ count │
│  varchar   │ int64 │
├────────────┼───────┤
│ english    │ 11334 │
│ chinese    │  1175 │
│ french     │   777 │
│ russian    │   758 │
│ spanish    │   694 │
│ japanese   │   614 │
│ german     │   597 │
│ korean     │   469 │
│ arabic     │   464 │
│ portuguese │   404 │
│ italian    │   375 │
│ turkish    │   363 │
│ hindi      │   323 │
│ vietnamese │   311 │
│ hungarian  │   160 │
│ catalan    │   153 │
│ javanese   │    70 │
│ xhosa      │    68 │
│ nyanja     │    18 │
│ aragonese  │    16 │
│ aymara     │    15 │
│ volapük    │    15 │
├────────────┴───────┤
│ 22 rows  2 columns │
└────────────────────┘
```

Let's create a variation of `hf_metadata` generate a "concatenated" version of the language files. The first part of teh following query "unnests" the keywords, so we expand the records from, for example, one record with the keywords array `["lang1", "lang2", "lang3"]` to three records with individual `keyword` column values of `"lang1"`, etc.

```sql
CREATE OR REPLACE TABLE hf_languages AS
WITH expanded_keywords AS (
  SELECT trim(lower(unnest(keywords))) AS language_keyword,
    name,
    license,
    license_url,
    language,
    dataset_url,
    creator_name,
    creator_url,
    description
  FROM hf_metadata
)
SELECT * 
FROM expanded_keywords
WHERE language_keyword IN (
  'arabic',
  'catalan',
  'chinese',
  'english',
  'french',
  'german',
  'hindi',
  'hungarian',
  'italian',
  'japanese',
  'korean',
  'portuguese',
  'russian',
  'spanish',
  'turkish',
  'vietnamese'
);
```

```
D DESCRIBE hf_languages;
┌──────────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│   column_name    │ column_type │  null   │   key   │ default │  extra  │
│     varchar      │   varchar   │ varchar │ varchar │ varchar │ varchar │
├──────────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ language_keyword │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ name             │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ license          │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ license_url      │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ language         │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ dataset_url      │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ creator_name     │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ creator_url      │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ description      │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
└──────────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘
D SELECT * FROM hf_languages LIMIT 10;
┌──────────────────┬──────────────────────┬───┬─────────────────────┬──────────────────────┬──────────────────────┐
│ language_keyword │         name         │ … │    creator_name     │     creator_url      │     description      │
│     varchar      │       varchar        │   │       varchar       │       varchar        │       varchar        │
├──────────────────┼──────────────────────┼───┼─────────────────────┼──────────────────────┼──────────────────────┤
│ english          │ tinymistral-hypnos…  │ … │ James               │ https://huggingfac…  │ Dataset created fo…  │
│ russian          │ dataset-qa-ip-law    │ … │ lawful-good-project │ https://huggingfac…  │ Датасет для оценки…  │
│ vietnamese       │ alpaca_multiturns_…  │ … │ Hieu Lam            │ https://huggingfac…  │ \n\t\n\t\t\n\t\n\t…  │
│ vietnamese       │ lima_dialogue_vi     │ … │ Hieu Lam            │ https://huggingfac…  │ \n\t\n\t\t\n\t\n\t…  │
│ vietnamese       │ itorca_dpo_vi        │ … │ Hieu Lam            │ https://huggingfac…  │ \n\t\n\t\t\n\t\n\t…  │
│ english          │ itorca_dpo_en        │ … │ Hieu Lam            │ https://huggingfac…  │ \n\t\n\t\t\n\t\n\t…  │
│ english          │ slorca_dialogue_en   │ … │ Hieu Lam            │ https://huggingfac…  │ \n\t\n\t\t\n\t\n\t…  │
│ vietnamese       │ oasst_dialogue_vi    │ … │ Hieu Lam            │ https://huggingfac…  │ \n\t\n\t\t\n\t\n\t…  │
│ vietnamese       │ oasst_dialogue_base  │ … │ Hieu Lam            │ https://huggingfac…  │ \n\t\n\t\t\n\t\n\t…  │
│ english          │ oasst_dialogue_base  │ … │ Hieu Lam            │ https://huggingfac…  │ \n\t\n\t\t\n\t\n\t…  │
├──────────────────┴──────────────────────┴───┴─────────────────────┴──────────────────────┴──────────────────────┤
│ 10 rows                                                                                     9 columns (5 shown) │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
D SELECT count(*) FROM hf_languages;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│    18971     │
└──────────────┘
```

Now write it to a file:

```sql
COPY hf_languages TO './data/reference/hf_all_languages.json' (FORMAT json, ARRAY true);
```

A way to write the individual language files is to use `hf_languages`, e.g.,:

```sql
COPY (
  SELECT 
    name,
    license,
    license_url,
    language,
    dataset_url,
    creator_name,
    creator_url,
    description
  FROM hf_languages
  WHERE language_keyword = 'arabic'
) TO './data/json/processed/2025-05-12/languages/hf_arabic.json'
 (FORMAT json, ARRAY true);
```

> **NOTES:** 
>
> 1. I omitted the `language_keyword` field.
> 2. The `(FORMAT json, ARRAY true)` lets you use an alternative extension, but it's the default if the extension is `json`. The `ARRAY true` causes `duckdb` to write a JSON array, not just "JSONL" records. This is very useful for converting this output to a JavaScript file, discussed below.

Let's write several language datasets using `src/scripts/write-language-files.sh`. We'll put them in the directory, `./data/json/processed/YYYY-MM-DD/languages`, where the `YYYY-MM-DD` is treated as a "publication" date.

> **NOTE:** Since this section was written, I have moved to `src/scripts/write-category-files.py`, which also writes files for `modality` and `demain`, as well as `language`. Use it instead.

> **WARNING:** Make sure to exit out of `duckdb` first, if you have it running, because second invocations of it will fail in order to prevent possible corruption of `croissant.duckdb` when accessed from concurrent `duckdb` processes.

The script basically runs the following code:

```shell
timestamp=$(date "+%Y-%m-%d")
base=./data/json/processed/$timestamp/languages
mkdir -p $base
langs=(
  "arabic"
  "catalan"
  "chinese"
  "english"
  "french"
  "german"
  "hindi"
  "hungarian"
  "italian"
  "japanese"
  "korean"
  "portuguese"
  "russian"
  "spanish"
  "turkish"
  "vietnamese"
)
for lang in ${langs[@]}
do
  output=$base/hf_$lang.json
  cat <<EOF | duckdb croissant.duckdb
  COPY (
    SELECT 
      name,
      license,
      language,
      url,
      creator_name,
      creator_url,
      description
    FROM hf_languages
    WHERE language_keyword = '$lang'
  ) TO '$output' (FORMAT json, ARRAY true);
EOF
done
```

#### Making Valid JS Files

We need JavaScript files to import into the website. This required careful coding because of the embedded escaped quotes, newlines, etc. The following, for example, doesn't really work, because escapes get evaluated!

```shell
in=data/json/processed/2025-05-12/languages/hf_all_languages.json
out=data/json/processed/2025-05-12/languages/hf_all_languages.js
echo "var by_languages = " > $out
first_line=true
cat $in | while read line
do
  if $first_line
  then
    first_line=false
  else
    printf ",\n" >> $out
  fi
  printf "%s" "$line" >> $out
done
echo "\n];" >> $out
```

The script `src/scripts/write-category-files.py` properly handles creation of the JS files from the JSON files. It does the following:

1. Creates the JSON data files for _categories_ `modality`, `domain`, as well as `language`.
1. Creates the corresponding `_<category>/<keyword>.markdown` files (which are simple _boilerplate_).
1. Generates a JavaScript file from each JSON file.

The JavaScript files are copied to `docs` with `src/scripts/copy-files-to-docs.sh` that runs commands similar to the following:

```shell
# run from the static-catalog directory!!
ymd=$(date +"%Y-%m-%d")
for d in ./data/json/processed/$ymd/*
do
  group=$(basename $d)
  echo "JS for group: $group"
  rm -rf ../docs/files/data/catalog/$group
  mkdir -p ../docs/files/data/catalog/$group
  cp $d/*.js ../docs/files/data/catalog/$group
done
for d in ./markdown/processed/$ymd/*
do
  group=$(basename $d)
  echo "Markdown for group: $group"
  rm -rf ../docs/_$group
  mkdir -p ../docs/_$group
  cp $d/*.markdown ../docs/_$group
done
```

### ArXiv References?

We noticed the two arXiv references earlier. How many references are there to arXiv papers?

```sql
D SELECT keyword, count FROM hf_keywords WHERE keyword LIKE 'arxiv:%' ORDER BY count DESC LIMIT 10;
┌──────────────────┬───────┐
│     keyword      │ count │
│     varchar      │ int64 │
├──────────────────┼───────┤
│ arxiv:2204.07705 │  1176 │
│ arxiv:2407.00066 │  1173 │
│ arxiv:2208.01009 │    57 │
│ arxiv:2306.02707 │    39 │
│ arxiv:2401.06199 │    36 │
│ arxiv:2301.13688 │    24 │
│ arxiv:2501.19393 │    21 │
│ arxiv:1606.05250 │    21 │
│ arxiv:2110.14168 │    20 │
│ arxiv:2304.13705 │    20 │
├──────────────────┴───────┤
│ 10 rows        2 columns │
└──────────────────────────┘
```

## Other Keywords of Interest

For the interim static OTDI catalog, there are other keywords of interest:

* `automation` - or `industrial`, `manufacturing`, ...
* `molecular discovery` - or related terms like `chemistry`, `molecular`, `molecule`, `materials`, or variations thereof. 
* `time-series` - or variations thereof.

Modalities are interesting, including variations of the following:

* `audio`
* `image`
* `video`
* `text`
* `multimedia`

First, we used a similar query to the following above to get the language keywords, where we expand ("unnest") the array of `keywords`:

```sql
WITH expanded AS (
SELECT trim(lower(unnest(keywords))) AS keyword,
  name,
  license,
  license_url,
  language,
  dataset_url,
  creator_name,
  creator_url,
  description
FROM hf_metadata)
SELECT count() FROM expanded;
```

Let's create a table; we'll need it below.

```sql
CREATE OR REPLACE TABLE hf_expanded_metadata AS (
  SELECT trim(lower(unnest(keywords))) AS keyword,
    name,
    license,
    license_url,
    language,
    dataset_url,
    creator_name,
    creator_url,
    description
  FROM hf_metadata
);
```

It produces 499948 records from the original 44631 or 11 times as many! (Of course, this tells us the average number of keywords per dataset is 11... _These keywords go to 11!_)

What are the most common keywords? Let's find all of them with > 100 records:

```sql
SELECT keyword, count FROM hf_keywords WHERE count > 100 ORDER BY count DESC;
```

There are 164. Let's save to a file:

```sql
copy (SELECT keyword, count FROM hf_keywords WHERE count > 100 ORDER BY count DESC) 'biggest-keywords.csv'
```

As discussed above, we use `src/scripts/write-category-files.py` to write all the files for all the "popular" keywords we care about.

## Appendix: Running Some Test Queries

Here are some additional queries tried with DuckDB to look at the original Parquet files and the "raw" output FROM the Spark job. You can see a _lot_ more of them in `duckdb-notes.md`. Note that some of the details below may not match current table schemas:

```sql
DESCRIBE
  SELECT *
  FROM './data/json/2025-05-06_16-36-59/spark/*.json';
```

It prints:
```
┌─────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│ column_name │ column_type │  null   │   key   │ default │  extra  │
│   varchar   │   varchar   │ varchar │ varchar │ varchar │ varchar │
├─────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ croissant   │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
└─────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘
```

What about the input Parquet files?

```sql
DESCRIBE
  SELECT *
  FROM './data/raw/*.parquet';
```

It prints:

```
┌─────────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│   column_name   │ column_type │  null   │   key   │ default │  extra  │
│     varchar     │   varchar   │ varchar │ varchar │ varchar │ varchar │
├─────────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ dataset         │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ request_time    │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ response        │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ response_reason │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ croissant       │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
└─────────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘
```

```sql
SELECT * FROM './data/raw/*.parquet';
```

```
┌──────────────────────┬──────────────────────┬──────────┬─────────────────┬───────────────────────────────────────────┐
│       dataset        │     request_time     │ response │ response_reason │                 croissant                 │
│       varchar        │       varchar        │  int64   │     varchar     │                  varchar                  │
├──────────────────────┼──────────────────────┼──────────┼─────────────────┼───────────────────────────────────────────┤
│ FreedomIntelligenc…  │ 2025-03-17 04:04:5…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ facebook/natural_r…  │ 2025-03-17 04:04:5…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ open-r1/codeforces…  │ 2025-03-17 04:04:5…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ Congliu/Chinese-De…  │ 2025-03-17 04:04:5…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ SmallDoge/SmallTho…  │ 2025-03-17 04:04:5…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ open-r1/OpenR1-Mat…  │ 2025-03-17 04:04:5…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ gaia-benchmark/GAIA  │ 2025-03-17 04:04:5…  │      401 │ Unauthorized    │ {"error":"Access to dataset gaia-benchm…  │
│ CharlieDreemur/Ope…  │ 2025-03-17 04:04:5…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ fka/awesome-chatgp…  │ 2025-03-17 04:04:5…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ Conard/fortune-tel…  │ 2025-03-17 04:04:5…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ open-r1/codeforces   │ 2025-03-17 04:04:5…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ SynthLabsAI/Big-Ma…  │ 2025-03-17 04:04:5…  │      401 │ Unauthorized    │ {"error":"Access to dataset SynthLabsAI…  │
│ allenai/olmOCR-mix…  │ 2025-03-17 04:04:5…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ KodCode/KodCode-V1   │ 2025-03-17 04:04:5…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ madrylab/gsm8k-pla…  │ 2025-03-17 04:04:5…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ Intelligent-Intern…  │ 2025-03-17 04:04:5…  │      401 │ Unauthorized    │ {"error":"Access to dataset Intelligent…  │
│ a-m-team/AM-DeepSe…  │ 2025-03-17 04:04:5…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ openai/gsm8k         │ 2025-03-17 04:04:5…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ HuggingFaceFW/fine…  │ 2025-03-17 04:04:5…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ Congliu/Chinese-De…  │ 2025-03-17 04:04:5…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│          ·           │          ·           │       ·  │ ·               │                     ·                     │
│          ·           │          ·           │       ·  │ ·               │                     ·                     │
│          ·           │          ·           │       ·  │ ·               │                     ·                     │
│ gdsu/sdxl_images_s…  │ 2025-03-17 16:32:2…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ sert121/adult_data…  │ 2025-03-17 16:32:3…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ sert121/adult_data…  │ 2025-03-17 16:32:3…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ Tigressive/karen-l…  │ 2025-03-17 16:32:3…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ cat-searcher/code-…  │ 2025-03-17 16:32:3…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ mlfoundations-dev/…  │ 2025-03-17 16:32:3…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ mlfoundations-dev/…  │ 2025-03-17 16:32:3…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ sugarcokecola/eval…  │ 2025-03-17 16:32:3…  │      400 │ Bad Request     │ {"error":"The croissant format is not a…  │
│ sert121/adult_data…  │ 2025-03-17 16:32:3…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ wskang/datasets      │ 2025-03-17 16:32:3…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ sert121/adult_data…  │ 2025-03-17 16:32:3…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ pltops/Humour-Bench  │ 2025-03-17 16:32:3…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ gdsu/sdxl_images_e…  │ 2025-03-17 16:32:3…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ ellen2imagine/push…  │ 2025-03-17 16:32:3…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ sert121/adult_data…  │ 2025-03-17 16:32:3…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ RodainaMel/pfe-dat…  │ 2025-03-17 16:32:3…  │      400 │ Bad Request     │ {"error":"The croissant format is not a…  │
│ ZhiqiGao/TPBench     │ 2025-03-17 16:32:3…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ nthakur/bge-retrie…  │ 2025-03-17 16:32:3…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ ESITime/timesi-ari…  │ 2025-03-17 16:32:4…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
│ raftstudy/raft_sft…  │ 2025-03-17 16:32:4…  │      200 │ OK              │ {"@context":{"@language":"en","@vocab":…  │
├──────────────────────┴──────────────────────┴──────────┴─────────────────┴───────────────────────────────────────────┤
│ 332988 rows (40 shown)                                                                                     5 columns │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

So, it's clear we want to select for `response_reason = 'OK'`.

This is what we did in the Spark job, so that the set of JSON files only has "useful" content:

```sql
D SELECT * FROM './data/json/2025-05-06_16-36-59/spark/*.json' LIMIT 5;
```

It prints:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                      croissant                                                       │
│                                                       varchar                                                        │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ {"@context":{"@language":"en","@vocab":"https://schema.org/","citeAs":"cr:citeAs","column":"cr:column","conformsTo…  │
│ {"@context":{"@language":"en","@vocab":"https://schema.org/","citeAs":"cr:citeAs","column":"cr:column","conformsTo…  │
│ {"@context":{"@language":"en","@vocab":"https://schema.org/","citeAs":"cr:citeAs","column":"cr:column","conformsTo…  │
│ {"@context":{"@language":"en","@vocab":"https://schema.org/","citeAs":"cr:citeAs","column":"cr:column","conformsTo…  │
│ {"@context":{"@language":"en","@vocab":"https://schema.org/","citeAs":"cr:citeAs","column":"cr:column","conformsTo…  │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

How many records?

```sql
SELECT count(*) FROM './data/raw/*.parquet';
```

```
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│    332988    │
└──────────────┘
```

```sql
SELECT count(*) FROM './data/json/2025-05-06_16-36-59/spark/*.json';
```

```
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│    261495    │
└──────────────┘
```

So, about 79% of the queries for metadata were successful.

See `duckdb-notes.md` for additional queries that tried to use the DuckDB JSON functions to import the Spark output, with very limited success...
