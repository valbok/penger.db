"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

import csv
import abc

"""
" Abstract class to import data in CSV to current implementation
"""
class CsvImport( object ):
    __metaclass__ = abc.ABCMeta

    """
    " @param (str) Path to file where data in csv is located
    " @param (str)
    """
    def __init__( self, path, delimiter = "\t" ):
        self._path = path
        f = open( path )
        self._transactions = csv.reader( f, delimiter = delimiter )

    @property
    def transactions( self ):
        return self._transactions

    """
    " Processes actual import
    """
    @abc.abstractmethod
    def process( self ):
        raise Exception( 'Not allowed to use abstract method' )
