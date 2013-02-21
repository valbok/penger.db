#-*- coding: UTF-8 -*-
"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

from ..lib import *
import hashlib
from dateutil.parser import parse
import re

"""
" One transaction payment
"""
class Transaction( PersistentObject ):
    _definition = Definition( table = "transaction", keys = [ "id" ], incrementField = "id" )

    """
    " @reimp
    """
    def __init__( self, list = {} ):
        PersistentObject.__init__( self, list )
        if not self.hasFields():
            return

        d = self.attr( 'date' )
        if ( not self._isInt( d ) ):
            d = parse( d ).strftime( '%s' )
            self.attr( 'date', d )

        self.attr( 'hash', self._createHash() )

    """
    " Creates hash based on submitted data
    "
    " @return (str)
    """
    def _createHash( self ):
        v = str( self.attr( 'date' ) ) + str( self.attr( 'payment' ) ) + self.attr( 'description' ) + str( self.attr( 'user_id' ) )

        return hashlib.md5( v ).hexdigest()

    """
    " Fetches object by id
    "
    " @return (__CLASS__)
    """
    @staticmethod
    def fetch( id ):
        o = Transaction()

        return o._fetchObjectByIncrementField( id )

    """
    " @reimp
    """
    def exists( self ):
        t = Transaction()

        return bool( t.fetchObject( "hash = '" + re.escape( self._createHash() ) + "'" ) )

    """
    " @return (list)
    """
    @staticmethod
    def fetchList( userID, where = None, limit = None, offset = None, orderByDict = { "date": DB.ASC } ):
        if where == None:
            where = "user_id = '" + str( int( userID ) ) + "'"
        else:
            where = "user_id = '" + str( int( userID ) ) + "' AND " + where

        return Transaction().fetchObjectList( where = where, limit = limit, offset = offset, orderByDict = orderByDict )

    """
    " @return (list)
    """
    @staticmethod
    def fetchChargeListByDates( userID, beginTS = None, endTS = None, limit = None, offset = None, orderByDict = { "date": DB.ASC } ):
        where = "payment < 0 "
        if beginTS != None:
            where += " AND date >= " + str( beginTS )

        if endTS != None:
            where += " AND date <= " + str( endTS )

        return Transaction().fetchList( userID, where, limit = limit, offset = offset, orderByDict = orderByDict )

    """
    " Counts credites by date
    "
    " @param (int)
    " @param (int)
    "
    " @return (dict( ts: value ))
    """
    @staticmethod
    def fetchChargeDateList( userID, beginTS = None, endTS = None ):
        result = {}
        dTable = Transaction()._definition.table

        where = " WHERE payment < 0 AND user_id = '" + str( int( userID ) ) + "'"
        if beginTS != None:
            where += " AND date >= " + str( beginTS )

        if endTS != None:
            where += " AND date <= " + str( endTS )

        sql = "SELECT date, sum( payment ) as result FROM {} {} GROUP BY date ORDER BY date ASC".format( dTable, where )
        db = DB.get()
        cur = db.cursor()
        cur.execute( sql )
        rows = cur.fetchall()
        for i in rows:
            result[i[0]] = abs( i[1] )

        return result

    """
    " Counts debits by date
    "
    " @param (int)
    " @param (int)
    "
    " @return (dict( ts: value ))
    """
    @staticmethod
    def fetchIncomeDateList( userID, beginTS = None, endTS = None ):
        result = {}
        dTable = Transaction()._definition.table

        where = " WHERE payment > 0 AND user_id = '" + str( int( userID ) ) + "'"
        if beginTS != None:
            where += " AND date >= " + str( beginTS )

        if endTS != None:
            where += " AND date <= " + str( endTS )

        sql = "SELECT date, sum( payment ) as result FROM {} {} GROUP BY date ORDER BY date ASC".format( dTable, where )
        db = DB.get()
        cur = db.cursor()
        cur.execute( sql )
        rows = cur.fetchall()
        for i in rows:
            result[i[0]] = i[1]

        return result

    """
    " Fetches total income
    "
    " @param (int)
    " @param (int)
    "
    " @return (float)
    """
    @staticmethod
    def fetchTotalIncome( userID, beginTS = None, endTS = None ):
        dTable = Transaction()._definition.table

        where = " WHERE payment > 0 AND user_id = '" + str( int( userID ) ) + "'"
        if beginTS != None:
            where += " AND date >= " + str( beginTS )

        if endTS != None:
            where += " AND date <= " + str( endTS )

        sql = "SELECT sum( payment ) as result FROM {} {}".format( dTable, where )
        db = DB.get()
        cur = db.cursor()
        cur.execute( sql )
        rows = cur.fetchall()

        return rows[0][0]

    """
    " Fetches total outcome
    "
    " @param (int)
    " @param (int)
    "
    " @return (float)
    """
    @staticmethod
    def fetchTotalCharges( userID, beginTS = None, endTS = None ):
        dTable = Transaction()._definition.table

        where = " WHERE payment < 0 AND user_id = '" + str( int( userID ) ) + "'"
        if beginTS != None:
            where += " AND date >= " + str( beginTS )

        if endTS != None:
            where += " AND date <= " + str( endTS )

        sql = "SELECT sum( payment ) as result FROM {} {}".format( dTable, where )

        db = DB.get()
        cur = db.cursor()
        cur.execute( sql )
        rows = cur.fetchall()

        return abs( rows[0][0] )

    """
    " Fetches total balance
    "
    " @param (int)
    " @param (int)
    "
    " @return (float)
    """
    @staticmethod
    def fetchBalance( userID, beginTS = None, endTS = None ):
        dTable = Transaction()._definition.table

        where = " WHERE user_id = '" + str( int( userID ) ) + "'"
        if beginTS != None:
            where += " AND date >= " + str( beginTS )

        if endTS != None:
            where += " AND date <= " + str( endTS )

        sql = "SELECT sum( payment ) as result FROM {} {}".format( dTable, where )

        db = DB.get()
        cur = db.cursor()
        cur.execute( sql )
        rows = cur.fetchall()

        return rows[0][0]

    """
    " Fetches similar transaction list to current
    "
    " @param (int)
    " @param (int)
    "
    " @return (float)
    """
    def fetchSimilarChargeList( self, level = 1, beginTS = None, endTS = None ):
        result = {}
        userID = self.attr( 'user_id' )
        hash = self.attr( 'hash' )
        desc = self.escapeString( self.attr( 'description' ) )

        where = "payment < 0"

        if level == 0:
            where += " AND description = '" + desc + "'"
        elif level == 1:
            desc = self.getDescriptionRegExp()

            where += " AND description RLIKE '" + desc + "'"

        if beginTS != None:
            where += " AND date >= " + str( beginTS )

        if endTS != None:
            where += " AND date <= " + str( endTS )

        result = self.fetchList( userID, where )

        return result


    """
    " @return (str)
    """
    def getDescriptionRegExp( self ):
        desc = self.attr( 'description' )
        desc = desc.replace( '\\', '\\\\' )
        desc = desc.replace( '[', '\[' )
        desc = desc.replace( ']', '\]' )
        desc = desc.replace( '*', '\\\*' )
        desc = desc.replace( "'", "\'" )
        desc = desc.replace( '"', '\"' )

        # 08.01
        desc = re.sub( '^[0-9][0-9]\.[0-9][0-9] ', r'[0-9]+.[0-9]+ ', desc )
        desc = re.sub( ' [0-9][0-9]\.[0-9][0-9] ', r' [0-9][0-9].[0-9][0-9]  ', desc )

        # 10022,0223
        desc = re.sub( '[0-9][0-9][0-9][0-9][0-9],[0-9][0-9][0-9][0-9]', r'[0-9]+,[0-9]+', desc )
        # 1000,0223
        desc = re.sub( '[0-9][0-9][0-9][0-9],[0-9][0-9][0-9][0-9]', r'[0-9]+,[0-9]+', desc )
        # 100,0223
        desc = re.sub( '[0-9][0-9][0-9],[0-9][0-9][0-9][0-9]', r'[0-9]+,[0-9]+', desc )
        # 86,9923
        desc = re.sub( '[0-9][0-9],[0-9][0-9][0-9][0-9]', r'[0-9]+,[0-9]+', desc )
        #1,0823
        desc = re.sub( '[0-9],[0-9][0-9][0-9][0-9]', r'[0-9]+,[0-9]+', desc )

        # 10022,022
        desc = re.sub( '[0-9][0-9][0-9][0-9][0-9],[0-9][0-9][0-9]', r'[0-9]+,[0-9]+', desc )
        # 1000,022
        desc = re.sub( '[0-9][0-9][0-9][0-9],[0-9][0-9][0-9]', r'[0-9]+,[0-9]+', desc )
        # 100,022
        desc = re.sub( '[0-9][0-9][0-9],[0-9][0-9][0-9]', r'[0-9]+,[0-9]+', desc )
        # 86,992
        desc = re.sub( '[0-9][0-9],[0-9][0-9][0-9]', r'[0-9]+,[0-9]+', desc )
        #1,082
        desc = re.sub( '[0-9],[0-9][0-9][0-9]', r'[0-9]+,[0-9]+', desc )

        # 10022,02
        desc = re.sub( '[0-9][0-9][0-9][0-9][0-9],[0-9][0-9]', r'[0-9]+,[0-9]+', desc )
        # 1000,02
        desc = re.sub( '[0-9][0-9][0-9][0-9],[0-9][0-9]', r'[0-9]+,[0-9]+', desc )
        # 100,02
        desc = re.sub( '[0-9][0-9][0-9],[0-9][0-9]', r'[0-9]+,[0-9]+', desc )
        # 86,99
        desc = re.sub( '[0-9][0-9],[0-9][0-9]', r'[0-9]+,[0-9]+', desc )
        #1,08
        desc = re.sub( '[0-9],[0-9][0-9]', r'[0-9]+,[0-9]+', desc )

        # 6557.10.18467
        #desc = re.sub( ' [0-9][0-9][0-9][0-9]\.[0-9][0-9]\.[0-9][0-9][0-9][0-9][0-9] ', r' % ', desc )
        #desc = re.sub( ' [0-9][0-9][0-9][0-9]\.[0-9][0-9]\.[0-9][0-9][0-9][0-9][0-9]$', r' %', desc )
        #desc = re.sub( '^[0-9][0-9][0-9][0-9]\.[0-9][0-9]\.[0-9][0-9][0-9][0-9][0-9] ', r'% ', desc )

        # Betalt: 01.01.12
        desc = re.sub( '[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]$', r'[0-9][0-9].[0-9][0-9].[0-9][0-9]', desc )
        desc = re.sub( ' [0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]$', r'[0-9][0-9].[0-9][0-9].[0-9][0-9]', desc )
        desc = re.sub( ' [0-9][0-9]\.[0-9][0-9]\.[0-9][0-9] ', r' [0-9][0-9].[0-9][0-9].[0-9][0-9] ', desc )

        desc = re.sub( ' [0-9][0-9][0-9][0-9][0-9] ', r' [0-9]+ ', desc )
        desc = re.sub( ' [0-9][0-9][0-9][0-9] ', r' [0-9]+ ', desc )
        desc = re.sub( ' [0-9][0-9][0-9] ', r' [0-9]+ ', desc )
        desc = re.sub( ' [0-9][0-9] ', r' [0-9]+ ', desc )
        desc = re.sub( ' [0-9] ', r' [0-9]+ ', desc )

        # 10022.0233
        desc = re.sub( ' [0-9][0-9][0-9][0-9][0-9]\.[0-9][0-9][0-9][0-9]$', r' [0-9]+.[0-9]+', desc )
        # 1000.0233
        desc = re.sub( ' [0-9][0-9][0-9][0-9]\.[0-9][0-9][0-9][0-9]$', r' [0-9]+.[0-9]+', desc )
        # 100.0233
        desc = re.sub( ' [0-9][0-9][0-9]\.[0-9][0-9][0-9][0-9]$', r' [0-9]+.[0-9]+', desc )
        # 86.9933
        desc = re.sub( ' [0-9][0-9]\.[0-9][0-9][0-9][0-9]$', r' [0-9]+.[0-9]+', desc )
        #1.0833
        desc = re.sub( ' [0-9]\.[0-9][0-9][0-9][0-9]$', r' [0-9]+.[0-9]+', desc )

        # 10022.022
        desc = re.sub( ' [0-9][0-9][0-9][0-9][0-9]\.[0-9][0-9][0-9]$', r' [0-9]+.[0-9]+', desc )
        # 1000.022
        desc = re.sub( ' [0-9][0-9][0-9][0-9]\.[0-9][0-9][0-9]$', r' [0-9]+.[0-9]+', desc )
        # 100.022
        desc = re.sub( ' [0-9][0-9][0-9]\.[0-9][0-9][0-9]$', r' [0-9]+.[0-9]+', desc )
        # 86.992
        desc = re.sub( ' [0-9][0-9]\.[0-9][0-9][0-9]$', r' [0-9]+.[0-9]+', desc )
        #1.082
        desc = re.sub( ' [0-9]\.[0-9][0-9][0-9]$', r' [0-9]+.[0-9]+', desc )

        # 10022.02
        desc = re.sub( ' [0-9][0-9][0-9][0-9][0-9].[0-9][0-9]$', r' [0-9]+.[0-9]+', desc )
        # 1000.02
        desc = re.sub( ' [0-9][0-9][0-9][0-9].[0-9][0-9]$', r' [0-9]+.[0-9]+', desc )
        # 100.02
        desc = re.sub( ' [0-9][0-9][0-9].[0-9][0-9]$', r' [0-9]+.[0-9]+', desc )
        # 86.99
        desc = re.sub( ' [0-9][0-9].[0-9][0-9]$', r' [0-9]+.[0-9]+', desc )
        #1.08
        desc = re.sub( ' [0-9].[0-9][0-9]$', r' [0-9]+.[0-9]+', desc )

        desc = re.sub( '^[0-9][0-9][0-9][0-9] ', r'[0-9]+ ', desc )
        desc = re.sub( ' [0-9][0-9][0-9][0-9][0-9]$', r' [0-9]+', desc )
        desc = re.sub( ' [0-9][0-9][0-9][0-9]$', r' [0-9]+', desc )
        desc = re.sub( ' [0-9][0-9][0-9]$', r' [0-9]+', desc )
        desc = re.sub( ' [0-9][0-9]$', r' [0-9]+', desc )
        desc = re.sub( ' [0-9]$', r' [0-9]+', desc )


        desc = re.sub( '\*', r'\\\*', desc )

        desc = desc.replace( 'STORMOA', '[[:alpha:]]*' )
        desc = desc.replace( 'STORM ', '[[:alpha:]]* ' )
        desc = desc.replace( ' MOAVN ', ' [[:alpha:]]* ' )
        desc = desc.replace( ' LANGELANDSVN ', ' [[:alpha:]]* ' )
        desc = desc.replace( ' LANGELANDSVE ', ' [[:alpha:]]* ' )
        desc = desc.replace( ' MOA SYD ', ' [[:alpha:]]* ' )


        desc = re.sub( '.LESUND', r'[[:space:]]*[[:alpha:]]*', desc )
        desc = re.sub( 'ALESUND', r'[[:alpha:]]*', desc )
        desc = re.sub( '.lesund', r'[[:space:]]*[[:alpha:]]*', desc )
        desc = re.sub( 'VATNE', r'[[:alpha:]]*', desc )
        desc = re.sub( 'Vatne', r'[[:alpha:]]*', desc )
        desc = re.sub( 'SKODJE', r'[[:alpha:]]*', desc )
        desc = re.sub( 'Skodje', r'[[:alpha:]]*', desc )
        desc = re.sub( 'S.VIK', r'[[:alpha:]]*', desc )
        desc = re.sub( 'S.vik', r'[[:alpha:]]*', desc )
        desc = re.sub( 'Sykkylven', r'[[:alpha:]]*', desc )
        desc = re.sub( 'SYKKYLVEN', r'[[:alpha:]]*', desc )
        desc = re.sub( 'BRATTV.G', r'[[:alpha:]]*', desc )
        desc = re.sub( 'Brattv.g', r'[[:alpha:]]*', desc )
        desc = re.sub( '.RSTA', r'[[:space:]]*[[:alpha:]]*', desc )
        desc = re.sub( '.rsta', r'[[:space:]]*[[:alpha:]]*', desc )


        desc = desc.replace( '.', '\.' )
        desc = " ".join( desc.split() )
        desc = desc.replace( ' ', '[[:space:]]*' )

        return "^" + desc + "$"

    """
    " @param (list)
    "
    " @return (float)
    """
    @staticmethod
    def getTotalAmount( list ):
        result = 0
        for i in list:
            result += i.attr( 'payment' )

        return abs( result )

    """
    " @param (list)
    "
    " @return (float)
    """
    @staticmethod
    def fetchPercentChargeList( userID, beginTS = None, endTS = None, limit = None ):
        l = Transaction.fetchChargeListByDates( userID, beginTS = beginTS, endTS = endTS, limit = limit )
        totalCharges = float( "{0:.2f}".format( Transaction.fetchTotalCharges( userID, beginTS, endTS ) ) )

        totalCount = len( l )
        handledDict = {}
        result = []
        for i in l:
            id = i.attr( 'id' )
            # It has been handled already, no need to check similar list anymore
            if id in handledDict:
                continue

            desc = i.attr( 'description' )
            tp = i.attr( 'payment' )
            handledDict[id] = i.attr( 'payment' )

            ll = i.fetchSimilarChargeList( level = 1, beginTS = beginTS, endTS = endTS )
            for ii in ll:
                iid = ii.attr( 'id' )
                # If similar transaction has been already handled previously for another transaction
                if iid in handledDict:
                    continue

                tp += ii.attr( 'payment' )
                handledDict[iid] = ii.attr( 'payment' )

            tp = abs( tp )
            # Means it is duplicate and there is no any need to handle it
            if tp == 0:
                continue

            percent = 100 * tp / totalCharges

            item = { 'id': i.attr( 'id' ),
                     'desc': desc,
                     'reg_exp': i.getDescriptionRegExp(),
                     'similar_count': len( ll ),
                     'total_count': totalCount,
                     'total_amount': totalCharges,
                     'amount': tp,
                     'percent': float( "{0:.2f}".format( percent ) ) }

            result.append( item )

        def cmpfunc( a, b ):
            if a['percent'] < b['percent']:
                return -1

            if a['percent'] > b['percent']:
                return 1

            return 0

        result.sort( cmp = cmpfunc )

        return result
