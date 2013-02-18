"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

import copy
from interfaces import *
from db import *
import zope.interface
import MySQLdb
import re

"""
" Abstract and base object.
" Should not be instantiated directly.
" Implements basic functionality to fetch and store data to DB using db module.
"""
class PersistentObject( object ):
    zope.interface.implements( IPersistentObject )

    """
    " @param (dict) Dictionary of fields. Key - field name, Value - field's value
    """
    def __init__( self, list = {} ):
        self._fieldList = list

    """
    " Clears any assigned fields
    "
    " @return (self)
    """
    def _clear( self ):
       self._fieldList = {}

       return self

    """
    " Main point to fetch data from database.
    "
    " @param (string) where String condition
    " @return (list) List of instances of needed classes
    """
    def fetchObjectList( self, where = None, limit = None, offset = None, orderByDict = None ):
        dTable = self._definition.table
        dKeys = self._definition.keys
        dInc = self._definition.incrementField
        sql = "SELECT * FROM {}".format( dTable )
        if where != None and len( where ) > 0:
            sql += " WHERE " + where

        if orderByDict != None:
            s = ", ".join( [ '%s %s' % ( k, v ) for ( k, v ) in orderByDict.items() ] )
            sql += " ORDER BY " + s

        if limit != None:
            ls = " LIMIT "
            limit = str( limit )
            offset = str( offset ) if offset != None else None
            lss = ls + limit if offset == None else ls + offset + ", " + limit
            sql += lss

        db = DB.get()
        cur = db.cursor()
        cur.execute( sql )
        rows = cur.fetchall()
        fieldNames = [i[0] for i in cur.description]
        result = []
        for o in rows:
            c = copy.copy( self )
            c._clear()
            for i in xrange( len( o ) ):
                v = o[i]
                n = fieldNames[i]
                c.attr( n, v )

            result.append( c )

        return result

    """
    " Wrapper to fetch only one object by condition
    "
    " @return (__CLASS__) An innstance of needed class
    """
    def fetchObject( self, where = None ):
        l = self.fetchObjectList( where, limit = 1 )

        return l[0] if len( l ) > 0 else None

    """
    " Wrapper to fetch only one object by increment field
    "
    " @return (__CLASS__) An innstance of needed class
    """
    def _fetchObjectByIncrementField( self, v ):
        where = self._getIncrementField() + '="' + re.escape( str( v ) ) + '"'

        return self.fetchObject( where )

    """
    " Returns incement field if exists
    "
    " @return (str)
    """
    def _getIncrementField( self ):
        return self._definition.incrementField

    """
    " @implements( IPersistentObject )
    """
    def getAttribute( self, name ):
        try:
            v = self._fieldList[name]
        except KeyError, e:
            v = None;

        return v;

    """
    " @implements( IPersistentObject )
    """
    def setAttribute( self, name, value ):
        self._fieldList[name] = value

        return self;

    """
    " @implements( IPersistentObject )
    """
    def attr( self, name, value = None ):
        return self.setAttribute( name, value ) if value else self.getAttribute( name )

    """
    " @implements( IPersistentObject )
    " @note Transaction unsafe
    """
    def insert( self ):
        dTable = self._definition.table
        dKeys = self._definition.keys
        dInc = self._definition.incrementField
        fieldList = dict( self._fieldList )

        if not fieldList:
            return self

        db = DB.get()
        cur = db.cursor()

        try:
            del fieldList[dInc]
        except KeyError:
            pass # Means no attribute provided

        kList = fieldList.keys()
        fields = ", ".join( kList )

        values = ", ".join( [ '"%s"' % ( v ) for ( k, v ) in fieldList.items() ] )
        sql = "INSERT INTO {} ({}) VALUES ({})".format( dTable, fields, values )
        cur.execute( sql )
        lastid = cur.lastrowid
        if dInc and lastid:
            self.setAttribute( dInc, lastid )
        cur.close()

        return self

    """
    " @implements( IPersistentObject )
    " @note Transaction unsafe
    """
    def update( self ):
        dTable = self._definition.table
        dKeys = self._definition.keys
        dInc = self._definition.incrementField
        fieldList = dict( self._fieldList )
        if not fieldList:
            return self

        db = DB.get()
        cur = db.cursor()

        kList = fieldList.keys()
        values = ", ".join( [ '%s="%s"' % ( k, v ) for ( k, v ) in fieldList.items() ] )
        where = ""
        for k in dKeys:
            where += k + "=\"" + re.escape( str( fieldList[k] ) ) + "\""

        sql = "UPDATE {} SET {} WHERE {}".format( dTable, values, where )
        cur.execute( sql )
        cur.close()

    """
    " Returns WHERE condition to check if current object exists in table
    "
    " @return (bool)
    """
    def _getExistCondition( self ):
        dKeys = self._definition.keys
        fieldList = dict( self._fieldList )
        where = []

        for k in dKeys:
            try:
                v = fieldList[k]
            except KeyError:
                continue

            where.append( k + "=\"" + re.escape( str( fieldList[k] ) ) + "\"" )

        return " AND ".join( where ) if len( where ) else ""

    """
    " Checks if current object has been stored
    "
    " @return (bool)
    """
    def exists( self ):
        w = self._getExistCondition()
        if not len( w ):
            return False

        o = self.fetchObject( w )
        return bool( o )

    """
    " Wrapper to check if value is int
    "
    " @return (bool)
    """
    @staticmethod
    def _isInt( value ):
        if value == None:
            return False

        try:
            int( value )
            return True
        except ValueError:
            return False

    """
    " Checks if data has been assigned
    "
    " @return (bool)
    """
    def hasFields( self ):
        return bool( len( self._fieldList ) )
