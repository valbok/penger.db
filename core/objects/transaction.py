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
            d = parse( d ).strftime('%s')
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
