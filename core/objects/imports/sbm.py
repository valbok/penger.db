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
    def process( self, userID, unique = True ):
        first = True
        result = []

        for r in self.transactions:
            if first:
                first = False
                continue

            b = r[4]
            try:
                b = float( b.replace( ",", "." ) )
            except ValueError:
                b = 0

            date = r[0] # dd.mm.yyyy
            edate = date.split( "." )
            if len( edate ) > 1:
                date = edate[2] + "-" + edate[1] + "-" + edate[0] # yyyy-mm-dd

            desc = r[3]

            t = Transaction( { 'user_id': userID, 'date': date, 'description': desc, 'payment': str( b ) } )
            if unique and t.exists():
                continue

            t.insert()
            result.append( t )

        return result
