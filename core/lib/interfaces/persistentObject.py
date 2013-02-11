"""
" @author VaL
" @copyright Copyright (C) 2013 VaL::bOK
" @license GNU GPL v2
"""

from abc import ABCMeta, abstractmethod, abstractproperty
import zope.interface

class IPersistentObject( zope.interface.Interface ):
    _fieldList = zope.interface.Attribute( """Field List""" )
    _definition = zope.interface.Attribute( """DB Definition""" )

    def getAttribute():
        pass

    def setAttribute():
        pass

    def insert():
        pass

    def update():
        pass

    def attr():
        pass
