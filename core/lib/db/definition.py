"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

class Definition( object ):
    def __init__( self, table, keys, incrementField = None ):
        self._table = table
        self._keys = keys
        self._incrementField = incrementField

    @property
    def table( self ):
        return self._table

    @property
    def keys( self ):
        return self._keys

    @property
    def incrementField( self ):
        return self._incrementField
