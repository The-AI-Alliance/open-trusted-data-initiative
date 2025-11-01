#!/usr/bin/env python
from typing import Any, Dict, List
from datetime import datetime
import argparse, json, os, pathlib, re, sys, tempfile
import pandas as pd
from common import beep, error, warning, info, make_directories

class StringsToJSON:
    def __init__(self):
        self.error_count: int = 0
        self.total_count: int = 0

    def error_str(self, error: Exception, s: str):
        return f"{type(error)}: {error}. (count = {self.error_count} out of {self.total_count}) Ignoring: string = {s}"

    def parse(self, s: str) -> (bool, Dict[str,Any], str):
        self.total_count += 1
        try:
            obj = json.loads(s)
            return (True, obj, '')
        except json.decoder.JSONDecodeError as err:
            self.error_count += 1
            return (False, {}, self.error_str(err, s))

class CroissantExtractor:
    unquote         = re.compile(r'(^"|"$)')      # match " at beginning and end (to remove them below)
    unescape_quote  = re.compile(r'(?!\\)\"')     # match cases of SINGLE \ in '\"' (to remove the '\')
    unescape_slash  = re.compile(r'\\+/')         # match '\/' for 1+ '\' (to remove the '\+')
    unescape_others = re.compile(r'\\+(?=["nt])') # match '\\n', '\\t', etc. for 2+ '\\' (to remove the extras)

    def __init__(self, errors_dir: str = '.'):
        self.errors_dir = errors_dir
        self.errors_file = None
        self.toJSON = StringsToJSON()

    def unescape(self, s: str) -> str:
        s1 = re.sub(CroissantExtractor.unquote,         '',    s)
        s2 = re.sub(CroissantExtractor.unescape_quote,  '"',   s1)
        s3 = re.sub(CroissantExtractor.unescape_slash,  '/',   s2)
        s4 = re.sub(CroissantExtractor.unescape_others, r'\\', s3)
        return s4

    def __call__(self, row: Dict[str,Any]) -> (bool, Dict[str,Any], str):
        cr = row.get("croissant")
        if not cr:
            return False, {}, f"row doesn't have a 'croissant' field! Ignoring: row = {row}"

        js = self.unescape(cr)
        success, js, error_str = self.toJSON.parse(cr)
        if success:
            return True, js, ''
        else:
            return False, {}, error_str

def parquet_to_json(args):
    """
    Reads the HF-derived metadata from parquet files and writes the "croissant" JSON column to JSON files.
    """

    info("NOTE: This program runs for a looong time!")

    make_directories(args.output, delete_first=True, verbose=args.verbose)
    make_directories(args.errors, delete_first=True, verbose=args.verbose)

    # Read the Parquet files using Pandas
    df1 = pd.read_parquet(args.input, engine='pyarrow')
    objs = df1.to_dict(orient='records')
    
    list_count = len(objs)
    if args.verbose > 1:
        info("The input dataset size and first record:")
        info(f"  count: {list_count}")
        info(f"  first: {objs[0]}")

    counts = {}
    successful_count = 0
    error_count = 0
    jsons = []
    with tempfile.NamedTemporaryFile(dir=args.errors, delete=False) as errors_out:
        extractor = CroissantExtractor()

        for obj in objs:
            response_reason = obj['response_reason']
            counts[response_reason] = counts.get(response_reason, 0) + 1

            if response_reason == 'OK':
                success, obj, error_str = extractor(obj)
                if not success:
                    error_count += 1
                    warning(error_str, file = errors_out)
                else:
                    successful_count += 1
                    jsons += [obj]
    
    with open(f'{args.output}/croissant.json', 'w') as json_out:
        json.dump(jsons, json_out, indent="\t")

    if args.verbose > 0:
        info("Counts:")
        info(f"  input:            {list_count:-8d}")
        info(f"  errors:           {error_count:-8d} (where extracting JSON failed)")
        info(f"  successful:       {successful_count:-8d} (where extracting JSON succeeded)")
        info(f"  response reasons seen with counts:")
        for reason in sorted(counts):
            info(f"  {reason:-15s}:        {counts[reasons]:-8d}")

def run():
    parser = argparse.ArgumentParser(
                        prog='parquet-to-json',
                        description='Reads HF metadata from Parquet and writes what we need to JSON',
                        epilog='')
    parser.add_argument('-v', '--verbose',
                        help="Verbosity level for output. Higher numbers result in more details. Default value is 1. Use 0 for very little output.",
                        type=int,
                        default=1) 
    parser.add_argument('-i', '--input',
                        required=True,
                        help="The input directory of parquet files.")
    parser.add_argument('-o', '--output',
                        required=True,
                        help="The output directory for JSON files.")
    parser.add_argument('-e', '--errors',
                        required=True,
                        help="The output directory for error logs.")
    args = parser.parse_args(sys.argv[1:])
    parquet_to_json(args)

    info(f"Output written to {args.output}")
    beep()

if __name__ == "__main__":
    run()
