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

sys.path.append( "../../" )

from core import *
from init import *

parser = argparse.ArgumentParser( description = 'Filters' )
parser.add_argument( '--from_date', type = str, default = None, help = 'Date from' )
parser.add_argument( '--to_date', type = str, default = None, help = 'Date to' )
args = parser.parse_args()

oy = []
ox = []
iy = []
ix = []

f = parse( args.from_date ).strftime( '%s' ) if args.from_date != None else None
e = parse( args.to_date ).strftime( '%s' ) if args.to_date != None else None

out = Transaction.fetchChargeDateList( f, e )
inc = Transaction.fetchIncomeDateList( f, e )

kout = out.keys()
kinc = inc.keys()
kout.sort()
kinc.sort()

totalChanrges = 0
totalIncome = 0

for i in kout:
    d = datetime.datetime.fromtimestamp( i ).strftime( "%Y-%m-%d" )
    totalChanrges += out[i]
    print d + " = " + str( out[i] )
    ox.append( d )
    oy.append( out[i] )
    if i not in inc:
        inc[i] = 0

    ix.append( d )
    iy.append( inc[i] )
    totalIncome += inc[i]

N = len( ox )
def format_date( xx, pos = None ):
    i = np.clip( int( xx + 0.5 ), 0, N - 1 )
    return ( ox[i] )

fig = plt.figure( "Balance" )
ax = fig.add_subplot( 111 )
ax.plot( oy )
ax.plot( iy )

ax.set_title( "{0:.2f}".format( totalIncome ) + " - " + "{0:.2f}".format( totalChanrges ) + " = " + "{0:.2f}".format( totalIncome - totalChanrges ) + ' NOK' )
ax.grid( True )
#ax.set_xlabel( 'date' )
ax.set_ylabel( 'NOK' )
ax.xaxis.set_major_formatter( ticker.FuncFormatter( format_date ) )

fig.autofmt_xdate()

plt.show()
