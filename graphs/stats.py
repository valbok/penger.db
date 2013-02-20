#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

import argparse
import sys

sys.path.append( "../" )

from core import *
from init import *

parser = argparse.ArgumentParser( description = 'Filters' )
parser.add_argument( '--from_date', type = str, default = None, help = 'Date from' )
parser.add_argument( '--to_date', type = str, default = None, help = 'Date to' )
parser.add_argument( '--user_id', type = str, default = "1", help = 'User ID' )

args = parser.parse_args()
userID = args.user_id

f = parse( args.from_date ).strftime( '%s' ) if args.from_date != None else None
e = parse( args.to_date ).strftime( '%s' ) if args.to_date != None else None

if f != None:
    print "From timestamp: " + str( f )

if e != None:
    print "To timestamp: " + str( e )

d = Transaction.fetchPercentChargeList( userID, f, e )
p = 0
a = 0
for i in d:
    p += i["percent"]
    a += i["amount"]
    print str( i["percent"] ) + "% [" + str( i["similar_count"] ) + "/" + str( i["total_count"] ) + "] [" + str( i["amount"] ) + "/" + str( i["total_amount"] ) + "] [id:" + str( i["id"] ) + "] \n\t" + i["desc"] + "\n\t"  + i["reg_exp"]

print "Checksum: "
print "\t %: " + str( p )
print "\t amount: " + str( a )

#checkedTotalCharges = abs( checkedTotalCharges )
#print "Checksum NOK: " + str( checkedTotalCharges )
#print "Checksum %: " + str( totalPercent )
