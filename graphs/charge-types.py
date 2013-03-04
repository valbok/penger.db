#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

from pylab import *

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

f = parse( args.from_date ).strftime( '%s' ) if args.from_date != None else None
e = parse( args.to_date ).strftime( '%s' ) if args.to_date != None else None

if f != None:
    print "From timestamp: " + str( f )

if e != None:
    print "To timestamp: " + str( e )

typeDict = \
{
    'Food': [ 'FAVORITTEN', 'VADSETH', 'BEST', 'S\-LAG', 'PADMAX', 'MEGA', 'KIOSK AS', 'MAT', 'Rimi', 'KIWI', 'COOP', 'SPAR', 'REMA', 'EUROSPAR', 'ICA', 'EUROPRIS', 'JOKER', 'BUNNPRIS', 'MENY', 'LONG CHENG', 'ASIAN', 'JULEHUSET', 'KONDITORI' ],
    'AES Rent': [ '5353\.10\.19756', '5353\.11\.04796', 'HESSAVEGEN'  ],
    'Rent': [ '.konomisjefen', '6559\.10\.23831', 'Sj.mannsveien', '6557\.10\.18467' ],
    'Cash': [ 'Sparebanken', 'NORDEA' ],
    'Kids and fun': [ 'ATLANTERHAVSP', 'AGGI AS', 'PRINCESS', 'KID', 'GODTFRES', 'LEKER', 'BURGER KING', 'LEKELAND', 'SV.MMEHALL', 'BR-LEKER', 'ATLANTERHAVSPAR', 'BRIO', 'RINGO', 'MCDONALDS', 'HJEM-IS', '.LESUND KOMMUNE', 'GRYTESTRANDA BA', 'BUTGER KING' ],
    'Health': [ 'GLITTER', 'LEGEKONTOR', 'TANNK', 'Lege', 'APOTEK', 'LEGESEN', 'SYKEHUSAPOTEKET', 'VITUSAPOTEK', 'VITA', 'SYKEHUS', 'POLIKLINIKK', 'LEGE' ],
    'Car and transfers': [ 'JOKER VATNE', 'KLEIVANE', 'SHELL', 'SHELL/7\-ELEVEN', 'MF', 'MRTAXI', 'AUTOI', 'DEKKTEAM', 'ISS', 'BILLETT', 'SNARKJØP', 'BOMPENGE', 'Nettbuss', 'FJORD1', 'Fatlatunnelen', 'AUTOSENTE', 'Terra Forsikring', 'YX', 'BILSERV', 'ESSO', 'STATOIL', 'TRAFIKKSKULE', 'UNO-X', 'TEMA', 'BUNKER', 'TRAFIKK', 'FJORD', 'BRABILAS', 'TINGHUSET', 'BOMRINGEN', 'JANGAARD', 'Jangaard', 'STRAUMSBRUA' ],
    'Alcohol': [ 'VINMONOPOLET' ],
    'Mob and net': [ 'Telenor', 'TELE2',  'INTERNET', 'TELENOR' ],
    'House and home devices': [ 'SKANDIA AUTOMATER AS', 'MEDIA', 'Sunnm.rspos', 'BOK \& PAPIR', 'JULA', 'ELKJ.P', 'EXPERT', 'LEFDAL', 'JYSK', 'PLANTASJEN', 'CLAS OHLSON' ],
    'Devices and comp': [ 'DATA', 'KOMPLETT.NO', 'JAPAN PHOTO', 'ELITEFOTO' ],
    'Electricity': [ 'TAFJORD', 'NORDVEST' ],
    'Tren': [ 'Treningssenter' ],
    'Clothes': [ 'VIVIKES', 'LINDEX', 'UTLENDINGSK', 'AARFLOT', 'BARNEMOTE', 'GINA', 'LOCATION', 'ELISABETH', 'VIC WOMAN', 'NAME IT', 'VILA', 'NILLE', 'LYSPUNKTET', 'VERO', 'FRETEX', 'CMYK', 'BAT AS', 'PLATOU', 'ANNES', 'KLONDIKE', 'MONARK', 'YOUNG', 'SUPER G','XXL', 'MORRIS', 'FOOTWEAR', 'KONIMIS', 'H&M', 'CUBUS', 'B\.RONGVI', 'MEGA', 'MANI', 'BABY', 'BARNAS', 'KAPPAHL', 'KREMMERHUSET', 'LINDEX', 'SKO', 'SKOPUNKTEN',  'KNUTEPUNKT' ],
    'Post': [ 'Post' ],
    'Leisure': [ 'NORWEGIAN', 'QUALITY AIRPORT', 'LUSTER', 'SAS', 'LOM', 'SPORTSHANDELEN', 'DUTY FREE', 'KAFETER', 'KR.MARHUSET', 'BAKERIET', 'AURMO DRIFT AS', 'TROLLSTIGEN', 'RESTAUR', 'SMAK', 'YRIS', 'GODTELAND', 'CARDLINE', 'SGS', 'KOKARSTEINEN', 'GODTELAND', 'EGON', 'TH\.BAKKENS', 'SERVICEST', 'J\.SLETTEDAL', 'JUGENDSTILSENTE', 'FJELLSTUA', 'Geiranger', 'STORDAL', 'BG\.KUNSTMUSEUM', 'GEIRANGER', 'RIGA','AVINOR', 'CZK', 'TANTE', 'Hotel', 'BILLETTSERVICE', 'P\-HOTELS', 'HOTELL', 'AKVARIET', 'TROLLSTIGEN', 'KAFE', 'SAS', 'AIRBALTIC', 'AIRPORT', 'BAGAZAS' ],
    'Transfers': [ 'DOROSHCHUK', 'OSTROVERSHENKO', 'OSTROVERSHENK', 'TIL:', 'Gjemnes' ],
    'Accounts': [ 'POLITISTASJONEN', 'POLITIDISTRIKT', 'Bankkort', 'VISA', 'FINN\.NO', 'Visa Classic', 'TRANS(ER)', 'TRANS', 'DEBETRENTER', 'Foreningen' ],
    'Hobby': [ 'SMALL SIZE', 'FOTO', 'PAYPAL', 'HOSTING CENTER', 'FOTO\-REKLAME', 'STUDIEFORBUNDET', 'WWW\.HETZNER\.DE'  ]

}
typePercentDict = {}
result = []
handled = {}

