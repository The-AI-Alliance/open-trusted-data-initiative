# Notes on Using DuckDB to Analyze the HF Metadata

## Getting Started

Install the [DuckDB](https://duckdb.org) CLI tools and Python library. See the [documentation](https://duckdb.org/docs/stable/).

The tools, such as the `duckdb` CLI:

```shell
curl https://install.duckdb.org | sh
```

The Python library:

```shell
pip install duckdb
```

## Using the JSON Support in the `duckdb` CLI

The JSON processing functions are [documented here](https://duckdb.org/docs/stable/data/json/json_functions.html).

In the CLI, you install the `json` module. Start the CLI `duckdb`, then at the `D` prompt (which I'll always omit in what follows...):

```
install 'json';
load 'json';
```

## Running Some Test Queries

Let's start with the output FROM a Spark job I ran to extract JSON data FROM the original Parquet files:

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

So, we see that we'll want to select for `response_reason = 'OK'`.

This is what we did in the Spark, so that set of JSON files only has "useful" content:

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

Let's play with the DuckDB JSON functions:

```sql
SELECT *
FROM read_ndjson_objects('./data/json/2025-05-06_16-36-59/spark/*.json')
LIMIT 100;
```

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                         json                                                         │
│                                                         json                                                         │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│                                                          ·                                                           │
│                                                          ·                                                           │
│                                                          ·                                                           │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
│ {"croissant":"{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"co…  │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                 100 rows (40 shown)                                                  │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```sql
DESCRIBE
  SELECT *
  FROM read_ndjson_objects('./data/json/2025-05-06_16-36-59/spark/*.json')
  LIMIT 100;
```
```
┌─────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│ column_name │ column_type │  null   │   key   │ default │  extra  │
│   varchar   │   varchar   │ varchar │ varchar │ varchar │ varchar │
├─────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ json        │ JSON        │ YES     │ NULL    │ NULL    │ NULL    │
└─────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘
```

Note that the JSON structure for all the records is basically `{"croissant": "big-complicated-string"}`. Converting that string to JSON itself is the next big challenge.

> **NOTE:** I read that DuckDB can automatically infer that each row is a separate JSON "document". The files don't have to be structured as "JSONL" or similar. DuckDB tries to flexibly interpret intent.


```sql
SELECT json_group_structure(json)
    FROM (
      SELECT *
      FROM read_ndjson_objects('./data/json/2025-05-06_16-36-59/spark/*.json')
      LIMIT 100
    );
```

```
┌──────────────────────────────┐
│ json_group_structure("json") │
│             json             │
├──────────────────────────────┤
│ {"croissant":"VARCHAR"}      │
└──────────────────────────────┘
```


Let's try to extract the JSON and parse it.

```sql
SELECT json.croissant
  FROM (
    SELECT *
    FROM read_ndjson_objects('./data/json/2025-05-06_16-36-59/spark/*.json')
    LIMIT 100
  );
```

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                      croissant                                                       │
│                                                         json                                                         │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ "{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"column\":\"cr:c…  │
│ ...                                                                                                                  │
│ "{\"@context\":{\"@language\":\"en\",\"@vocab\":\"https://schema.org/\",\"citeAs\":\"cr:citeAs\",\"column\":\"cr:c…  │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                 100 rows (40 shown)                                                  │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

So, this returns just the JSON string itself. Can we reference `croissant` in the outer function call?

```sql
SELECT json_group_structure(croissant)
  FROM (
    SELECT json.croissant
      FROM (
        SELECT *
        FROM read_ndjson_objects('./data/json/2025-05-06_16-36-59/spark/*.json')
        LIMIT 100
      )
  );
```

```
┌─────────────────────────────────┐
│ json_group_structure(croissant) │
│              json               │
├─────────────────────────────────┤
│ "VARCHAR"                       │
└─────────────────────────────────┘
```

Not that helpful...

Can we pass a query to `read_ndjson_objects`?

```sql
SELECT json_group_structure(croissant)
  FROM read_ndjson_objects(
    SELECT json.croissant
      FROM (
        SELECT *
        FROM read_ndjson_objects('./data/json/2025-05-06_16-36-59/spark/*.json')
        LIMIT 100
      )
  );
```

Nope...


## More Sophisticated Parsing of JSON

I found this [blog post](https://rpbouman.blogspot.com/2024/12/duckdb-bag-of-tricks-reading-json-data.html) about working with JSON. Let's experiment with the ideas it presents, starting with providing type information and specifying just the JSON fields we care about.

First, recall what we saw above about how what is inferred for the schema:

```sql
DESCRIBE
SELECT *
FROM './data/json/2025-05-06_16-36-59/spark/*.json';
```

```
┌─────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│ column_name │ column_type │  null   │   key   │ default │  extra  │
│   varchar   │   varchar   │ varchar │ varchar │ varchar │ varchar │
├─────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ croissant   │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
└─────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘
```

```sql
DESCRIBE
SELECT *
FROM './data/raw/*.parquet';
```
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

Now, let's try the ideas from the "bag of tricks" post:

```sql
CREATE OR REPLACE TABLE hf_croissant AS
SELECT * 
  FROM read_json(
    './data/json/2025-05-06_16-36-59/spark/*.json',
    columns =  {
      croissant: 'STRUCT(
                    creator STRUCT(
                      name VARCHAR,
                      url VARCHAR
                    ), 
                    name VARCHAR,
                    description VARCHAR,
                    url VARCHAR,
                    license VARCHAR,
                    "@context" STRUCT(
                      language VARCHAR
                    )
                  )'
    },
    auto_detect = true,
    format = 'newline_delimited',
    records = true
  );
```

```
Invalid Input Error:
JSON transform error in file "./data/json/2025-05-06_16-36-59/spark/part-00001-47603599-0b24-4d2e-bc83-88984308c705-c000.json", in line 1: Expected OBJECT, but got VARCHAR: "{\"@context\":{\"@language\":\"en\",\"@vocab\":\"...
Try setting 'auto_detect' to true, specifying 'format' or 'records' manually, or setting 'ignore_errors' to true.
```

(The suggestions I applied after running the same query without them.) Instead of the JSON files, let's try using the earlier query that extracted the values from the `croissant` column:

```sql
CREATE OR REPLACE TABLE hf_croissant1 AS
  FROM (
    SELECT json.croissant
    FROM (
      SELECT *
      FROM read_ndjson_objects('./data/json/2025-05-06_16-36-59/spark/*.json')
      LIMIT 100
    )
  );
COPY hf_croissant1 TO './data/json/2025-05-06_16-36-59/croissant.json';
```

This actually writes records like `{"croissant": string}`, where we want the `string`. We could try using `read_text`, as described in the blog post, but it's not going to work as described with non-JSON data, but we can use the subsequent queries there as motivations.

```sql
CREATE OR REPLACE TABLE hf_croissant2 AS
  FROM (
    SELECT json.croissant::JSON as croissant
    FROM (
      SELECT *
      FROM read_ndjson_objects('./data/json/2025-05-06_16-36-59/spark/*.json')
      LIMIT 100
    )
  );
DESCRIBE hf_croissant2;
COPY hf_croissant2 TO './data/json/2025-05-06_16-36-59/croissant.json';

SELECT * FROM hf_croissant2 LIMIT 1;
SELECT json_keys(croissant) FROM hf_croissant2 LIMIT 5;
SELECT unnest(json_keys(croissant)) FROM hf_croissant2 LIMIT 5;
SELECT json_keys(unnest(croissant)) FROM hf_croissant2 LIMIT 5;

SELECT json_structure(croissant) FROM hf_croissant2 LIMIT 5;  # returns "VARCHAR" for all rows
SELECT json_type(croissant) FROM hf_croissant2 LIMIT 5;       # returns VARCHAR for all rows
SELECT json(croissant) FROM hf_croissant2 LIMIT 5;            # Doesn't appear to do anything! The results look just like `SELECT croissant...`
SELECT croissant FROM hf_croissant2 LIMIT 5;  
SELECT json_structure(json(croissant)) FROM hf_croissant2 LIMIT 5;
SELECT json_type(json(croissant)) FROM hf_croissant2 LIMIT 5;
SELECT json(json(croissant)) FROM hf_croissant2 LIMIT 5;      # "Recursive" invocations do nothing!
SELECT json_extract(croissant, '$."@context"."@language"') FROM hf_croissant2 LIMIT 5;
SELECT json_extract(json(croissant), '$."@context"."@language"') FROM hf_croissant2 LIMIT 5;
SELECT json_extract(json_extract(croissant, '$'), '$."@context"."@language"') FROM hf_croissant2 LIMIT 5;
SELECT json_extract(croissant, '$') FROM hf_croissant2 LIMIT 5;
SELECT json_extract(json(croissant), '$') FROM hf_croissant2 LIMIT 5;
SELECT json_extract(json_extract(croissant, '$'), '$') FROM hf_croissant2 LIMIT 5;

SELECT json_extract('{"@context":{"@language":"en","@vocab":"https://schema.org/"}}', '$."@context"."@language"');
CREATE TABLE example (j JSON);
INSERT INTO example (
  SELECT json(croissant) FROM hf_croissant2 LIMIT 5
);
SELECT json_structure(j) FROM example;

SELECT croissant->'@context' FROM hf_croissant2 LIMIT 5;  
SELECT json_extract(croissant, '.') AS cr FROM hf_croissant2 LIMIT 5;
SELECT json_extract(croissant, 'description') AS cr FROM hf_croissant2 LIMIT 5;
SELECT json_extract(croissant, '"description"') AS cr FROM hf_croissant2 LIMIT 5;
SELECT json_extract(croissant, '.description') AS cr FROM hf_croissant2 LIMIT 5;
SELECT json_extract(croissant, '."description"') AS cr FROM hf_croissant2 LIMIT 5;
```

New JSON files. First `./data/json/sample/*.json` are the Spark snapshots I"e used above in a more convenient place and with easier to use names, and
`toss.json` created from `1.json` with this:

```shell
cat ./data/json/sample/1.json | jq .croissant | sed -e 's/^"//' -e 's/"$//' -e 's/\([^\\]\)\\"/\1"/g' > toss1.json
cat ./data/json/sample/1.json | jq .croissant | sed -e 's/^"//' -e 's/"$//' > toss2.json
```

Trying these files. `toss1.json` ends up with malformed JSON. The unquoting regex, which attempts to only change "top level" `\"`, but not nested ones like `\\"`, doesn't work. Tried `toss2.json`, which is less aggressively formatted, but it also doesn't work; the `\` at position two in `{\"foo\": ...}  doesn't work. (It says "line 2", but a one-line file does the same thing! Weird counting...)

Trying some shell commands to get the "unquoting" right:

```shell
head -5 ./data/json/sample/1.json > head5.json 
jq .croissant head5.json | sed -e 's/^"//'  -e 's/"$//'  -e 's/\([^\\]\)\\"/\1"/g' > toss-jq2b.json
```

This shell script follows a potentially-crucial insight I had; piping the output of `head` directly to `sed` causes escapes (`\`) to be evaluated differently than if I write to a file, then read it back!

Is the following Python script actually necessary (also in `parse.py`)?
```python
import os, io, json

def read_file_line_by_line(in_file_path):
    try:
        count = 0
        with open(in_file_path, 'r') as file:
            for line in iter(lambda: file.readline().strip(), ''):
                count += 1
                line = line.strip()
                yield count, line
    except FileNotFoundError:
        print(f"File {in_file_path} not found.")   

def print_to_string(str, **kwargs):
    output = io.StringIO()
    print(str, file=output, end='', **kwargs)
    contents = output.getvalue()
    output.close()
    return contents

def delete_file(file_path):
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            os.remove(file_path)
            print(f"File {file_path} deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print(f"File {file_path} does not exist or is not a file.")

in_file_path  = "toss-jq2.json"
out_file_path = "toss-jq3.json"
delete_file(out_file_path)

with open(out_file_path, 'w') as out:
    for i, line in read_file_line_by_line(in_file_path):
        try:
            line2 = print_to_string(line)
            js = json.loads(line2)
        except json.decoder.JSONDecodeError as err:
            print(f"json.decoder.JSONDecodeError: {err}: line {i}: {line2}")
            raise err
        except Error as err:
            print(f"Error: {err}: line {i}: {line2}")
            raise err
        json.dump(js, out)
        print("", file=out)
```

No! The only difference is `toss-jq3.json` gets some extra whitespace, but they are functionally identical. It appears that the shell commands are sufficient to unquote as needed, at least for the first 5 lines of the file.

Since I wrote the Python code, let's see if it works directly on `./data/json/sample/1.json` (i.e., change the definition of `in_file_path`). No, it appears to only change the whitespace in the file, not remove the escapes, etc.


Now try loading `toss-jq2.json`:

```sql
CREATE OR REPLACE TABLE hf_croissant2 AS
  FROM (
    SELECT *
    FROM read_ndjson_objects('toss-jq2.json')
    LIMIT 100
  );
DESCRIBE hf_croissant2;
select * from hf_croissant2;
```

Is it good??

```sql
SELECT json->'@context'->'@language' FROM hf_croissant2 LIMIT 5; 
```
```
┌─────────────────────────────────────────┐
│ (("json" -> '@context') -> '@language') │
│                  json                   │
├─────────────────────────────────────────┤
│ "en"                                    │
│ "en"                                    │
│ "en"                                    │
│ "en"                                    │
│ "en"                                    │
└─────────────────────────────────────────┘
```

and
```sql 
SELECT json_extract(json, 'description') FROM hf_croissant2 LIMIT 5;
```

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                      json_extract("json", 'description')                                      │
│                                                     json                                                      │
├───────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ "CAiRE/prosocial-dialog-zho_Hans dataset hosted on Hugging Face and contributed by the HF Datasets community" │
│ "CAiRE/prosocial-dialog-jpn_Jpan dataset hosted on Hugging Face and contributed by the HF Datasets community" │
│ "CAiRE/prosocial-dialog-ind_Latn dataset hosted on Hugging Face and contributed by the HF Datasets community" │
│ "Please refer to our GitHub repo for more details.\\n"                                                        │
│ "haganelego/wikiart_512x512 dataset hosted on Hugging Face and contributed by the HF Datasets community"      │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Yes! Finally, parseable JSON!!

Okay. Now let's try all the records:

```shell
jq .croissant ./data/json/sample/*.json | sed -e 's/^"//'  -e 's/"$//' -e 's/\([^\\]\)\\"/\1"/g' > dequoted-1.json
wc dequoted-1.json
head -1 dequoted-1.json
```

`wc` printed `261495 52099629 2604796536 dequoted-1.json`.

Let's try a table:

```sql
CREATE OR REPLACE TABLE hf_croissant AS
  FROM (
    SELECT *
    FROM read_ndjson_objects('dequoted-1.json')
    LIMIT 100
  );
DESCRIBE hf_croissant;
SELECT * FROM hf_croissant LIMIT 2;
```
```
Malformed JSON in file "dequoted-1.json", at byte 5824 in line 271: unexpected character.
```

Okay, it turns out that line 271 in `1.json` where the `sed` command converted a `\"\",` (i.e., an empty string) into `"\",`, which cause JSON parsing to fail. I determined this using my personal `~/bin/print-lines.sh` script, e.g., `~/bin/print-lines.sh -s 270:1 -p 5800:100 dequoted-1.json` covering the line (`270`) and character position (`5824`) where DuckDB reported a problem:

```shell
$ ~/bin/print-lines.sh -s 270:1 -p 5800:100 dequoted-1.json
-sa-4.0/","sameAs":"\","url":"https://huggingface.co/datasets/chenghao/sec-material-contracts"}
```

(`awk` is used in `print-lines.sh`, which counts from 1, it appears that the error is actually on line 270 in the data file, despite what DuckDB says.)

Let's try adding another clause to the `sed` command to first convert `\"\"`  to `""`:

```shell
jq .croissant ./data/json/sample/*.json | sed -e 's/^"//'  -e 's/"$//' -e 's/\\"\\"/""/g' -e 's/\([^\\]\)\\"/\1"/g' > dequoted-2.json
wc dequoted-2.json
head dequoted-2.json
```

Fixed?

```shell
$ ~/bin/print-lines.sh -s 270:1 -p 5800:100 dequoted-2.json
-sa-4.0/","sameAs":"","url":"https://huggingface.co/datasets/chenghao/sec-material-contracts"}
```

Yes! Okay, trying the table again:

```sql
CREATE OR REPLACE TABLE hf_croissant AS
  FROM (
    SELECT *
    FROM read_ndjson_objects('dequoted-2.json')
    LIMIT 100
  );
DESCRIBE hf_croissant;
SELECT * FROM hf_croissant LIMIT 2;
```

Next problem:

```
Malformed JSON in file "dequoted-2.json", at byte 4531 in line 2288: unexpected character.
```

```shell
$ ~/bin/print-lines.sh -s 2287:1 -p 4450:150 dequoted-2.json
t0rm0/glove.6B.50d.umap.2d","\\\"UMAP 2D-Projection of glove.6B.50d embeddings\\""],"creator":{"@type":"Person","name":"Mario Tormo Romero","url":"htt```
```

Let's find that string in the source JSON files:

```shell
$ grep -n 'UMAP 2D-Projection' ./data/json/sample/*.json
./data/json/sample/1.json:2287:{"croissant":\"alternateName\":[\"mt0rm0/glove.6B.50d.umap.2d\",\"\\\"UMAP 2D-Projection of glove.6B.50d embeddings\\\"\"],\"creator\":{\"@type\"...}
```

`alternateName` is a top-level key in the records. It's odd that the second element in the array has this weird escaping. Let's add more `sed` clauses to fix this case.

```shell
time jq .croissant ./data/json/sample/*.json | \
  sed -e 's/^"//'  -e 's/"$//' -e 's/\\"\\"/""/g' -e 's/\([^\\]\)\\"/\1"/g' -e 's/"\\\\\\"/"/g' -e 's/\\\\""/"/g' > dequoted-3.json
wc dequoted-3.json
head -1 dequoted-3.json
~/bin/print-lines.sh -s 2287:1 -p 4450:150 dequoted-3.json
```

```
...
t0rm0/glove.6B.50d.umap.2d","UMAP 2D-Projection of glove.6B.50d embeddings"],"creator":{"@type":"Person","name":"Mario Tormo Romero","url":"https://hu
```

Better. Try the table again and keep fixing similar issues:

```shell
$ ~/bin/print-lines.sh -s 6882:1 -p 8100:100 dequoted-3.json
ig-default"},"extract":{"column":"\\\\\"}}},{"@type":"cr:Field","@id":"default/_","name":"default/_"
$ jq .croissant ./data/json/sample/*.json | \
  sed -e 's/^"//'  -e 's/"$//' -e 's/\\"\\"/""/g' -e 's/\([^\\]\)\\"/\1"/g' -e 's/"\\\\\\"/"/g' -e 's/\\\\""/"/g' -e 's/:\s*"\\[\\]*"/:""/g' > dequoted-4.json
$ ~/bin/print-lines.sh -s 6882:1 -p 8100:100 dequoted-4.json

# Attempt to create table:
# Invalid Input Error:
# Malformed JSON in file "dequoted-4.json", at byte 3799 in line 10755: unexpected character.
$ ~/bin/print-lines.sh -s 10754:1 -p 3750:100 dequoted-4.json
nateName":["ragha92/FNS_Summarization","\\\\\"],"creator":{"@type":"Person","name":"Raghasai K","url
$ jq .croissant ./data/json/sample/*.json | \
  sed -e 's/^"//'  -e 's/"$//' -e 's/\\"\\"/""/g' -e 's/\([^\\]\)\\"/\1"/g' -e 's/"\\\\\\"/"/g' -e 's/\\\\""/"/g' -e 's/\([:,]\)\s*"\\[\\]*"/\1""/g' > dequoted-5.json
$ ~/bin/print-lines.sh -s 10754:1 -p 3750:100 dequoted-5.json
nateName":["ragha92/FNS_Summarization",""],"creator":{"@type":"Person","name":"Raghasai K","url":"ht

# Attempt to create table:
# Invalid Input Error:
# Malformed JSON in file "dequoted-5.json", at byte 19450 in line 65493: unexpected character.
$ ~/bin/print-lines.sh -s 65492:1 -p 19400:100 dequoted-5.json
r":{"@type":"Person","name":"matteo manias\\\\\","url":"https://huggingface.co/matteo1822"},"keyword
$ jq .croissant ./data/json/sample/*.json | \
  sed -e 's/^"//'  -e 's/"$//' -e 's/\\"\\"/""/g' -e 's/\([^\\]\)\\"/\1"/g' -e 's/"\\\\\\"/"/g' -e 's/\\\\""/"/g' -e 's/\([:,]\)\s*"\\[\\]*"/\1""/g' -e 's/manias\(\\*\)"/manias"/g' > dequoted-6.json
$ ~/bin/print-lines.sh -s 65492:1 -p 19400:100 dequoted-6.json
r":{"@type":"Person","name":"matteo manias","url":"https://huggingface.co/matteo1822"},"keywords":["

# Attempt to create table:
# Invalid Input Error:
# Malformed JSON in file "dequoted-6.json", at byte 3381 in line 155646: unexpected character.
$ ~/bin/print-lines.sh -s 155645:1 -p 3350:100 dequoted-6.json
me":"HAL9000","description":"" HAL9000Alfa es un pequeño programa que crea un chat conversacional,
$ jq .croissant ./data/json/sample/*.json | \
  sed -e 's/^"//'  -e 's/"$//' -e 's/\\"\\"/""/g' -e 's/\([^\\]\)\\"/\1"/g' -e 's/"\\\\\\"/"/g' -e 's/\\\\""/"/g' -e 's/\([:,]\)\s*"\\[\\]*"/\1""/g' -e 's/manias\(\\*\)"/manias"/g' -e 's/"" HAL9000/" HAL9000/g'> dequoted-7.json
$ ~/bin/print-lines.sh -s 155645:1 -p 3350:100 dequoted-7.json
me":"HAL9000","description":" HAL9000Alfa es un pequeño programa que crea un chat conversacional, p

# Attempt to create table:
# Invalid Input Error:
# Malformed JSON in file "dequoted-7.json", at byte 3804 in line 0: unexpected character.
$ ~/bin/print-lines.sh -s 1:1 -p 3750:100 dequoted-7.json
```

What does line 0 mean?? Truncating the file several times, it might be an earlier error on line 162993.

```shell
jq .croissant ./data/json/sample/*.json | \
  sed -e 's/^"//'  -e 's/"$//' -e 's/\\"\\"/""/g' -e 's/\([^\\]\)\\"/\1"/g' -e 's/"\\\\\\"/"/g' -e 's/\\\\""/"/g' -e 's/\([:,]\)\s*"\\[\\]*"/\1""/g' -e 's/manias\(\\*\)"/manias"/g' -e 's/"" HAL9000/" HAL9000/g' -e 's/ture.\(\\*\)"/ture."/g' > dequoted-8.json
  ```

But trying truncated versions of the data, it appears that earlier records are corrupt. But if you truncate the input JSON file, _depending on how much_, the first error reported moves around, often earlier than previously reported errors! I suspect most of these errors are in the `description` fields.

Rather than continue down this rat hole. Let's use `parse-json.py` to look for lines that don't parse correctly and filter them out, then load that output. I'll start with `dequoted-7.json`:

```shell
$ parse-json.py --verbose --input dequoted-7.json --output filtered-7.json
...
Error statistics:
             file:    total    bad        %
  dequoted-7.json:   261479     16   0.006%
output file: filtered-7.json
```

Great! Only 16 out of 261479 or 0.006%. Now let's try to create the table with `filtered-7.json:

```sql
CREATE OR REPLACE TABLE hf_croissant AS
  FROM (
    SELECT *
    FROM read_ndjson_objects('filtered-7.json')
  );
DESCRIBE hf_croissant;
SELECT * FROM hf_croissant LIMIT 2;
SELECT json_valid(json) as valid FROM hf_croissant WHERE valid = 'false';
SELECT json_keys(json) FROM hf_croissant LIMIT 2;
SELECT count(*) FROM hf_croissant;
```

Which prints:

```
┌─────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│ column_name │ column_type │  null   │   key   │ default │  extra  │
│   varchar   │   varchar   │ varchar │ varchar │ varchar │ varchar │
├─────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ json        │ JSON        │ YES     │ NULL    │ NULL    │ NULL    │
└─────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                         json                                                         │
│                                                         json                                                         │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ {"@context":{"@language":"en","@vocab":"https://schema.org/","citeAs":"cr:citeAs","column":"cr:column","conformsTo…  │
│ {"@context":{"@language":"en","@vocab":"https://schema.org/","citeAs":"cr:citeAs","column":"cr:column","conformsTo…  │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
┌─────────┐
│  valid  │
│ boolean │
├─────────┤
│ 0 rows  │
└─────────┘
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                json_keys("json")                                                 │
│                                                    varchar[]                                                     │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [@context, @type, distribution, recordSet, conformsTo, name, description, alternateName, creator, keywords, url] │
│ [@context, @type, distribution, recordSet, conformsTo, name, description, alternateName, creator, keywords, url] │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│    261495    │
└──────────────┘
```

Finally! Now, let's extract the fields we want into a new table. First, here is a query to grab a set of fields as needed:

```sql
WITH metadata AS (
  SELECT  json->>'$.name'            AS name,
          json->>'$.description'     AS description,
          json->>'$.url'             AS url,
          json->>'$.license'         AS license,
          json->>'$.keywords'        AS keywords,
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

Now create a metadata table:

```sql
CREATE OR REPLACE TABLE hf_metadata AS
  WITH metadata AS (
    SELECT  json->>'$.name'            AS name,
            json->>'$.description'     AS description,
            json->>'$.url'             AS url,
            json->>'$.license'         AS license,
            json->>'$.keywords'        AS keywords,
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
│ keywords     │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
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

So, only 60K out of 261K records (23%) have a license! Not great. 

> **NOTE:** In preparing the condensed `README.md` from these notes, I realized that I should have used `json->>'$.keywords[*]' AS keywords,`, so that `keywords` has type `json[]` instead of `json`. The `README` follows that path, which greatly simplifies analysis of the keywords below. Here, I left these notes as they were originally.

Let's see what those licenses are. First, I need to tell `duckdb` to not truncate the output (I'll only need ~75 lines):

```sql
D .maxrows 1234
```

```sql
SELECT license, count(license) AS count
FROM hf_metadata GROUP BY license ORDER BY count DESC NULLS FIRST;
```
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

(There are no `NULLS`, but I put that in there as a "reminder"...)

Let's look at the `languages` and `keywords`:

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

Okay, so _every_ dataset is English!! This is not what I was hoping for. What about the keywords?

```sql
SELECT keywords FROM hf_metadata LIMIT 10;
```
```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                       keywords                                                       │
│                                                       varchar                                                        │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ ["apache-2.0","100K - 1M","parquet","Text","Datasets","pandas","Croissant","Polars","🇺🇸 Region: US"]                 │
│ ["openrail","< 1K","soundfolder","Audio","Datasets","Croissant","🇺🇸 Region: US"]                                     │
│ ["mit","10K - 100K","parquet","Text","Datasets","pandas","Croissant","Polars","🇺🇸 Region: US"]                       │
│ ["openrail","< 1K","soundfolder","Audio","Datasets","Croissant","🇺🇸 Region: US"]                                     │
│ ["mit","100K - 1M","csv","Text","Datasets","pandas","Croissant","Polars","🇺🇸 Region: US"]                            │
│ ["question-answering","text-generation","English","apache-2.0","1M - 10M","parquet","Text","Datasets","Dask","Croi…  │
│ ["question-answering","Russian","gpl-3.0","< 1K","csv","Text","Datasets","pandas","Croissant","Polars","🇺🇸 Region: …  │
│ ["mit","< 1K","csv","Tabular","Datasets","pandas","Croissant","Polars","🇺🇸 Region: US"]                              │
│ ["mit","10K - 100K","csv","Text","Datasets","pandas","Croissant","Polars","🇺🇸 Region: US"]                           │
│ ["mit","< 1K","csv","Tabular","Datasets","pandas","Croissant","Polars","🇺🇸 Region: US"]                              │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
```

select regexp_replace('["foo", "bar"]', '[\[\]"]+', '');
select replace(replace(replace('["foo", "bar"]', '[', ''), ']', ''), '"', '');

```sql
WITH keywords AS (
  SELECT unnest(regexp_split_to_array(
    replace(replace(replace(keywords, '[', ''), ']', ''), '"', ''), '\s*,\s*')) AS keyword
  FROM hf_metadata
) 
SELECT keyword, count(keyword) AS count
FROM keywords GROUP BY keyword ORDER BY count DESC NULLS FIRST LIMIT 100;
```
```
┌─────────────────────────────┬───────┐
│           keyword           │ count │
│           varchar           │ int64 │
├─────────────────────────────┼───────┤
│ 🇺🇸 Region: US               │ 60087 │
│ Croissant                   │ 53547 │
│ Datasets                    │ 53543 │
│ Text                        │ 43424 │
│ Polars                      │ 41101 │
│ pandas                      │ 33573 │
│ < 1K                        │ 20501 │
│ apache-2.0                  │ 19824 │
│ parquet                     │ 18957 │
│ mit                         │ 16921 │
│ English                     │ 14664 │
│ json                        │ 13424 │
│ 1K - 10K                    │ 13192 │
│ 10K - 100K                  │ 10421 │
│ csv                         │  9680 │
│ Tabular                     │  8687 │
│ Dask                        │  8477 │
│ Image                       │  8409 │
│ text-generation             │  6406 │
│ 100K - 1M                   │  5722 │
│ Audio                       │  5557 │
│ openrail                    │  4568 │
│ soundfolder                 │  4388 │
│ question-answering          │  3850 │
│ text-classification         │  3830 │
│ imagefolder                 │  3565 │
│ cc-by-4.0                   │  3560 │
│ crowdsourced                │  3219 │
│ monolingual                 │  2689 │
│ 1M - 10M                    │  2660 │
│ Video                       │  2461 │
│ robotics                    │  2299 │
│ Time-series                 │  2269 │
│ other                       │  2202 │
│ LeRobot                     │  2201 │
│ original                    │  2063 │
│ unknown                     │  2013 │
│ text                        │  1879 │
│ cc-by-sa-4.0                │  1595 │
│ Chinese                     │  1546 │
│ summarization               │  1486 │
│ found                       │  1315 │
│ text2text-generation        │  1265 │
│ cc-by-nc-4.0                │  1249 │
│ image-to-text               │  1229 │
│ art                         │  1224 │
│ text-to-image               │  1223 │
│ arxiv:2204.07705            │  1176 │
│ arxiv:2407.00066            │  1173 │
│ feature-extraction          │  1160 │
│ Synthetic                   │  1124 │
│ French                      │  1089 │
│ text-retrieval              │  1082 │
│ expert-generated            │  1077 │
│ cc-by-nc-sa-4.0             │  1072 │
│ token-classification        │  1069 │
│ multilingual                │  1061 │
│ cc0-1.0                     │  1034 │
│ 10M - 100M                  │  1014 │
│ tutorial                    │  1006 │
│ translation                 │   981 │
│ Russian                     │   976 │
│ code                        │   950 │
│ Spanish                     │   948 │
│ Japanese                    │   932 │
│ language-modeling           │   841 │
│ cc                          │   838 │
│ 1K<n<10K                    │   838 │
│ German                      │   835 │
│ sentence-similarity         │   834 │
│ image-classification        │   811 │
│ medical                     │   735 │
│ so100                       │   703 │
│ Korean                      │   662 │
│ Arabic                      │   658 │
│ multi-class-classification  │   635 │
│ infinite-dataset-hub        │   606 │
│ extractive-qa               │   592 │
│ Portuguese                  │   580 │
│ topic-classification        │   578 │
│ multi-label-classification  │   577 │
│ biology                     │   560 │
│ Italian                     │   557 │
│ named-entity-recognition    │   556 │
│ cc-by-nc-nd-4.0             │   531 │
│ gpl-3.0                     │   524 │
│ odc-by                      │   518 │
│ machine-generated           │   502 │
│ object-detection            │   493 │
│ legal                       │   492 │
│ text-scoring                │   487 │
│ Turkish                     │   483 │
│ sentiment-analysis          │   475 │
│ Hindi                       │   462 │
│ cc-by-sa-3.0                │   462 │
│ news-articles-summarization │   461 │
│ table-question-answering    │   452 │
│ visual-question-answering   │   448 │
│ webdataset                  │   431 │
│ WebDataset                  │   430 │
├─────────────────────────────┴───────┤
│ 100 rows                  2 columns │
└─────────────────────────────────────┘
```
So there are other languages present! 

> **NOTES:**
> 1. I tried `regexp_replace(keywords, '[\[\]"]+', '')`, but it appears to only replace the first match, not all of them, and there doesn't appear to be a function that will replace all occurrences! Hence I used the three `replace` functions, which is an ugly hack.
> 2. The regex split assumes that no keyword contains a `,`, which is hopefully a good assumption (or at least, good "enough"...).
> 3. Look at the number of references to a few arXiv papers!

Let's see which ones we can find. First, for convenience, let's create a table of keywords. We'll also convert them to lower case:

```sql
CREATE OR REPLACE TABLE keywords AS
  WITH keywords AS (
    SELECT unnest(regexp_split_to_array(
      replace(replace(replace(keywords, '[', ''), ']', ''), '"', ''), '\s*,\s*')) AS keyword
    FROM hf_metadata
  ) 
  SELECT lower(keyword) AS lower_keyword, count() AS count
  FROM keywords GROUP BY lower_keyword;
DESCRIBE keywords;
SELECT count() FROM keywords;
```
```
┌───────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│  column_name  │ column_type │  null   │   key   │ default │  extra  │
│    varchar    │   varchar   │ varchar │ varchar │ varchar │ varchar │
├───────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ lower_keyword │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ count         │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
└───────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│    22214     │
└──────────────┘
```

### Languages

Let's save to a file to search for language entries:

```sql
COPY (SELECT lower_keyword FROM keywords) TO 'keywords.csv';
```

Now, we need a list of the world's languages in a convenient format. Here are two JSON-formatted lists: [one](https://gist.github.com/jrnk/8eb57b065ea0b098d571), which claims to be an ISO list, and [two](https://gist.github.com/rglover/23d9d10d788c87e7fc5f5d7d8629633f). Even though the second has more entries, ~240 vs. ~180, let's use the ISO list, saved to 

```sql
CREATE OR REPLACE TABLE languages AS
  SELECT *
  FROM read_json('ISO-639-1-language.json');
DESCRIBE languages;
SELECT count() FROM languages;
SELECT * FROM languages LIMIT 10;
```
```
┌─────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│ column_name │ column_type │  null   │   key   │ default │  extra  │
│   varchar   │   varchar   │ varchar │ varchar │ varchar │ varchar │
├─────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ code        │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ name        │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
└─────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│     184      │
└──────────────┘
┌─────────┬───────────┐
│  code   │   name    │
│ varchar │  varchar  │
├─────────┼───────────┤
│ aa      │ Afar      │
│ ab      │ Abkhazian │
│ ae      │ Avestan   │
│ af      │ Afrikaans │
│ ak      │ Akan      │
│ am      │ Amharic   │
│ an      │ Aragonese │
│ ar      │ Arabic    │
│ as      │ Assamese  │
│ av      │ Avaric    │
├─────────┴───────────┤
│ 10 rows   2 columns │
└─────────────────────┘
```

```sql
WITH langs AS (
  SELECT code, lower(name) AS lower_name
  FROM   languages
)
SELECT   keywords.lower_keyword, keywords.count, langs.code, langs.lower_name 
FROM     keywords
JOIN     langs
ON       keywords.lower_keyword = langs.code
ORDER BY keywords.count DESC;
```

```
┌───────────────┬───────┬─────────┬──────────────────────────────────┐
│ lower_keyword │ count │  code   │            lower_name            │
│    varchar    │ int64 │ varchar │             varchar              │
├───────────────┼───────┼─────────┼──────────────────────────────────┤
│ cv            │    13 │ cv      │ chuvash                          │
│ ga            │    12 │ ga      │ irish                            │
│ en            │    11 │ en      │ english                          │
│ ko            │    11 │ ko      │ korean                           │
│ ml            │     9 │ ml      │ malayalam                        │
│ it            │     8 │ it      │ italian                          │
│ mt            │     8 │ mt      │ maltese                          │
│ ru            │     7 │ ru      │ russian                          │
│ tt            │     7 │ tt      │ tatar                            │
│ ho            │     6 │ ho      │ hiri motu                        │
│ tw            │     6 │ tw      │ twi                              │
│ wa            │     6 │ wa      │ walloon                          │
│ cs            │     5 │ cs      │ czech                            │
│ tr            │     5 │ tr      │ turkish                          │
│ uz            │     4 │ uz      │ uzbek                            │
│ ha            │     4 │ ha      │ hausa                            │
│ fr            │     4 │ fr      │ french                           │
│ ja            │     4 │ ja      │ japanese                         │
│ ik            │     4 │ ik      │ inupiaq                          │
│ uk            │     4 │ uk      │ ukrainian                        │
│ ak            │     3 │ ak      │ akan                             │
│ zh            │     3 │ zh      │ chinese                          │
│ eu            │     3 │ eu      │ basque                           │
│ pt            │     3 │ pt      │ portuguese                       │
│ sa            │     3 │ sa      │ sanskrit                         │
│ es            │     3 │ es      │ spanish; castilian               │
│ de            │     3 │ de      │ german                           │
│ ar            │     3 │ ar      │ arabic                           │
│ hr            │     3 │ hr      │ croatian                         │
│ as            │     2 │ as      │ assamese                         │
│ hi            │     2 │ hi      │ hindi                            │
│ eo            │     2 │ eo      │ esperanto                        │
│ fa            │     2 │ fa      │ persian                          │
│ fi            │     2 │ fi      │ finnish                          │
│ hu            │     2 │ hu      │ hungarian                        │
│ to            │     2 │ to      │ tonga (tonga islands)            │
│ no            │     2 │ no      │ norwegian                        │
│ kg            │     1 │ kg      │ kongo                            │
│ rm            │     1 │ rm      │ romansh                          │
│ kr            │     1 │ kr      │ kanuri                           │
│ na            │     1 │ na      │ nauru                            │
│ mk            │     1 │ mk      │ macedonian                       │
│ tg            │     1 │ tg      │ tajik                            │
│ sq            │     1 │ sq      │ albanian                         │
│ lv            │     1 │ lv      │ latvian                          │
│ li            │     1 │ li      │ limburgan; limburger; limburgish │
│ el            │     1 │ el      │ greek, modern (1453-)            │
├───────────────┴───────┴─────────┴──────────────────────────────────┤
│ 47 rows                                                  4 columns │
└────────────────────────────────────────────────────────────────────┘
```

Searching for some of the languages seen in the keywords:

```sql
SELECT lower_keyword, count
FROM keywords WHERE lower_keyword IN (
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

Let's write a few language datasets:

```sql
COPY (
  SELECT name, description, license, url, creator_name, creator_url
  FROM hf_metadata
  WHERE lower(keywords) LIKE '%english%'
) TO 'english.json';
COPY (
  SELECT name, description, license, url, creator_name, creator_url
  FROM hf_metadata
  WHERE lower(keywords) LIKE '%french%'
) TO 'french.json';
COPY (
  SELECT name, description, license, url, creator_name, creator_url
  FROM hf_metadata
  WHERE lower(keywords) LIKE '%spanish%'
) TO 'spanish.json';
COPY (
  SELECT name, description, license, url, creator_name, creator_url
  FROM hf_metadata
  WHERE lower(keywords) LIKE '%german%'
) TO 'german.json';
COPY (
  SELECT name, description, license, url, creator_name, creator_url
  FROM hf_metadata
  WHERE lower(keywords) LIKE '%arabic%'
) TO 'arabic.json';
COPY (
  SELECT name, description, license, url, creator_name, creator_url
  FROM hf_metadata
  WHERE lower(keywords) LIKE '%vietnamese%'
) TO 'vietnamese.json';
COPY (
  SELECT name, description, license, url, creator_name, creator_url
  FROM hf_metadata
  WHERE lower(keywords) LIKE '%japanese%'
) TO 'japanese.json';
COPY (
  SELECT name, description, license, url, creator_name, creator_url
  FROM hf_metadata
  WHERE lower(keywords) LIKE '%korean%'
) TO 'korean.json';
COPY (
  SELECT name, description, license, url, creator_name, creator_url
  FROM hf_metadata
  WHERE lower(keywords) LIKE '%hindi%'
) TO 'hindi.json';
COPY (
  SELECT name, description, license, url, creator_name, creator_url
  FROM hf_metadata
  WHERE lower(keywords) LIKE '%portuguese%'
) TO 'portuguese.json';
COPY (
  SELECT name, description, license, url, creator_name, creator_url
  FROM hf_metadata
  WHERE lower(keywords) LIKE '%turkish%'
) TO 'turkish.json';
```

```shell
for lang in english chinese # french russian spanish japanese german korean arabic portuguese italian turkish hindi vietnamese 
do
  echo "language: $lang"
  cat <<EOF > temp-query.sql
  COPY (
    SELECT name, description, license, url, creator_name, creator_url
    FROM hf_metadata
    WHERE lower(keywords) LIKE '%${lang}%'
  ) TO '${lang}.json';
EOF
  duckdb -f temp-query.sql
  wc $lang.json
  head -5 $lang.json
  echo
done
```


### ArXiv References?

```sql
SELECT lower_keyword, count FROM keywords WHERE lower_keyword LIKE 'arxiv:%' ORDER BY count DESC LIMIT 10;
```
```
┌──────────────────┬───────┐
│  lower_keyword   │ count │
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
│ arxiv:2501.19393 │    21 │
│ arxiv:2203.02155 │    21 │
├──────────────────┴───────┤
│ 10 rows        2 columns │
└──────────────────────────┘
```

## Saving to JSON files.

Here is an example of writing a table to JSON:

```sql
COPY (SELECT * FROM hf_metadata) TO 'hf_metadata.json';
```

## Appendix

Miscellaneous notes while working that I moved out of the way, once finished...

Experiments with `sed` cleanup:

```shell
echo '\"\\\"UMAP' |sed -e 's/\\"\\[\\]*"/""/g'
echo ':\"\\\""UMAP' |sed  -e 's/\([^\\]\)\\"/\1"/g' -e 's/\\\\""*/\\"/g'

sed -e 's/^"//'  -e 's/"$//' -e 's/\([^\\]\)\\"/\1"/g' -e 's/\\"[ ]*\\[\\]*"/""/g' -e 's/\\\\""/\\"/g'  -e 's/\([:,]\)\s*"\\[\\]*"/\1""/g'  bad.json
sed -e 's/\\" *\\"/""/g' -e 's/\([^\\]\)\\"/\1"/g' bad.json
sed -e 's/\\" *\\"/""/g' -e 's/\([^\\]\)\\"/\1"/g' -e 's/\\[\\]*"\([^"]\)/\\"\1/g' bad.json
sed -e 's/\\"\\"/""/g' -e 's/\([^\\]\)\\"/\1"/g' -e 's/\\\\"/\"/g' -e 's/\\\\""*/\"/g' bad.json
sed -e 's/^"//'  -e 's/"$//' -e 's/\\"\\"/""/g' -e 's/\([^\\]\)\\"/\1"/g' -e 's/"\\\\\\"/"/g' -e 's/\\\\""/"/g' -e 's/\([:,]\)\s*"\\[\\]*"/\1""/g' bad.json
e 's/"\\\\\\"/"/g' -e 's/\([:,]\)\s*"\\[\\]*"/\1""/g' 

sed -e 's/^"//'  -e 's/"$//' -e 's/\\"\(\\*\)\\"/""/g' -e 's/\([^\\]\)\\"/\1"/g' -e 's/\\\\""/"/g' bad.json
sed -e 's/^"//'  -e 's/"$//' -e 's/\\"\\"/""/g' -e 's/\([^\\]\)\\"/\1"/g' -e 's/"\\\\\\"/"/g' -e 's/\\\\""/"/g' -e 's/\([:,]\)\s*"\\[\\]*"/\1""/g' -e 's/manias\(\\*\)"/manias"/g' bad.json

sed -e 's/^"//'  -e 's/"$//' -e 's/\\"\\"/""/g' -e 's/\([^\\]\)\\"/\1"/g' -e 's/"\\\\\\"/"/g' -e 's/\\\\""/"/g' -e 's/\([:,]\)\s*"\\\(\\\)*"/\1""/g' -e 's/manias\(\\\)*"' bad.json
```

For reference, here are some other interesting queries:

```sql
select json from hf_croissant limit 2;
select json_keys(json) from hf_croissant limit 2;
select unnest(json_keys(json)) AS keys from hf_croissant limit 20;

SELECT *
FROM read_json('dequoted-3.json',
           columns = {name: 'VARCHAR',
                      description: 'VARCHAR',
                      license: 'VARCHAR'}) LIMIT 100;
```


## Writing JSON

See https://duckdb.org/docs/stable/data/json/writing_json.

For example:
```sql
COPY (SELECT * FROM todos) TO 'todos.json';
```

