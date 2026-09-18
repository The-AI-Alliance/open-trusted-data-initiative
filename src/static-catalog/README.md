# README on Processing Hugging Face Metadata to Build the "Static" Catalog

* Dean Wampler, May 11, 2025
* Updates, June 9, 2025, October 24, 2025

## Introduction

This README describes how the "static" catalog is built. The catalog currently shown on the OTDI website is called "static" because a snapshot of metadata, captured from Hugging Face, is processed into JSON files for loading into the catalog views by keywords. A "dynamic" catalog would be one where you have more flexible search of very recent metadata. The metadata used for the static catalog is captured continuously, but the catalog pages are only updated monthly, on average. This is a temporary implementation until the dynamic catalog is fully implemented and available.

> [!NOTE]
> The following content is a condensed version of the long `duckdb-notes.md` file, plus other notes, where Dean experimented with DuckDB, Spark, and other tools. This file covers the commands that worked. Also, this file has been updated a few times since the initial draft as the processing steps have been refined and automated. To see the notes for the first "V0.0.1" version of the static catalog, see this file as of git tag `V0.3.2-static-catalog-0.0.1`.
>
> Update October 31, 2025: See [`license-notes.md`](license-notes.md) for details on making sense of how licenses are specified, and finding permissive licenses in datasets where the license was improperly specified.

## Introduction

We start with the metadata files created by Joe Olson's nightly job that queries Hugging Face for Croissant metadata. The format of those files is Parquet with a flat schema, with one column containing the entire JSON document for the metadata. Parsing that metadata proved difficult, because of deep "escape quoting". It was necessary to put together a set of tools to extract this metadata and load it into [DuckDB](https://duckdb.org) for further analysis and processing.

## Rebuilding the Catalog

Ask Dean Wampler for help, if needed.

Steps:

* Acquire a snapshot of the parquet files and put them in the directory `data/parquet/<date>` (under this directory, `static-catalog`), where date is the date the snapshot was captured, in the form `YYYY-MM-DD`.
* Edit the `Makefile` and set `PARQUET_SNAPSHOT_TIMESTAMP` to match that date string. (Or just invoke the `make` commands below starting with `PARQUET_SNAPSHOT_TIMESTAMP=YYYY-MM-DD make targets` for the actual date.) Note that by default, the current date will be used for temporary files created during the subsequent steps, which will likely be later than the parquet files capture date.
* Update `./data/reference/keyword-categories.json` with any changes to the hierarchy of categories and keywords you want to make.
* Run `make catalog`, which does the following:
  * Runs `./src/catalog/parquet-to-json.py`, which reads the parquet files in `./data/parquet/<date>`, extracts the `croissant` column as a string, performs _unescapes_ (e.g., `\"` to `"`, etc.), then writes JSON files to `./data/json/temp/YYYY-MM-DD`, where `YYYY-MM-DD` is today's date by default. (You can override this with the environment variable `TIMESTAMP`.)
  * Runs `./src/catalog/load-into-duckdb.py`, which reads the JSON in `./data/json/temp/YYYY-MM-DD` into `duckdb` tables.
  * Runs `./src/catalog/write-category-files.py` to read the `temp` JSON output and write one markdown file _for each topic_ under `./markdown/processed/YYYY-MM-DD`, and one JavaScript and one JSON file _for each topic_ under `./data/json/processed/YYYY-MM-DD`.
  * Runs `./src/catalog/copy-files-to-docs.sh` to copy the files created over to the correct locations in `docs`.
* Commit the changes and push upstream!

You can run all the scripts discussed separately; use `--help` to see options.

