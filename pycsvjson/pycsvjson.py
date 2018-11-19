""" Script to map CSV files to JSON and load into RethinkDB """
# -*- coding: utf-8 -*-
## Copyright (c) 2017 Nicholas K Tulach

## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:

## The above copyright notice and this permission notice shall be included in all
## copies or substantial portions of the Software.

## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
## SOFTWARE.

import argparse
import csv
import os
import ujson as json
from boltons.iterutils import remap
from jsonschema import RefResolver
from jsonmapping import Mapper
from tqdm import tqdm

__version__ = '0.0.5'

TEMPFILE = 'temp.csv'

def convert_file(in_file, out_file):
    from bs4 import UnicodeDammit
    with open(in_file, 'rb') as source, \
         open(out_file, mode='w', encoding='utf-8-sig') as out:
        for line in source:
            dammit = UnicodeDammit(line)
            out.write(dammit.unicode_markup)

def row_count(filename):
    """ Counts the rows in a given file """
    count = 0
    with open(filename, 'r') as ofp:
        for _ in ofp:
            count = count + 1
        # Remove header row from count
        count = count - 1 if count > 0 else count
    return count

def file_to_json(mapfile):
    """ Given a filename string pointing to a JSON mapping, returns a
        dictionary representation of the JSON file
    """
    if isinstance(mapfile, str):
        with open(mapfile, 'r') as filehandle:
            return json.load(filehandle)
    else:
        return json.load(mapfile)

def not_empty(collection):
    """ For collection objects (lists and dictionaries), check if the collection
        is empty. Returns True if not empty; false otherwise
    """
    if isinstance(collection, (dict, list)):
        return bool(collection)
    return True

def map_row(csvfile, mapfile, columns=None):
    """ Generator function that transforms a CSV row into a mapped
        dictionary object, one row at a time
    """
    mapping = file_to_json(mapfile)
    resolver = RefResolver.from_schema(mapping)
    mapper = Mapper(mapping, resolver)
    drop_blank = lambda p, k, v: v is not None and v != "" and not_empty(v)
    total_rows = row_count(csvfile)

    if isinstance(csvfile, str):
        csvfp = open(csvfile, 'r', encoding='utf-8-sig')
    for row in tqdm(csv.DictReader(csvfp), total=total_rows):
        row = {key: value for key, value in row.items() if key in columns} \
            if columns else row
        _, data = mapper.apply(row)
        data = remap(data, visit=drop_blank)
        yield data

def main():
    """ Main function for csvtojson application """
    parser = argparse.ArgumentParser()
    parser.add_argument('csvfile', help='CSV source file')
    parser.add_argument('mapfile', help='JSON mapping file, including schema')
    parser.add_argument('-o',
                        '--output',
                        help='Output file name',
                        default='output.json')
    parser.add_argument('-p',
                        '--pretty',
                        action='store_true',
                        help='Indent resulting JSON file')
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))
    args = parser.parse_args()
    with open(args.output, 'w') as ofp:
        try:
            convert_file(args.csvfile, TEMPFILE)
            indent = 4 if args.pretty else 0
            json.dump(map_row(TEMPFILE, args.mapfile), ofp, indent=indent)
        finally:
            try:
                os.remove(TEMPFILE)
            except OSError:
                pass

if __name__ == "__main__":
    main()
