#!/usr/bin/env python
"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

import matplotlib.ticker as ticker

import datetime
import numpy as np
import matplotlib.pyplot as plt
import sys

sys.path.append( "../../" )

from core import *
from init import *

# Data for Y
y = []
# Data for X
x = []
l = Transaction.fetchDateCreditList()
kk = l.keys()
# Dates sorted by ASC
kk.sort()
# What has been spent totally for period
totalChanrges = 0

for i in kk:
    totalChanrges += l[i]
    print datetime.datetime.fromtimestamp( i ).strftime( "%Y-%m-%d" ) +" = " + str( l[i] )
    x.append( datetime.datetime.fromtimestamp( i ).strftime( "%Y-%m-%d" ) )
    y.append( l[i] )

N = len( x )
def format_date( xx, pos = None ):
    i = np.clip( int( xx + 0.5 ), 0, N - 1 )
    return ( x[i] )

fig = plt.figure( "Total changes" )
ax = fig.add_subplot( 111 )
ax.plot( y )
ax.set_title( "{0:.2f}".format( totalChanrges ) + ' NOK' )
ax.grid( True )
#ax.set_xlabel( 'date' )
ax.set_ylabel( 'NOK' )
ax.xaxis.set_major_formatter( ticker.FuncFormatter( format_date ) )

fig.autofmt_xdate()

plt.show()
