#!/usr/bin/env python3

import os
import sys
import json
import argparse

parser = \
argparse.ArgumentParser(
  prog = r"no_pair_of",
  description = r"""Generates the no_pair_of mod for CDDA, removing 'pair of'
                    from the beginning of item names like 'pair of scissors'.""" )

parser.add_argument(r"data_dir")
args = parser.parse_args()

JSON_SEARCH_ROOT = os.path.abspath(args.data_dir)

JSON_FILENAMES = []

for root, dirs, files in os.walk(JSON_SEARCH_ROOT):
  for fn in files:
    abs_fn = os.path.abspath( os.path.join( root, fn ) );
    if abs_fn.endswith(".json"):
      JSON_FILENAMES.append(abs_fn)

ENTRY_TYPES = []

def check_name( n ):
  return n.startswith( "pair" )

def check_record( x ):
  if type( x ) is dict and "id" in x and "name" in x:
    if type( x["name"] ) is str:
      return check_name( x["name"] )
    elif type( x["name"] ) is dict:
      for k in ("str","str_pl","str_sp"):
        if k in x["name"] :
          return check_name( x["name"][k] )
  return False

RECORDS_TO_RENAME = []

for jfn in JSON_FILENAMES:
  with open( jfn, encoding='utf-8' ) as jfp:
    try:
      json_data = json.load( jfp )
    except json.JSONDecodeError as ex :
      print( "Invalid JSON file: {}".format( jfn ), file=sys.stderr )
      print( ex, file=sys.stderr )
      continue

    if type( json_data ) is dict:
      if check_record( json_data ):
        RECORDS_TO_RENAME.append( json_data )
    elif type( json_data ) is list:
      for x in json_data:
        if check_record(x):
          RECORDS_TO_RENAME.append( x )

RECORDS_TO_OUTPUT = []

for old_rec in RECORDS_TO_RENAME:
  new_rec = {}
  if "id" not in old_rec:
    print( old_rec )

  new_rec["id"] = old_rec["id"]
  new_rec["copy-from"] = old_rec["id"]
  new_rec["type"] = old_rec["type"]

  if "comestible_type" in old_rec:
    new_rec["comestible_type"] = old_rec["comestible_type"]

  if type( old_rec["name"] ) is str:
    new_rec["name"] = old_rec["name"].replace("pair of ", "")
  elif type( old_rec["name"] ) is dict:
    new_rec["name"] = {}

    if "str" in old_rec["name"]:
      new_rec["name"]["str"] = old_rec["name"]["str"].replace("pair of ", "")

    if "str_sp" in old_rec["name"]:
      new_rec["name"]["str_sp"] = old_rec["name"]["str_sp"].replace("pair of ", "")

    if "str_pl" in old_rec["name"]:
      new_rec["name"]["str_pl"] = old_rec["name"]["str_pl"].replace("pairs of ", "")

  RECORDS_TO_OUTPUT.append(new_rec)

print( json.dumps(RECORDS_TO_OUTPUT, indent=2) )
