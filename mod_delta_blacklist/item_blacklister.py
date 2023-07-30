#!/usr/bin/env python3

import os
import json
import argparse

parser = \
argparse.ArgumentParser(
  prog = r"blacklister",
  description = r"""Creates a CDDA mod blacklisting a variety of things that
                    I decided to blacklist.""" )

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
  return ( "chainmail" in n )

def check_record( x ):
  if type( x ) is dict and "id" in x and "name" in x:
    if type( x["name"] ) is str:
      return check_name( x["name"] )
    elif type( x["name"] ) is dict:
      for k in ("str","str_pl","str_sp"):
        if k in x["name"] :
          return check_name( x["name"][k] )
  return False

THE_ITEM_BLACKLIST = {
  "type": "ITEM_BLACKLIST",
  "whitelist": False,
  "items": []
}

RECORDS_TO_ALTER = []

for jfn in JSON_FILENAMES:
  with open( jfn, 'r' ) as jfp:
    try:
      json_data = json.load( open( jfn, 'r' ) )
    except JSONDecodeError :
      print( "Invalid JSON file: {}".format( jfn ) )
      continue

    if type( json_data ) is dict:
      if check_record( json_data ):
        RECORDS_TO_ALTER.append( json_data )
    elif type( json_data ) is list:
      for x in json_data:
        if check_record( x ):
          RECORDS_TO_ALTER.append( x )

RECORDS_TO_OUTPUT = []

for old_rec in RECORDS_TO_ALTER:
  #new_rec = {}
  
  #new_rec["type"] = old_rec["type"]
  #new_rec["id"] = old_rec["id"]
  #new_rec["copy-from"] = old_rec["id"]
  
 # new_rec["autolearn"] = False

#  RECORDS_TO_OUTPUT.append(new_rec)
  
  THE_ITEM_BLACKLIST["items"].append( old_rec["id"] );

#print( json.dumps(RECORDS_TO_OUTPUT, indent=2) )

print( json.dumps([ THE_ITEM_BLACKLIST ], indent=2) )
