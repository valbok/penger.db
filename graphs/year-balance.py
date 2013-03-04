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
import matplotlib.patches as patches
import matplotlib.path as path
import sys
import calendar

sys.path.append( "../" )

from core import *
from init import *

parser = argparse.ArgumentParser( description = 'Filters' )
parser.add_argument( '--user_id', type = str, default = "1", help = 'User ID' )

args = parser.parse_args()
userID = args.user_id

yearBalanceList = []
totalBalance = 0
years = []
now = datetime.datetime.now()
for i in range( 2010, now.year + 1 ):
    f = parse( str( i ) + "-01-01" ).strftime( '%s' )
    e = parse( str( i ) + "-12-31" ).strftime( '%s' )

    totalCharges = Transaction.fetchTotalCharges( userID, f, e )
    totalIncome = Transaction.fetchTotalIncome( userID, f, e )
    r = totalIncome - totalCharges
    totalBalance += float( r )
    years.append( str( i ) )
    print str( i ) + ": " + "{0:.2f}".format( r )
    yearBalanceList.append( float( r ) )

print "Total = " + str( totalBalance )

fig = plt.figure( "Total balance by years" )
ax = fig.add_subplot( 111 )
ax.grid( True )
width = 1#0.35
N = len( yearBalanceList )
ind = np.arange( N )

def hex_to_rgb(value):
    value = value.lstrip( '#' )
    lv = len( value )

    return tuple( float( int( value[i : i + lv/3], 16 ) ) / 240 for i in range( 0, lv, lv/3))

rects1 = plt.bar(
            ind,
            yearBalanceList,
            width,
            color = hex_to_rgb( '#e5e5e5' )
            #error_kw = dict( elinewidth = 6, ecolor = 'pink' )
            )

plt.ylabel( 'NOK' )
plt.xlabel( "Total balance = " + str( totalBalance ) )
plt.xticks( ind + width - 0.5, years )

def autolabel( rects ):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        y = rect.get_y()
        if y < 0:
            height = 0 - height

        plt.text(
            rect.get_x() + rect.get_width() / 2.,
            1.01 * height if height > 0 else height - 0.02 * height,
            '%s' % float( height ),
            ha='center',
            color = hex_to_rgb( '#333333' ),
            va='bottom'
        )

autolabel( rects1 )
plt.show()
