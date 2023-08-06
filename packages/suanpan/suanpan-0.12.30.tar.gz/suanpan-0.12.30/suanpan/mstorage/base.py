# coding=utf-8
from __future__ import absolute_import, print_function

import abc

from suanpan.mstorage.vars import Float, Int, Json, String
from suanpan.objects import HasName


class MStorage(HasName):
    @abc.abstractmethod
    def get(self, name, *args, **kwargs):
        pass

    @abc.abstractmethod
    def set(self, name, value, *args, **kwargs):
        pass

    @abc.abstractmethod
    def mget(self, name, *args, **kwargs):
        pass

    @abc.abstractmethod
    def mset(self, name, mapping, *args, **kwargs):
        pass

    def Int(self, key):
        return Int(self, key)

    def Float(self, key):
        return Float(self, key)

    def String(self, key):
        return String(self, key)

    def Json(self, key):
        return Json(self, key)
