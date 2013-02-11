"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

import MySQLdb
import unittest
from core import *

class IncrementTable( PersistentObject ):
    _definition = Definition( table = "increment_table", keys = [ "id" ], incrementField = "id" )

    @staticmethod
    def fetch( id ):
        o = IncrementTable()
        return o.fetchObject( "id = " + str( id ) )


class NotIncrementTable( PersistentObject ):
    _definition = Definition( table = "not_increment_table", keys = [ "hash" ] )

class PersistentObjectTest( unittest.TestCase ):

    def setUpDB( self ):
        DB.init( db = "" )
        db = DB.get()
        db.begin()
        cur = db.cursor()
        cur.execute( "DROP DATABASE IF EXISTS penger_db_test " )
        cur.execute( "CREATE DATABASE penger_db_test" )
        cur.execute( "USE penger_db_test" )
        cur.execute( "CREATE TABLE increment_table ( id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, title TEXT NOT NULL )")
        cur.execute( "CREATE TABLE not_increment_table ( hash varchar(255) default NULL, title TEXT NOT NULL )")
        db.commit()

    def testEmptyInit( self ):
        s = IncrementTable()

    def testInit( self ):
        s = IncrementTable( { "field1" : "value1", "field2" : "value2" } )
        self.assertEquals( "value1", s.getAttribute( "field1" ) )
        self.assertEquals( "value2", s.getAttribute( "field2" ) )
        self.assertEquals( None, s.getAttribute( "fieldUnknown" ) )

    def testSetAttribute( self ):
        s = IncrementTable()
        s.setAttribute( "field1", "value1" ).setAttribute( "field2", "value2" )
        self.assertEquals( "value1", s.getAttribute( "field1" ) )
        self.assertEquals( "value2", s.getAttribute( "field2" ) )
        self.assertEquals( None, s.getAttribute( "fieldUnknown" ) )

    def testAttr( self ):
        s = IncrementTable()
        s.attr( "field1", "value1" ).attr( "field2", "value2" )
        self.assertEquals( "value1", s.attr( "field1" ) )
        self.assertEquals( "value2", s.attr( "field2" ) )
        self.assertEquals( None, s.attr( "fieldUnknown" ) )

    def testInsertIncrement( self ):
        self.setUpDB()
        db = DB.get()
        s = IncrementTable( { "title": "test" } )
        self.assertEquals( None, s.getAttribute( "id" ) )
        db.begin()
        s.insert()
        db.commit()
        self.assertEquals( 1, s.getAttribute( "id" ) )


    def testInsertNotIncrement( self ):
        self.setUpDB()
        s = NotIncrementTable( { "hash": "hash", "title": "test" } )
        s.insert();
        self.assertEquals( "hash", s.getAttribute( "hash" ) )

    def testFetchObjectListIncrement( self ):
        self.setUpDB()
        s = IncrementTable( { "title": "test" } )
        db = DB.get()
        db.begin()
        s.insert()
        db.commit()
        l = s.fetchObjectList()
        self.assertEquals( 1, len( l ) )
        o = l[0]
        self.assertEquals( True, isinstance( o, IncrementTable ) )
        self.assertEquals( "test", o.attr( "title" ) )

    def testFetchObjectListIncrementWhere( self ):
        self.setUpDB()
        db = DB.get()
        s = IncrementTable( { "title": "test2" } )

        db.begin()
        s = IncrementTable( { "title": "test" } )
        s.insert()
        s = IncrementTable( { "title": "test2" } )
        s.insert()
        db.commit()

        l = s.fetchObjectList( )
        self.assertEquals( 2, len( l ) )

        l = s.fetchObjectList( "id = 2" )
        self.assertEquals( 1, len( l ) )
        o = l[0]
        self.assertEquals( True, isinstance( o, IncrementTable ) )
        self.assertEquals( "test2", o.attr( "title" ) )


    def testFetchObjectListIncrementLimit( self ):
        self.setUpDB()
        db = DB.get()
        s = IncrementTable()
        db.begin()
        s = IncrementTable( { "title": "test" } )
        s.insert()
        s = IncrementTable( { "title": "test2" } )
        s.insert()
        db.commit()

        l = s.fetchObjectList()
        self.assertEquals( 2, len( l ) )

        l = s.fetchObjectList( limit = 1 )
        self.assertEquals( 1, len( l ) )
        o = l[0]
        self.assertEquals( "test", o.attr( "title" ) )

        l = s.fetchObjectList( limit = 1, offset = 1 )
        self.assertEquals( 1, len( l ) )
        o = l[0]
        self.assertEquals( "test2", o.attr( "title" ) )

        o = s.fetch( "1" )
        self.assertEquals( "test", o.attr( "title" ) )

        o = s.fetch( 2 )
        self.assertEquals( "test2", o.attr( "title" ) )

if __name__ == '__main__':
    unittest.main()