d = Transaction.fetchPercentChargeList( userID, f, e )
for typeKey in typeDict:
    tp = 0
    ta = 0
    print "\nBEGIN: " + typeKey + "\n"
    typeList = typeDict[typeKey]
    for i in d:
        desc = i["desc"]
        p = i["percent"]
        a = i["amount"]
        for q in typeList:
            rs = r"\b" + q + r"\b"
            if re.search( rs, desc, re.I ):
                if i["id"] in handled:
                    continue

                print str( i["percent"] ) + "% [" + str( i["similar_count"] ) + "/" + str( i["total_count"] ) + "] [" + str( i["amount"] ) + "/" + str( i["total_amount"] ) + "] [id:" + str( i["id"] ) + "] \n\t" + i["desc"] + "\n\t"  + i["reg_exp"]
                tp += p
                ta += a
                handled[i["id"]] = p


    print "\nEND: " + typeKey + ": " + str( ta ) + " NOK, " + str( tp ) + "%\n"
    result.append( { 'type': typeKey, 'percent': tp, 'amount': ta, 'total_amount': i["total_amount"] } )

def cmpfunc( a, b ):
    if a['percent'] < b['percent']:
        return -1

    if a['percent'] > b['percent']:
        return 1

    return 0

result.sort( cmp = cmpfunc )
percentList = []
labelList = []
totalP = 0
totalA = 0
for i in result:
    totalP += i['percent']
    totalA = i['total_amount']
    percentList.append( i['percent'] )
    labelList.append( i['type'] + ": " + str( i["amount"] ) )

percentList.append( 100 - totalP )
labelList.append( 'Unknown' )

# make a square figure and axes
figure( "Outcome", figsize = ( 6,6 ) )
ax = axes( [0.1, 0.1, 0.8, 0.8] )

# The slices will be ordered and plotted counter-clockwise.
labels = labelList
fracs = percentList

pie( fracs,  labels=labels, autopct='%1.1f%%', shadow=True)

title( str( totalA ) + " NOK", bbox={ 'facecolor':'0.8', 'pad':10})

show()
