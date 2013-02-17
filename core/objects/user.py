"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

from ..lib import *

"""
" User object
"""
class User( PersistentObject ):
    _definition = Definition( table = "user", keys = [ "id" ], incrementField = "id" )

    """
    " Fetches object by id
    "
    " @return (__CLASS__)
    """
    @staticmethod
    def fetch( id ):
        o = User()

        return o._fetchObjectByIncrementField( id )