> [!NOTE]
>
> * Run all the commands shown below in the `static-catalog` directory, e.g., when running `make catalog`.
> * `./src/catalog/parquet-to-json.py` requires `pandas`.
> * `./src/catalog/write-category-files.py` requires DuckDB to be installed (see [Using DuckDB](#using-duckdb)) _and_ it requires a database file named `./croissant.duckdb`. This file is very large, so we don't version it in the git repo. Talk to Dean Wampler or Joe Olson to get a copy of this file and put it in this directory.
> * The markdown files copied to `../docs` correspond to _collections_ defined in `../docs/_config.yaml`; there is a subfolder for each collection, currently `_language`, `_domain`, and `_modality` (the `_` is required)
> * The JavaScript files are copied to `../docs/files/data/catalog`. They contain the static data, defined as JS arrays of objects.
> * The markdown and JSON directory hierarchies are _different_. The markdown files need to be flat, only _collection_ subfolders (currently `_language`, `_domain`, and `_modality`). We tried making hierarchical directories here, but this isn't supported by Jekyll/Liquid. In contrast, the JavaScript files written to `../docs/files/data/catalog` are hierarchical, because they use our own convention and are handled appropriately by the JavaScript code that loads them, `../docs/_includes/data_table_template.html`.
> * When numbers of rows are quoted below, e.g., "123,456 rows in table foo", those numbers are from a June 2025 run of this process. As the number of Hugging Face datasets keeps growing, all such numbers will be larger in more recent runs.

The rest of this README covers more details on how these processing steps work. It doesn't cover creating or editing `./data/reference/keyword-categories.json`, which was created manually!

## Initial Setup

These steps are necessary before the `make catalog` automation can work.

### Python Environment

We'll use [`uv`](https://docs.astral.sh/uv/) to manage the Python environment, so `uv` commands will be shown. However, you can manage these dependencies any way you prefer. 

If you don't want to use `uv`:
* Install the dependencies seen in `./pyproject.toml` using `pip` or whatever tool you prefer. However, you can omit `jupyterlab`, `ipykernel`, and `bokeh`. They are _not_ required for generating the catalog data. They are used for an ad-hoc analysis of the metadata. See `analysis/README.md` for information. 
* Edit the `Makefile` to define `UV_RUN` to be "".

### Get the Parquet Data

Get a copy of the Parquet files with the Croissant metadata and use it as follows. Let's assume those Parquet files are in the current directory:

```shell
ymd=YYYY-MM-DD  # for today's date
mkdir -p data/parquet/$ymd
mv *.parquet data/parquet/$ymd
```

### Install DuckDB

We use the [DuckDB](https://duckdb.org) CLI tools.

Use this command to install the tools, including the `duckdb` CLI:

```shell
curl https://install.duckdb.org | sh
```

See the [documentation](https://duckdb.org/docs/stable/) for more details.

### Using the JSON Support in the `duckdb` CLI

The JSON processing functions are [documented here](https://duckdb.org/docs/stable/data/json/json_functions.html).

Start the `duckdb` CLI so you can install the `json` module. We specify a persistent database `./croissant.duckdb`. Otherwise, everything is just in memory and lost when you exit the CLI:

```shell
duckdb ./croissant.duckdb
```

> ![WARNING]
> The `croissant.duckdb` file can easily grow to GBs in size! For this reason, we are not currently storing it in the git repo.

At the `D` prompt (which will often be omitted in what follows, except when showing output...) type the following:

```
install 'json';
load 'json';
```

These commands don't need to be repeated in subsequent sessions.

Use `.quit` to exit `duckdb`.

## Parsing Parquet to JSON Files

The `make catalog` build first builds `make-clean`, which deletes directories where new files will be created, then runs `make catalog-data-prep`. This target invokes `./src/catalog/parquet-to-json.py`, which uses `pandas` to read the parquet files in `./data/parquet/<date>`, where `<date>` is the snapshot capture date in the format `YYYY-MM-DD`.

The input parquet format includes two columns we care about, `response_reason` and `croissant`. The former should have the value `OK`, meaning the metadata was successfully retrieved in Croissant format for the corresponding dataset. We filter out all records without this value, reducing the input from about 413,000 datasets to 329,000.

The `croissant` column contains giant strings of quoted JSON, which means lots of _escapes_ like this:

```json
"{\"@context\":{\"@language\":\"en\",...}}"
```

The rest of `./src/catalog/parquet-to-json.py` _unescapes_ the JSON string and writes it to one large file (>3GB), `./data/json/YYYY-MM-DD/croissant.json`, where `YYYY-MM-DD` is today's date.

## Load into DuckDB

Next, the `make catalog` target makes the target `catalog-duckdb-load` to load the temporary JSON files into [DuckDB](https://duckdb.org), which has good support for JSON and it allows us to do useful joins, filtering, etc.

Specifically, this `make` target runs the script `./src/catalog/load-into-duckdb.py` to read the JSON in `./data/json/temp/YYYY-MM-DD` and to create the following `duckdb` tables.

```sql
CREATE OR REPLACE TABLE hf_croissant AS FROM (
    SELECT  name,
            description,
            url                        AS dataset_url,
            license,
            keywords,
            "@context"->>'$.@language' AS language,
            creator->>'$.name'         AS creator_name,
            creator->>'$.url'          AS creator_url,
    FROM    read_json('./data/json/temp/YYYY-MM-DD')
);
```

The `foo->>bar` syntax is used to extract elements from nested JSON objects.

Two other _reference_ files are loaded as tables:

```sql
CREATE OR REPLACE TABLE hf_licenses AS
    SELECT * FROM read_json('./data/reference/license-id-name-mapping.json');
```

In the original parquet and the derived JSON data, the license field is specified as a [choosealicense.com](https://choosealicense.com) URL. The `hf_licenses` table maps between these URLs and license names. For example, the first line in the JSON file is this:

```json
{"id":"0bsd", "name":"BSD Zero Clause License", "url":"https://choosealicense.com/licenses/0bsd/"}
```

There are 47 rows.

Similarly, it's useful to have a reference table that maps ISO ids for languages to their names:

```sql
CREATE OR REPLACE TABLE iso_languages AS
  SELECT code, lower(name) AS name
  FROM read_json('./data/reference/ISO-639-1-language.json');
```

For example, the first entry is this:

```json
{ "code": "aa", "name": "Afar" },
```

In some cases, several names are given:

```json
{
  "code": "cu",
  "name": "Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic"
},
```

From `hf_croissant` and `hf_licenses`, we create `hf_metadata`:

```sql
CREATE OR REPLACE TABLE hf_metadata AS
    SELECT
        hfc.name          AS name,
        hfc.description   AS description,
        lic.name          AS license,
        lic.id            AS license_id,
        hfc.license       AS license_url,
        hfc.language      AS language,
        hfc.dataset_url   AS dataset_url,
        hfc.keywords      AS keywords,
        hfc.creator_name  AS creator_name,
        hfc.creator_url   AS creator_url
    FROM hf_croissant hfc
    JOIN hf_licenses  lic
    ON hfc.license = lic.url;
```

This table has about 60,000 rows, whereas `hf_croissant` has 329,000; only 20% of the rows remain!

### Invalid Licenses

The reason for this radical reduction is the fact that most datasets don't define a license value at all and many that do use an invalid choosealicense.com URL for the license field. To see this, let's use a variation of the previous query with a `LEFT JOIN` to find the undefined or invalid licenses:

```sql
CREATE OR REPLACE TABLE hf_metadata_with_all_licenses AS
    SELECT
        hfc.name          AS name,
        hfc.description   AS description,
        lic.name          AS license,
        lic.id            AS license_id,
        hfc.license       AS license_url,
        hfc.language      AS language,
        hfc.dataset_url   AS dataset_url,
        hfc.keywords      AS keywords,
        hfc.creator_name  AS creator_name,
        hfc.creator_url   AS creator_url
    FROM hf_croissant hfc
    LEFT JOIN hf_licenses  lic
    ON hfc.license = lic.url;
```

The following query shows that there are 252,000 datasets with no license and many others where there is a URL, but no `license_id`:

```sql
SELECT license_id, license_url, count() AS count
FROM hf_metadata_with_all_licenses
GROUP BY license_id,license_url
ORDER BY count DESC;
```

The cases where a URL is shown, but the `license_id` is `NULL` are examples that use invalid URLs for choosealicense.com. Reading the URLs, many look like attempts to specify a legitimate, known license, but the URLs are 404s. This query counts all those cases:

```sql
SELECT count() AS count
FROM hf_metadata_with_all_licenses
WHERE license_id IS NULL AND license_url NOT NULL;
```

About 17,600 datasets have this issue!

We discard all the datasets with no license or an improperly-defined license, although we intend to revisit that latter almost 18,000 records at some later time.

Finally, we create `hf_expanded_metadata`, which expands the array of keywords into separate records, one per keyword:

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
    description,
    keywords
  FROM hf_metadata
);
```

This table has 677,000 rows, suggesting on average there are 11 keywords per dataset. Note that the keywords are converted to lower case.

This table is used subsequently to generate the JavaScript and Markdown files required for the static catalog rendering in the website for greater uniformity.

## Creating JavaScript and Markdown Files for the Website

Next, `make catalog` builds the `make-build` target that _builds_ the JavaScript and Markdown files required. This target runs the script `./src/catalog/write-category-files.py` to do this.

The script reads the categories, possible subcategories, and topics (corresponding to keywords) from `./data/reference/keyword-categories.json`. It generates Markdown files in three directories, `_language`, `_domain`, `_modality` in `./markdown/processed/YYYY-MM-DD/`. The leading `_` is a convention used by Jekyll. These files will be copied to the root directory of the website, `docs`. Each file, such as `.../_language/language_asia_korean.markdown` contains metadata data in a YAML block and content to display for that language, e.g.,:

```markdown
---
name: Korean
tag: korean
context: ""
cleaned_tag: korean
parent_tag: asia
parent_title: Asian Languages
grand_parent_tag: language
grand_parent_title: Languages
alt_tags:
---

{% include data-table-template.html
  keyword="korean"
  cleaned_keyword="korean"
  title="Korean"
  context=""
  ancestor_path="language/asia"
  parent_title = "Asian Languages"
  grand_parent_title = "Languages"
  alt_keywords=""
%}
```

The template file `data-table-template.html` will be used to create the table shown for Korean. The data for the table comes from a separate JavaScript file.

The JavaScript files are in `./data/json/processed/YYYY-MM-DD`, e.g., a JSON file, `.../language/asia/korean.json`, and a corresponding JavaScript file, `.../language/asia/korean.js`, which just wraps the JSON in a variable definition for inclusion in the relevant catalog page. (TODO: There are alternative ways to load the JSON directly that we should pursue, rather than having separate, nearly-identical JSON and JavaScript files.) There are directories for `language`, `domain`, and `modality`.

```javascript
const data_for_language_asia_korean =
[
  {"name":"MAPS","keyword":"korean","license":"MIT License","license_url":"https://choosealicense.com/licenses/mit/","language":"en","dataset_url":"https://huggingface.co/datasets/Fujitsu-FRE/MAPS","creator_name":"Fujitsu Research of Europe","creator_url":"https://huggingface.co/Fujitsu-FRE","description":"\n\t\n\t\t\n\t\tDataset Card for Multilingual Benchmark for Global Agent Performance and Security\n\t\n\nThis is the first Multilingual Agentic AI Benchmark for evaluating agentic AI systems across different languages and diverse tasks. Benchmark enables systematic analysis of how agents perform under multilingual conditions. To balance performance and safety evaluation, our benchmark comprises 805 tasks: 405 from performance-oriented datasets (GAIA, SWE-bench, MATH) and 400 from the Agent Security… See the full description on the dataset page: https://huggingface.co/datasets/Fujitsu-FRE/MAPS.","first_N":5,"first_N_keywords":["text-generation","question-answering","Arabic","English","Japanese"],"keywords_longer_than_N":true},
  ...
  {"name":"BH_test_ko","keyword":"korean","license":"Creative Commons Attribution Share Alike 4.0 International","license_url":"https://choosealicense.com/licenses/cc-by-sa-4.0/","language":"en","dataset_url":"https://huggingface.co/datasets/EunsuKim/BH_test_ko","creator_name":"Eunsu Kim","creator_url":"https://huggingface.co/EunsuKim","description":"EunsuKim/BH_test_ko dataset hosted on Hugging Face and contributed by the HF Datasets community","first_N":5,"first_N_keywords":["text-generation","Korean","cc-by-sa-4.0","10K - 100K","csv"],"keywords_longer_than_N":true}
]
;
```

## Copy the JavaScript and Markdown Files to the Website

Finally, `make catalog` builds the `catalog-install` target, which runs the `./src/catalog/copy-files-to-docs.sh` `zsh` script.

This script copies the contents of `./data/json/processed/YYYY-MM-DD` to `docs/files/data/catalog` and the contents of `./markdown/processed/YYYY-MM-DD` to `docs`.

## Conclusions

You are now ready to commit and push the changes to the website, after local sanity checking, of course.
