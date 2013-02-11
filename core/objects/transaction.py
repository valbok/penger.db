"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

from ..lib import *

class Transaction( PersistentObject ):
    _definition = Definition( table = "transaction", keys = [ "id" ], incrementField = "id" )
