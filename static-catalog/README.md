# README on Processing Hugging Face Metadata

Dean Wampler, May 11, 2025

> **NOTE:** This is a condensed version of the long `duckdb-notes.md` file, plus other notes, where Dean experimented with DuckDB, Spark, and other tools. This file covers the commands that worked.

## Introduction

We start with the metadata files created by Joe Olson's nightly job that queries Hugging Face for Croissant metadata. The format of those files is Parquet with a flat schema, with one column containing the entire JSON document for the metadata. Parsing that metadata proved difficult, because of deep "escape quoting". It was necessary to put together a set of tools to extract this metadata and load it into  [DuckDB](https://duckdb.org) for further analysis and processing.

## Initial Setup

Get a copy of the Parquet files with the Croissant metadata and use it as follows. Let's assume those Parquet files are in the current directory:

```shell
mkdir -p data/raw
mv *.parquet data/raw
mkdir -p data/json
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

Now create a metadata table:

```sql
CREATE OR REPLACE TABLE hf_metadata AS
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
  WHERE     license NOT NULL;
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
│ language     │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ url          │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ keywords     │ VARCHAR[]   │ YES     │ NULL    │ NULL    │ NULL    │
│ creator_name │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ creator_url  │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
└──────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘
D SELECT count(*) FROM hf_metadata;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│    60107     │
└──────────────┘
```

So, only 60K out of 261K records (23%) have a license! Not great. Let's see what those licenses are. First, let's tell `duckdb` to not truncate the output at the default of 40 rows. (Only ~75 lines are needed for the next query):

```sql
.maxrows 1234
```

```sql
SELECT license, count(license) AS count
FROM hf_metadata GROUP BY license ORDER BY count DESC NULLS FIRST;
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

Let's create a table of unique licenses. To do this, we need a convenient way to map the license ids in the URL to names. We extracted this information from the `choosealicense` [GitHub repo](https://github.com/github/choosealicense.com/tree/gh-pages/_licenses), specifically the [`_licenses`](https://github.com/github/choosealicense.com/tree/gh-pages/_licenses) directory. A JSON file was created here, ``./data/json/license-id-name-mapping.json`.

```sql
CREATE OR REPLACE TABLE hf_license_ids_names AS
  WITH licenses AS (
    SELECT * FROM read_json('data/json/ISO-639-1-language.json')
  )
  SELECT code, lower(name) AS name
  FROM licenses;
```

