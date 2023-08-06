#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2017 David Toro <davsamirtor@gmail.com>

# compatibility with python 2 and 3
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# import build-in modules
from collections import OrderedDict, MutableMapping

# special variables
# __all__ = []
__author__ = "David Toro"
# __copyright__ = "Copyright 2017, The <name> Project"
# __credits__ = [""]
__license__ = "GPL"
# __version__ = "1.0.0"
__maintainer__ = "David Toro"
__email__ = "davsamirtor@gmail.com"
# __status__ = "Pre-release"


class References(MutableMapping):
    """
    Dictionary to keep aliases solving internal references 
    and calling functions. Circular references are not checked since
    it is inefficient and they can happen at runtime when evaluating 
    callable references.

    Example::

        # dictionary like functions
        aliases = References(
            {"this": "References Class",  # "this" is reference of "References Class"
             "me": "this",  # "me" is reference of "this" which reference "References Class"
             "number 2": 2,  # "number 2" references 2
             2: "2"})  # 2 references "2", now "number 2" references 2 too
        assert(aliases["this"] == "References Class")
        aliases["solve"] = lambda: aliases["me"] + " solves references"
        assert(aliases["solve"] == 'References Class solves references')

        # using advance function
        assert(aliases.filter_type("number 2") == '2')
        assert(aliases.filter_type("number 2", int) == 2)
        assert(aliases.filter_type("number 2", str) == '2')
        aliases.filter_type("me", int, True)  # TypeError

        # prevent circular references like
        key = "References Class"
        aliases[key] = "this"
        try:
            aliases[key]
        except RecursionError:
            del aliases[key]
            raise(KeyError("key '{}' have circular references".format(key)))
    """

    def __init__(self, *args, **kwargs):
        """
        dict() -> new empty dictionary
        dict(mapping) -> new dictionary initialized from a mapping object's
            (key, value) pairs
        dict(iterable) -> new dictionary initialized as if via:
            d = {}
            for k, v in iterable:
                d[k] = v
        dict(**kwargs) -> new dictionary initialized with the name=value pairs
            in the keyword argument list.  For example:  dict(one=1, two=2)
        # (copied from class doc)
        """
        assert (len(args) <= 1)
        self._map = {}
        try:
            for k, v in args[0].items():
                self[k] = v
        except AttributeError:
            for k, v in args[0]:
                self[k] = v
        for k, v in kwargs.items():
            self[k] = v

    def __getitem__(self, item):
        # solve references
        return self.filter_type(item)

    def __setitem__(self, key, value):
        self._map[key] = value

    def __delitem__(self, key):
        del self._map[key]

    def filter_type(self, item, type=None, strict=False):
        """
        get item's alias of the same filtered type

        :param item: alias or reference to find
        :param type: type to return in alias references
        :param strict: raise error if type in not found among aliases else 
            return found alias even if the desired type does not match
        :return: item alias
        """
        value = self._map[item]
        if callable(value):
            value = value()
        if type is not None and isinstance(value, type):
            return value

        try:
            return self.filter_type(value, type, strict)
        except (KeyError, TypeError):
            # catch a key not found, an unhashable object or if type
            # was not found (this is re-raised later with proper message)
            pass

        if strict and type is not None and not isinstance(value, type):
            raise TypeError("type '{}' not found in references for '{}' "
                            "key".format(type, item))
        return value

    def __iter__(self):
        return iter(self._map)

    def __len__(self):
        return len(self._map)


class Aliases(MutableMapping):
    """
    Dictionary to keep aliases to te first inserted alias
    and calling functions. This does not creates deadlocks as referencing
    the first alias gives itself.

    Example::

        # dictionary like functions:
        # the order of aliases are important so it is not recommended to use
        # a dictionary since it reoganize the keys and values
        aliases = Aliases(
            [("this", "Aliases Class"),  # "this" is alias of "Aliases Class"
             ("me", "this"),  # "me" is alias of "this"
             ("number 2", 2),  # 2 is the first alias and "number 2" ist alias
             (2, "2")]  # 2 and "2" now are aliases
        )
        assert(aliases["this"] == "Alias Class")
        aliases["solve"] = lambda: aliases["me"] + " solves references"
        assert(aliases["solve"] == 'Alias Class solves references')

        # using advance function
        # here 2 is key and "2" is value, but remeber both are aliases
        # and the first alias was 2 
        assert(aliases.filter_type("2") == 2)
        assert(aliases.filter_type("number 2") == 2)
        assert(aliases.filter_type("number 2", int) == 2)
        # "number 2" is a key but it is an alias of 2 so it is searchable
        assert(aliases.filter_type("number 2", str) == 'number 2')
        # because we asked for a str it returns 'number 2' 
        # instead of the first alias 2
        assert(aliases.filter_type("2", str) == 'number 2')
        aliases.filter_type("me", int, True)  # TypeError
    """

    def __init__(self, *args, **kwargs):
        """
        dict() -> new empty dictionary
        dict(mapping) -> new dictionary initialized from a mapping object's
            (key, value) pairs
        dict(iterable) -> new dictionary initialized as if via:
            d = {}
            for k, v in iterable:
                d[k] = v
        dict(**kwargs) -> new dictionary initialized with the name=value pairs
            in the keyword argument list.  For example:  dict(one=1, two=2)
        # (copied from class doc)
        """
        assert (len(args) <= 1)
        self._map = {}
        try:
            for k, v in args[0].items():
                self[k] = v
        except AttributeError:
            for k, v in args[0]:
                self[k] = v
        for k, v in kwargs.items():
            self[k] = v

    def __getitem__(self, item):
        # solve aliases
        return self.filter_type(item)

    def __setitem__(self, key, value):
        # value has priority over key
        # main_set = OrderedSet([value, key])  # http://code.activestate.com/recipes/576694/
        main_set = OrderedDict([(value, None), (key, None)])
        try:
            # get set from key
            my_set = self._map[key]
            my_set.update(main_set)
            main_set = my_set
        except KeyError:
            # if value of key exits get ist set
            try:
                my_set = self._map[value]
                my_set.update(main_set)
                self._map[key] = my_set
                return
            except KeyError:
                # set set of key
                self._map[key] = main_set

        # here main_set is the same from key
        try:
            my_set = self._map[value]
            if main_set is not my_set:
                main_set.update(my_set)
                self._map[value] = main_set
        except KeyError:
            self._map[value] = main_set

    def __delitem__(self, key):
        my_set = self._map[key]
        del my_set[key]  # my_set.remove(key)
        del self._map[key]

    def filter_type(self, item, type=None, strict=False):
        """
        get item's alias of the same filtered type

        :param item: alias or reference to find
        :param type: type to return in alias references
        :param strict: raise error if type in not found among aliases else 
            return found alias even if the desired type does not match
        :return: item alias
        """
        values = self._map[item]
        value = None
        flag = False
        for value in values:
            if callable(value):
                value = value()
                if value != item:  # prevent recursions
                    try:
                        return self.filter_type(value, type, strict)
                    except (KeyError, TypeError):
                        # catch a key not found, an unhashable object or if type
                        # was not found (this is re-raised later with proper message)
                        pass

            if type is None:
                return value
            elif isinstance(value, type):
                return value

            flag = True

        if strict:  # type not found
            raise TypeError("type '{}' not found in references for '{}' "
                            "key".format(type, item))
        if flag:
            return value
        else:
            raise KeyError(item)

    def __iter__(self):
        return iter(self._map)

    def __len__(self):
        return len(self._map)