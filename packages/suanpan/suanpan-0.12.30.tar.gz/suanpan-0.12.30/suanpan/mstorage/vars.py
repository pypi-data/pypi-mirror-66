# coding=utf-8
from __future__ import absolute_import, print_function

from suanpan.utils import json


class Variable(object):
    def __init__(self, mstorage, key):
        self.mstorage = mstorage
        self.key = key
        self._value = None

    @property
    def value(self):
        if self._value is None:
            self._value = self.get()
        return self._value

    def get(self):
        self._value = self.decode(self.mstorage.get(self.key))
        return self._value

    def set(self, value):
        self._value = value
        self.mstorage.set(self.key, self.encode(self._value))

    def delete(self):
        self.mstorage.delete(self.key)

    @classmethod
    def encode(cls, value):
        return value

    @classmethod
    def decode(cls, value):
        return value


class String(Variable):
    pass


class Int(Variable):
    @classmethod
    def encode(cls, value):
        return str(value)

    @classmethod
    def decode(cls, value):
        return int(value)


class Float(Variable):
    @classmethod
    def encode(cls, value):
        return str(value)

    @classmethod
    def decode(cls, value):
        return float(value)


class Json(Variable):
    @classmethod
    def encode(cls, value):
        return json.dumps(value)

    @classmethod
    def decode(cls, value):
        return json.loads(value)
