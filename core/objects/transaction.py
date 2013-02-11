"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

from ..lib import *

"""
" One transaction payment
"""
class Transaction( PersistentObject ):
    _definition = Definition( table = "transaction", keys = [ "id" ], incrementField = "id" )
