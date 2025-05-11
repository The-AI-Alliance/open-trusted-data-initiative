#!/usr/bin/env python

import argparse, glob, io, json, os, sys

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

def delete_file(file_path, verbose: bool = True):
    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            raise Exception(f"Directory passed to delete_file: {file_path}")
        elif os.path.isfile(file_path):
            try:
                os.remove(file_path)
                if verbose:
                    print(f"File {file_path} deleted successfully.")
            except Exception as e:
                print(f"An error occurred: {e}")
    elif verbose:
        print(f"File {file_path} does not exist.")

def get_file_paths(full_pattern: str) -> list[str]:
    return glob.glob(full_pattern)

def get_files_in_directory(directory: str, pattern: str) -> list[str]:
    return get_in_file_paths(os.path.join(directory, pattern))

def parse_args():
    parser = argparse.ArgumentParser(
                        prog='parse-json',
                        description='Parse JSON files with "JSONL" records. Discard bad lines.',
                        epilog='')
    parser.add_argument('-i', '--input',
                        required=True,
                        help=f"A file name or path glob of JSON files to input (required).")
    parser.add_argument('-o', '--output',
                        required=True,
                        help="The output JSON file to write (required). If it already exists, it will be overwritten.")
    parser.add_argument('-n', "--num-lines",
                        type=int,
                        default=-1,
                        help="Stop after processing N lines in each file (default: process all lines).")
    parser.add_argument('-v', '--verbose',
                        help="Show verbose output",
                        action='store_true')  # on/off flag
    args = parser.parse_args(sys.argv[1:])
    return args

def longest_path_length(paths: list[str]) -> int:
    length = 0
    for path in paths:
        plen = len(path)
        if plen > length:
            length = plen
    return length

args = parse_args()
in_file_paths  = get_file_paths(args.input)
path_len = longest_path_length(in_file_paths)
out_file_path = args.output
delete_file(out_file_path, verbose=args.verbose)

with open(out_file_path, 'w') as out:
    line_count = {}
    bad_line_count = {}
    for in_file_path in in_file_paths:
        if args.verbose:
            print(f"Processing input file: {in_file_path}...")
        line_count[in_file_path] = 0
        bad_line_count[in_file_path] = 0
        for i, line in read_file_line_by_line(in_file_path):
            try:
                line2 = print_to_string(line)
                js = json.loads(line2)
                line_count[in_file_path] = line_count[in_file_path] + 1
            except json.decoder.JSONDecodeError as err:
                print(f"json.decoder.JSONDecodeError: {err}: line {i} will be ignored: {line2}")
                bad_line_count[in_file_path] = bad_line_count[in_file_path] + 1
            except Error as err:
                print(f"Error: {err}: line {i} will be ignored: {line2}")
                bad_line_count[in_file_path] = bad_line_count[in_file_path] + 1
            json.dump(js, out)
            print("", file=out)
            if args.num_lines > 0 and args.num_lines <= i:
                break

if args.verbose:
    file_str_fmt = "{0:>"+str(path_len)+"}:"
    print("Error statistics:")
    file_str=file_str_fmt.format("file")
    print(f"  {file_str}    total    bad        %")
    for in_file_path in in_file_paths:
        total = line_count[in_file_path]
        bad   = bad_line_count[in_file_path]
        percentage = bad*100.0/total
        file_str=file_str_fmt.format(in_file_path)
        print(f"  {file_str}  {total:7d}  {bad:5d}   {percentage:-5.3f}%")
    print(f"output file: {out_file_path}")