```sql
SELECT license, count(license) AS count
FROM hf_metadata GROUP BY license ORDER BY count DESC NULLS FIRST;
```

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
│ en       │ 60107 │
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
│ [openrail, < 1K, soundfolder, Audio, Datasets, Croissant, 🇺🇸 Region: US]                                             │
│ [mit, 10K - 100K, parquet, Text, Datasets, pandas, Croissant, Polars, 🇺🇸 Region: US]                                 │
│ [openrail, < 1K, soundfolder, Audio, Datasets, Croissant, 🇺🇸 Region: US]                                             │
│ [mit, 100K - 1M, csv, Text, Datasets, pandas, Croissant, Polars, 🇺🇸 Region: US]                                      │
│ [question-answering, text-generation, English, apache-2.0, 1M - 10M, parquet, Text, Datasets, Dask, Croissant, Pol…  │
│ [question-answering, Russian, gpl-3.0, < 1K, csv, Text, Datasets, pandas, Croissant, Polars, 🇺🇸 Region: US, legal]   │
│ [mit, < 1K, csv, Tabular, Datasets, pandas, Croissant, Polars, 🇺🇸 Region: US]                                        │
│ [mit, 10K - 100K, csv, Text, Datasets, pandas, Croissant, Polars, 🇺🇸 Region: US]                                     │
│ [mit, < 1K, csv, Tabular, Datasets, pandas, Croissant, Polars, 🇺🇸 Region: US]                                        │
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
│ openrail      │
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
│    22204     │
└──────────────┘
D SELECT * FROM hf_keywords ORDER BY count DESC NULLS FIRST LIMIT 100;
┌─────────────────────────────┬───────┐
│           keyword           │ count │
│           varchar           │ int64 │
├─────────────────────────────┼───────┤
│ 🇺🇸 region: us               │ 60087 │
│ croissant                   │ 53602 │
│ datasets                    │ 53565 │
│ text                        │ 45302 │
│ polars                      │ 41101 │
│ pandas                      │ 33572 │
│ < 1k                        │ 20500 │
│ apache-2.0                  │ 19824 │
│ parquet                     │ 18957 │
│ mit                         │ 16922 │
│ english                     │ 14703 │
│ json                        │ 13438 │
│ 1k - 10k                    │ 13192 │
│ 10k - 100k                  │ 10421 │
│ csv                         │  9680 │
│ tabular                     │  8697 │
│ image                       │  8688 │
│ dask                        │  8478 │
│ text-generation             │  6405 │
│ 100k - 1m                   │  5722 │
│ audio                       │  5661 │
│ openrail                    │  4568 │
│ soundfolder                 │  4388 │
│ question-answering          │  3848 │
│ text-classification         │  3830 │
│ imagefolder                 │  3565 │
│ cc-by-4.0                   │  3560 │
│ crowdsourced                │  3219 │
│ monolingual                 │  2689 │
│ 1m - 10m                    │  2660 │
│ video                       │  2515 │
│ robotics                    │  2304 │
│ time-series                 │  2285 │
│ lerobot                     │  2211 │
│ other                       │  2202 │
│ original                    │  2063 │
│ unknown                     │  2013 │
│ cc-by-sa-4.0                │  1595 │
│ chinese                     │  1563 │
│ summarization               │  1492 │
│ found                       │  1315 │
│ text2text-generation        │  1265 │
│ cc-by-nc-4.0                │  1250 │
│ image-to-text               │  1231 │
│ art                         │  1230 │
│ text-to-image               │  1224 │
│ arxiv:2204.07705            │  1176 │
│ arxiv:2407.00066            │  1173 │
│ feature-extraction          │  1160 │
│ synthetic                   │  1138 │
│ french                      │  1095 │
│ text-retrieval              │  1082 │
│ expert-generated            │  1077 │
│ cc-by-nc-sa-4.0             │  1072 │
│ token-classification        │  1069 │
│ multilingual                │  1068 │
│ cc0-1.0                     │  1034 │
│ 10m - 100m                  │  1014 │
│ translation                 │   992 │
│ tutorial                    │   992 │
│ russian                     │   988 │
│ spanish                     │   982 │
│ code                        │   953 │
│ japanese                    │   940 │
│ webdataset                  │   861 │
│ german                      │   852 │
│ language-modeling           │   841 │
│ 1k<n<10k                    │   838 │
│ cc                          │   838 │
│ sentence-similarity         │   834 │
│ image-classification        │   811 │
│ medical                     │   762 │
│ so100                       │   688 │
│ korean                      │   682 │
│ arabic                      │   673 │
│ multi-class-classification  │   635 │
│ infinite-dataset-hub        │   606 │
│ biology                     │   605 │
│ portuguese                  │   596 │
│ extractive-qa               │   592 │
│ topic-classification        │   578 │
│ multi-label-classification  │   577 │
│ italian                     │   564 │
│ named-entity-recognition    │   556 │
│ cc-by-nc-nd-4.0             │   531 │
│ gpl-3.0                     │   524 │
│ odc-by                      │   518 │
│ turkish                     │   508 │
│ machine-generated           │   502 │
│ legal                       │   498 │
│ object-detection            │   493 │
│ text-scoring                │   487 │
│ sentiment-analysis          │   475 │
│ hindi                       │   471 │
│ cc-by-sa-3.0                │   462 │
│ news-articles-summarization │   461 │
│ table-question-answering    │   452 │
│ visual-question-answering   │   449 │
│ document-retrieval          │   424 │
│ vietnamese                  │   423 │
├─────────────────────────────┴───────┤
│ 100 rows                  2 columns │
└─────────────────────────────────────┘
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
$ more hf_keywords.csv
keyword,count
#bert,1
#intent,1
#semantic-relatedness,1
#semantic-similarity,1
#sentence-relatedness,1
'\nsmalltalk class comments',1
'are'are,3
'auhelawa,8
'finance,1
'java class comments',1
'krm',1
'python class comments',1
'source code comments',1
/,17
0,4
0-bad,8
0-deepfake,1
0x22almostevil/multilingual-wikihow-qa-16k,1
...
```

There are some funky entries here...

Now, we need a list of the world's languages in a convenient format. Here are two JSON-formatted lists: [one](https://gist.github.com/jrnk/8eb57b065ea0b098d571), which claims to be an ISO list, and [two](https://gist.github.com/rglover/23d9d10d788c87e7fc5f5d7d8629633f). Even though the second list has more entries, ~240 vs. ~180, let's use the ISO list, saved to the file `data/json/ISO-639-1-language.json`:

```sql
CREATE OR REPLACE TABLE iso_languages AS
  WITH langs AS (
    SELECT * FROM read_json('ISO-639-1-language.json')
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
┌─────────┬───────┬─────────┬──────────────────────────────────┐
│ keyword │ count │  code   │               name               │
│ varchar │ int64 │ varchar │             varchar              │
├─────────┼───────┼─────────┼──────────────────────────────────┤
│ cv      │    13 │ cv      │ chuvash                          │
│ ga      │    12 │ ga      │ irish                            │
│ en      │    11 │ en      │ english                          │
│ ko      │    11 │ ko      │ korean                           │
│ ml      │     9 │ ml      │ malayalam                        │
│ mt      │     8 │ mt      │ maltese                          │
│ it      │     8 │ it      │ italian                          │
│ ru      │     7 │ ru      │ russian                          │
│ tt      │     7 │ tt      │ tatar                            │
│ ho      │     6 │ ho      │ hiri motu                        │
│ tw      │     6 │ tw      │ twi                              │
│ wa      │     6 │ wa      │ walloon                          │
│ tr      │     5 │ tr      │ turkish                          │
│ cs      │     5 │ cs      │ czech                            │
│ ik      │     4 │ ik      │ inupiaq                          │
│ uk      │     4 │ uk      │ ukrainian                        │
│ uz      │     4 │ uz      │ uzbek                            │
│ fr      │     4 │ fr      │ french                           │
│ ja      │     4 │ ja      │ japanese                         │
│ ha      │     4 │ ha      │ hausa                            │
│ de      │     3 │ de      │ german                           │
│ zh      │     3 │ zh      │ chinese                          │
│ eu      │     3 │ eu      │ basque                           │
│ sa      │     3 │ sa      │ sanskrit                         │
│ es      │     3 │ es      │ spanish; castilian               │
│ hr      │     3 │ hr      │ croatian                         │
│ pt      │     3 │ pt      │ portuguese                       │
│ ar      │     3 │ ar      │ arabic                           │
│ ak      │     3 │ ak      │ akan                             │
│ hu      │     2 │ hu      │ hungarian                        │
│ eo      │     2 │ eo      │ esperanto                        │
│ no      │     2 │ no      │ norwegian                        │
│ fi      │     2 │ fi      │ finnish                          │
│ to      │     2 │ to      │ tonga (tonga islands)            │
│ hi      │     2 │ hi      │ hindi                            │
│ fa      │     2 │ fa      │ persian                          │
│ as      │     2 │ as      │ assamese                         │
│ na      │     1 │ na      │ nauru                            │
│ sq      │     1 │ sq      │ albanian                         │
│ lv      │     1 │ lv      │ latvian                          │
│ kg      │     1 │ kg      │ kongo                            │
│ kr      │     1 │ kr      │ kanuri                           │
│ el      │     1 │ el      │ greek, modern (1453-)            │
│ tg      │     1 │ tg      │ tajik                            │
│ li      │     1 │ li      │ limburgan; limburger; limburgish │
│ rm      │     1 │ rm      │ romansh                          │
│ mk      │     1 │ mk      │ macedonian                       │
├─────────┴───────┴─────────┴──────────────────────────────────┤
│ 47 rows                                            4 columns │
└──────────────────────────────────────────────────────────────┘
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
┌───────────────┬───────┐
│ lower_keyword │ count │
│    varchar    │ int64 │
├───────────────┼───────┤
│ english       │ 14703 │
│ chinese       │  1563 │
│ french        │  1095 │
│ russian       │   988 │
│ spanish       │   983 │
│ japanese      │   940 │
│ german        │   852 │
│ korean        │   682 │
│ arabic        │   675 │
│ portuguese    │   596 │
│ italian       │   564 │
│ turkish       │   508 │
│ hindi         │   471 │
│ vietnamese    │   423 │
│ catalan       │   235 │
│ hungarian     │   235 │
│ javanese      │   101 │
│ xhosa         │   101 │
│ aragonese     │    30 │
│ nyanja        │    29 │
│ volapük       │    26 │
│ aymara        │    24 │
├───────────────┴───────┤
│ 22 rows     2 columns │
└───────────────────────┘
```

Let's create a variation of `hf_metadata` generate a "concatenated" version of the language files. The first part of teh following query "unnests" the keywords, so we expand the records from, for example, one record with the keywords array `["lang1", "lang2", "lang3"]` to three records with individual `keyword` column values of `"lang1"`, etc.

```sql
CREATE OR REPLACE TABLE hf_languages AS
WITH expanded_keywords AS (
  SELECT trim(lower(unnest(keywords))) AS language_keyword,
    name,
    license,
    language,
    url,
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
│ language         │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ url              │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ creator_name     │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ creator_url      │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ description      │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
└──────────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘
D SELECT * FROM hf_languages LIMIT 10;
┌──────────────────┬──────────────────────┬──────────────────────┬───┬──────────────────────┬──────────────────────┐
│ language_keyword │         name         │       license        │ … │     creator_url      │     description      │
│     varchar      │       varchar        │       varchar        │   │       varchar        │       varchar        │
├──────────────────┼──────────────────────┼──────────────────────┼───┼──────────────────────┼──────────────────────┤
│ english          │ tinymistral-hypnos…  │ https://choosealic…  │ … │ https://huggingfac…  │ Dataset created fo…  │
│ russian          │ dataset-qa-ip-law    │ https://choosealic…  │ … │ https://huggingfac…  │ Датасет для оценки…  │
│ vietnamese       │ alpaca_multiturns_…  │ https://choosealic…  │ … │ https://huggingfac…  │ \n\t\n\t\t\n\t\n\t…  │
│ vietnamese       │ lima_dialogue_vi     │ https://choosealic…  │ … │ https://huggingfac…  │ \n\t\n\t\t\n\t\n\t…  │
│ vietnamese       │ itorca_dpo_vi        │ https://choosealic…  │ … │ https://huggingfac…  │ \n\t\n\t\t\n\t\n\t…  │
│ english          │ itorca_dpo_en        │ https://choosealic…  │ … │ https://huggingfac…  │ \n\t\n\t\t\n\t\n\t…  │
│ english          │ slorca_dialogue_en   │ https://choosealic…  │ … │ https://huggingfac…  │ \n\t\n\t\t\n\t\n\t…  │
│ vietnamese       │ oasst_dialogue_vi    │ https://choosealic…  │ … │ https://huggingfac…  │ \n\t\n\t\t\n\t\n\t…  │
│ vietnamese       │ oasst_dialogue_base  │ https://choosealic…  │ … │ https://huggingfac…  │ \n\t\n\t\t\n\t\n\t…  │
│ english          │ oasst_dialogue_base  │ https://choosealic…  │ … │ https://huggingfac…  │ \n\t\n\t\t\n\t\n\t…  │
├──────────────────┴──────────────────────┴──────────────────────┴───┴──────────────────────┴──────────────────────┤
│ 10 rows                                                                                      8 columns (5 shown) │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
D SELECT count(*) FROM hf_languages;
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│    25511     │
└──────────────┘
```

Now write it to a file:

```sql
COPY hf_languages TO './data/json/processed/2025-05-12/languages/hf_all_languages.json';
```

A way to write the individual language files is to use `hf_languages`, e.g.,:

```sql
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
  WHERE language_keyword = 'arabic'
) TO './data/json/processed/2025-05-12/languages/hf_arabic.json';
```

Note that I omitted the `language_keyword` field.

Let's write several language datasets, using the following shell command (see also `src/scripts/write-language-files.sh`. We'll put them in the directory, `./data/json/processed/YYYY-MM-DD/languages`, where the `YYYY-MM-DD` is treated as a "publication" date.

> **NOTE:** Make sure to exit out of `duckdb` first, just in case it might corrupt `croissant.duckdb` to access it from separate instances of `duckdb`.

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
  ) TO '$output';
EOF
done
ls -l $base
```

```
total 124528
-rw-r--r--   1 ...  20M May 12 12:13 hf_all_languages.js
-rw-r--r--   1 ...  21M May 12 12:30 hf_all_languages.json
-rw-r--r--@  1 ... 565K May 12 12:40 hf_arabic.json
-rw-r--r--@  1 ... 204K May 12 12:40 hf_catalan.json
-rw-r--r--@  1 ... 1.3M May 12 12:40 hf_chinese.json
-rw-r--r--@  1 ...  11M May 12 12:40 hf_english.json
-rw-r--r--@  1 ... 915K May 12 12:40 hf_french.json
-rw-r--r--@  1 ... 710K May 12 12:40 hf_german.json
-rw-r--r--@  1 ... 377K May 12 12:40 hf_hindi.json
-rw-r--r--@  1 ... 193K May 12 12:40 hf_hungarian.json
-rw-r--r--@  1 ... 456K May 12 12:40 hf_italian.json
-rw-r--r--@  1 ... 798K May 12 12:40 hf_japanese.json
-rw-r--r--@  1 ... 552K May 12 12:40 hf_korean.json
-rw-r--r--@  1 ... 471K May 12 12:40 hf_portuguese.json
-rw-r--r--@  1 ... 740K May 12 12:40 hf_russian.json
-rw-r--r--@  1 ... 806K May 12 12:40 hf_spanish.json
-rw-r--r--@  1 ... 395K May 12 12:40 hf_turkish.json
-rw-r--r--@  1 ... 327K May 12 12:40 hf_vietnamese.json
```

For example,

```shell
$ head -1 data/json/processed/2025-05-12/languages/hf_vietnamese.json
{"name":"alpaca_multiturns_dialogue_vi","description":"\\n\\t\\n\\t\\t\\n\\t\\n\\t\\n\\t\\tDescription\\n\\t\\n\\nThe dataset is from 5CD-AI/Vietnamese-Multi-turn-Chat-Alpaca, formatted as dialogues for speed and ease of use. Many thanks to 5CD-AI for releasing it.\\nImportantly, this format is easy to use via the default chat template of transformers, meaning you can use huggingface/alignment-handbook immediately, unsloth.\\n\\n\\t\\n\\t\\t\\n\\t\\n\\t\\n\\t\\tStructure\\n\\t\\n\\nView online through viewer.\\n\\n\\t\\n\\t\\t\\n\\t\\n\\t\\n\\t\\tNote\\n\\t\\n\\nWe advise you to reconsider before use, thank you. If you find it useful, please like… See the full description on the dataset page: https://huggingface.co/datasets/lamhieu/alpaca_multiturns_dialogue_vi.","license":"https://choosealicense.com/licenses/mit/","language":"en","url":"https://huggingface.co/datasets/lamhieu/alpaca_multiturns_dialogue_vi","creator_name":"Hieu Lam","creator_url":"https://huggingface.co/lamhieu"}
```

We might still want to replace the `\\` with `\`...

#### Making Valid JS Files

We need JavaScript files to import into the website, for example:

```shell
in=data/json/processed/2025-05-12/languages/hf_all_languages.json
out=data/json/processed/2025-05-12/languages/hf_all_languages.js
echo "var by_languages = [" > $out
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

The script `src/scripts/make-js-files.sh` creates these `*.js` files for all the `hf_*.json` files in `data/json/processed/YYYY-MM-DD/languages/` for today's date.

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
│ arxiv:2406.08464 │    52 │
│ arxiv:2306.02707 │    46 │
│ arxiv:2401.06199 │    36 │
│ arxiv:2301.13688 │    30 │
│ arxiv:1606.05250 │    24 │
│ arxiv:2110.14168 │    21 │
│ arxiv:2203.02155 │    21 │
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


## Appendix: Running Some Test Queries

Here are some additional queries tried with DuckDB to look at the original Parquet files and the "raw" output FROM the Spark job. You can see a _lot_ more of them in `duckdb-notes.md`f:

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
