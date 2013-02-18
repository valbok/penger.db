"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

from csvimport import *
from ..transaction import *

"""
" Custom implementation of import from SCANDIA:BANKEN bank
"""
class Scandia( CsvImport ):

    """
    " @return (list) List of processed objects
    " @note Transaction unsafe
    """
    def process( self, userID ):
        first = True
        result = []
        i = 0
        for r in self.transactions:
            i = i + 1
            if i <= 3:
                continue

            if len( r ) == 0:
                break

            try:
                c = float( r[5].replace( ",", "." ) )
            except ValueError:
                c = 0

            try:
                d = float( r[6].replace( ",", "." ) )
            except ValueError:
                d = 0;

            p = 0 - c if c > 0 else d
            t = Transaction( { 'user_id': userID, 'date': r[0], 'description': r[4], 'payment': str( p ) } )
            if t.exists():
                continue

            t.insert()
            result.append( t )

        return result
