#!/usr/bin/env python

import argparse, os, pathlib, subprocess, sys
from common import (
    is_process_running, list_to_str, 
    make_directories, today,
    info, warning, error, beep
)

parser = argparse.ArgumentParser(
                    prog='load-into-duckdb',
                    description='Loads JSON data into duckdb tables.',
                    epilog='')
parser.add_argument('-v', '--verbose',
                    help="Verbosity level for output. Higher numbers result in more details. E.g., use '2' to see the queries that are executed.",
                    type=int,
                    default=0) 
parser.add_argument('-i', '--input',
                    required=True,
                    help=f"Input JSON files location.")
parser.add_argument('--db-file',
                    required=True,
                    help=f"The duckdb database file.")
parser.add_argument('--licenses',
                    required=True,
                    help=f"A reference file with license metadata.")
parser.add_argument('--iso-langs',
                    required=True,
                    help=f"A reference file with ISO codes for languages.")
args = parser.parse_args(sys.argv[1:])

if args.verbose > 0:
    print("load-into-duckdb.py:")
    print(f"  input:    {args.input}")
    print(f"  DB file:  {args.db_file}")
    print(f"  licenses: {args.licenses}")

if is_process_running('duckdb'):
    error("It appears that 'duckdb' is already running. Please stop it then rerun this script.")

info("\n**** NOTE: This program may run for several minutes! (Invoke with '--verbose 1' to see progress.) ****\n")


start = f"duckdb {args.db_file}"

hf_croissant_create_query = f"""
CREATE OR REPLACE TABLE hf_croissant AS FROM (
    SELECT  name,
            description,
            url                        AS dataset_url,
            license,
            keywords,
            "@context"->>'$.@language' AS language,
            creator->>'$.name'         AS creator_name,
            creator->>'$.url'          AS creator_url,
    FROM    read_json('{args.input}')
);
"""

hf_licenses_create_query = f"""
CREATE OR REPLACE TABLE hf_licenses AS
    SELECT * FROM read_json('{args.licenses}');
"""

# This query also removes all null licenses!
hf_metadata_create_query = f"""
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
"""

iso_languages_create_query = f"""
CREATE OR REPLACE TABLE iso_languages AS
  SELECT code, lower(name) AS name
  FROM read_json('{args.iso_langs}');
"""

hf_expanded_metadata_create_query = f"""
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
"""

queries = {
    "hf_croissant": hf_croissant_create_query,
    "hf_licenses": hf_licenses_create_query, 
    "hf_metadata": hf_metadata_create_query,
    "iso_languages": iso_languages_create_query,
    "hf_expanded_metadata": hf_expanded_metadata_create_query
}

def run_query(prefix: str, table: str, query: str, verbose=0) -> None:
    try:
        if verbose > 1:
            print(f"Running query, {prefix} {table}:")
            print(query)

        # Open a new process with a pipe for stdin.
        command = 'zsh'
        # process = subprocess.Popen(command, stdin=subprocess.PIPE)
        q=f'{start}\n{query}'
        encoded_string = q.encode('utf-8')
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
          shell=True, executable="/bin/zsh")

        # Communicate with the process. This sends data to stdin and returns data from stdout and stderr.
        output, err = process.communicate(input=encoded_string)

        if verbose > 0 and output:
            print(f"Output from {prefix} {table} query:")
            print(output.decode('utf-8'))
        if err:
            error(f"Failures while {prefix} {table} query: {err.decode('utf-8')}")

    except Exception as e:
        error(f"An Exception {type(e)} occurred running the queries: {e}")

for table in queries:
    run_query('create', table, queries[table], args.verbose)

if args.verbose > 0:
    run_query('check that tables are present', '', '.tables', verbose=2)
    info(f"We expect the following tables: {list(queries.keys())}")
    for table in queries:
        run_query('count rows for', table, f'SELECT count() from {table};', verbose=2)
