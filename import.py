#!/usr/bin/env python
"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

"""
" CLI import script to upload data in csv format to database
"""
import sys
import csv
import argparse
from core import *

parser = argparse.ArgumentParser( description='Process some integers.' )
parser.add_argument( 'path', metavar = 'f', type = str, help = 'Path to csv file' )
parser.add_argument( '--type', type = str, default = "sbm",  help='Type of import: sbm or scandia' )

args = parser.parse_args()
path = args.path
type = args.type

try:
    if type == "sbm":
        i = Sbm( path )
    elif type == "scandia":
        i = Scandia( path )
    else:
        print "'%s' type is not valid" % type
        sys.exit( 1 )
except IOError:
    print "'%s' file does not exist or cannot be opened" % path
    sys.exit( 1 )

DB.init( db = "penger" )
db = DB.get()
db.begin()

print "%s processed" % len( i.process( 1 ) );

db.commit()
