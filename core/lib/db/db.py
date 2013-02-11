"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

import MySQLdb

class DB( object ):
    _instance = None
    def __init__( self, db ):
        self._db = db

    @property
    def db( self ):
        return self._db

    @staticmethod
    def init( host = "localhost", user = "root", passwd = "", db = "" ):
        DB._instance = DB( MySQLdb.connect( host, user, passwd, db ) )

        return DB._instance

    @staticmethod
    def get():
        return DB._instance.db;

    @staticmethod
    def uninit():
        DB._instance = None
