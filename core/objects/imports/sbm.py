"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

from csvimport import *
from ..transaction import *

"""
" Custom implementation of import from SBM bank
"""
class Sbm( CsvImport ):

    """
    " @return (list) List of processed objects
    " @note Transaction unsafe
    """
    def process( self, userID ):
        first = True
        result = []

        for r in self.transactions:
            if first:
                first = False
                continue

            try:
                c = float( r[2].replace( ",", "." ) )
            except ValueError:
                c = 0

            try:
                d = float( r[3].replace( ",", "." ) )
            except ValueError:
                d = 0;

            date = r[0] # dd.mm.yyyy
            edate = date.split( "." )
            if len( edate ) > 1:
                date = edate[2] + "-" + edate[1] + "-" + edate[0]

            t = Transaction( { 'user_id': userID, 'date': date, 'description': r[1], 'credit': str( c ), 'debit': str( d ) } )
            if t.exists():
                continue

            t.insert()
            result.append( t )

        return result
