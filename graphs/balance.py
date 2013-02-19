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
from init import *

parser = argparse.ArgumentParser( description = 'Filters' )
parser.add_argument( '--from_date', type = str, default = None, help = 'Date from' )
parser.add_argument( '--to_date', type = str, default = None, help = 'Date to' )
parser.add_argument( '--user_id', type = str, default = "1", help = 'User ID' )

args = parser.parse_args()
userID = args.user_id

oy = []
ox = []
iy = []
ix = []

f = parse( args.from_date ).strftime( '%s' ) if args.from_date != None else None
e = parse( args.to_date ).strftime( '%s' ) if args.to_date != None else None

if f != None:
    print "From timestamp: " + str( f )

if e != None:
    print "To timestamp: " + str( e )

out = Transaction.fetchChargeDateList( userID, f, e )
inc = Transaction.fetchIncomeDateList( userID, f, e )

kout = out.keys()
kinc = inc.keys()
kout.sort()
kinc.sort()

totalCharges = Transaction.fetchTotalCharges( userID, f, e )
totalIncome = Transaction.fetchTotalIncome( userID, f, e )

balanceList = []

for i in kout:
    d = datetime.datetime.fromtimestamp( i ).strftime( "%Y-%m-%d" )
    print d + " = " + str( out[i] )
    ox.append( d )
    oy.append( out[i] )
    if i not in inc:
        inc[i] = 0

    ix.append( d )
    iy.append( inc[i] )

    bb = Transaction.fetchBalance( userID, endTS = i )
    print "\tbalance = " + str( bb )
    balanceList.append( bb )

N = len( ox )
def format_date( xx, pos = None ):
    i = np.clip( int( xx + 0.5 ), 0, N - 1 )
    return ( ox[i] )

fig = plt.figure( "Balance" )
ax = fig.add_subplot( 111 )
p1, = ax.plot( oy )
p2, = ax.plot( iy )
p3, = ax.plot( balanceList )
ax.legend( [p3, p2, p1], ["Balance", "Income", "Charge"] )

ax.set_title( "{0:.2f}".format( totalIncome ) + " - " + "{0:.2f}".format( totalCharges ) + " = " + "{0:.2f}".format( totalIncome - totalCharges ) + ' NOK' )
ax.grid( True )
#ax.set_xlabel( 'date' )
ax.set_ylabel( 'NOK' )
ax.xaxis.set_major_formatter( ticker.FuncFormatter( format_date ) )

fig.autofmt_xdate()

plt.show()
