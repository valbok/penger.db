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
parser.add_argument( '--year', type = int, default = None, help = 'Year' )
parser.add_argument( '--user_id', type = str, default = "1", help = 'User ID' )

args = parser.parse_args()
userID = args.user_id

monthBalanceList = []
totalBalance = 0

now = datetime.datetime.now()
year = args.year if args.year != None else now.year
monthes = []
for i in range( 1, 13 ):
    f = parse( str( year ) + "-" + str( i ) + "-01" ).strftime( '%s' )
    d = calendar.monthrange( year, i )[1]
    e = parse( str( year ) + "-" + str( i ) + "-" + str( d ) ).strftime( '%s' )

    totalCharges = Transaction.fetchTotalCharges( userID, f, e )
    totalIncome = Transaction.fetchTotalIncome( userID, f, e )
    mname = calendar.month_name[i]
    r = totalIncome - totalCharges
    totalBalance += float( r )
    print mname + ": " + "{0:.2f}".format( totalIncome - totalCharges )
    monthes.append( mname )
    monthBalanceList.append( float( r ) )

print "Total = " + str( totalBalance )

fig = plt.figure( "Balance for " + str( year ) + " year" )
ax = fig.add_subplot( 111 )
ax.grid( True )
width = 1#0.35
N = len( monthBalanceList )
ind = np.arange( N )

def hex_to_rgb(value):
    value = value.lstrip( '#' )
    lv = len( value )

    return tuple( float( int( value[i : i + lv/3], 16 ) ) / 240 for i in range( 0, lv, lv/3))

rects1 = plt.bar(
            ind,
            monthBalanceList,
            width,
            color = hex_to_rgb( '#e5e5e5' )
            #error_kw = dict( elinewidth = 6, ecolor = 'pink' )
            )

plt.ylabel( 'NOK' )
plt.xlabel( "Total balance for this year = " + str( totalBalance ) )
plt.xticks( ind + width - 0.5, monthes )

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
