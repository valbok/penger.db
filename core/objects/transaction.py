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
        v = str( self.attr( 'date' ) ) + str( self.attr( 'debit' ) ) + str( self.attr( 'credit' ) ) + self.attr( 'description' ) + str( self.attr( 'user_id' ) )

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
    def fetchList( where = None, limit = None, offset = None, orderByDict = { "date": DB.ASC } ):
        t = Transaction()

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
    def fetchDateCreditList( beginTS = None, endTS = None ):
        result = {}
        dTable = Transaction()._definition.table

        where = None
        if beginTS != None:
            where = " date >= " + str( beginTS )

        if endTS != None:
            where = " date <= " + str( endTS ) if where == None else where + " AND date <= " + str( endTS )

        if where != None:
            where = "WHERE " + where

        sql = "SELECT date, sum( credit ) as result FROM {} {} GROUP BY date ORDER BY date ASC".format( dTable, where )
        print sql
        db = DB.get()
        cur = db.cursor()
        cur.execute( sql )
        rows = cur.fetchall()
        for i in rows:
            result[i[0]] = i[1]

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
    def fetchDateDebitList( beginTS = None, endTS = None ):
        result = {}
        dTable = Transaction()._definition.table

        where = None
        if beginTS != None:
            where = " date >= " + str( beginTS )

        if endTS != None:
            where = " date <= " + str( endTS ) if where == None else where + " AND date <= " + str( endTS )

        if where != None:
            where = "WHERE " + where

        sql = "SELECT date, sum( debit ) as result FROM {} {} GROUP BY date ORDER BY date ASC".format( dTable, where )
        print sql
        db = DB.get()
        cur = db.cursor()
        cur.execute( sql )
        rows = cur.fetchall()
        for i in rows:
            result[i[0]] = i[1]

        return result
