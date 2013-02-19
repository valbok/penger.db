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
        t = Transaction()
        if where == None:
            where = "user_id = '" + str( int( userID ) ) + "'"
        else:
            where = "user_id = '" + str( int( userID ) ) + "' AND " + where

        return t.fetchObjectList( where = where, limit = limit, offset = offset, orderByDict = orderByDict )

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
        result = {}
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
        result = {}
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
        result = {}
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
