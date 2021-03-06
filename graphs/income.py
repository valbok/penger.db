#!/usr/bin/env python
"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

import matplotlib.ticker as ticker
import argparse
import datetime
import numpy as np
import matplotlib.pyplot as plt
import sys

sys.path.append( "../" )

from core import *
import init

parser = argparse.ArgumentParser( description = 'Filters' )
parser.add_argument( '--from_date', type = str, default = None, help = 'Date from' )
parser.add_argument( '--to_date', type = str, default = None, help = 'Date to' )
parser.add_argument( '--user_id', type = str, default = "1", help = 'User ID' )

args = parser.parse_args()
userID = args.user_id

# Data for Y
y = []
# Data for X
x = []

f = parse( args.from_date ).strftime( '%s' ) if args.from_date != None else None
e = parse( args.to_date ).strftime( '%s' ) if args.to_date != None else None
l = Transaction.fetchIncomeDateList( userID, f, e )
kk = l.keys()
# Dates sorted by ASC
kk.sort()
# What has been earned totally for period
total = 0

for i in kk:
    total += l[i]
    print datetime.datetime.fromtimestamp( i ).strftime( "%Y-%m-%d" ) +" = " + str( l[i] )
    x.append( datetime.datetime.fromtimestamp( i ).strftime( "%Y-%m-%d" ) )
    y.append( l[i] )

N = len( x )
def format_date( xx, pos = None ):
    i = np.clip( int( xx + 0.5 ), 0, N - 1 )
    return ( x[i] )

fig = plt.figure( "Total income" )
ax = fig.add_subplot(111)
ax.plot( y )
ax.set_title( "{0:.2f}".format( total ) + ' NOK' )
ax.grid( True )
#ax.set_xlabel( 'date' )
ax.set_ylabel( 'NOK' )
ax.xaxis.set_major_formatter( ticker.FuncFormatter( format_date ) )

fig.autofmt_xdate()

plt.show()
