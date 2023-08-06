#!/usr/bin/env python
"""
Tracer of the activity on a given object.
"""

__author__ = 'Sylvain Roy <sylvain DOT roy AT m4x DOT org>'
__date__ = '15 Aug 2014'

import types
from sys import stdout


def instrument_method(method_name, method, name, stream):
        def imethod(self, *args, **kwargs):
                parameters = ", ".join(map(repr, list(args)))
                parameters += ", ".join(map(lambda i: '{}={}'.format(str(i[0]), repr(i[1])),
                                                                        kwargs.items()))
                indent = '  '*self._objectTracerAttributes['depth']
                print('{}> {}.{}({})'.format(indent, name, method_name, parameters), file=stream)
                self._objectTracerAttributes['depth'] += 1
                res = method(self, *args, **kwargs)
                self._objectTracerAttributes['depth'] -= 1
                print('{}< {}'.format(indent, repr(res)), file=stream)
                return res
        imethod.func_name = method_name
        return imethod


def build_xxxattr_methods(name, stream):
        def __getattribute__(self, att):
                val = object.__getattribute__(self, att)
                if type(val) == types.MethodType or att == '_objectTracerAttributes':
                        return val
                indent = '  '*object.__getattribute__(self, '_objectTracerAttributes')['depth']
                print("{}{}.{} > {}".format(indent, name, att, repr(val)), file=stream)
                return val
        def __setattr__(self, att, val):
                ret = object.__setattr__(self, att, val)
                if att == '__class__':
                        return
                indent = '  '*object.__getattribute__(self, '_objectTracerAttributes')['depth']
                print("{}{}.{} < {}".format(indent, name, att, repr(val)), file=stream)
        def __delattr__(self, att):
                val = object.__delattr__(self, att)
                indent = '  '*object.__getattribute__(self, '_objectTracerAttributes')['depth']
                print("{}del({}.{})".format(indent, name, att), file=stream)
        return {'__getattribute__': __getattribute__, '__setattr__': __setattr__, '__delattr__': __delattr__}


def instrument(obj, name="self", stream=stdout):
        """Instrument 'obj' to have all its interaction logged on 'stream'."""
        # Retrieve all methods of obj
        methods = {m[0]: m[1]
                           for m in obj.__class__.__dict__.items()
                           if type(m[1]) == types.FunctionType}
        # Create new instrumented version to trace method calls
        newmethods = {m[0]: instrument_method(m[0], m[1], name, stream) for m in methods.items()}
        # Adds xxxAttr methods to trace attributes access
        newmethods.update(build_xxxattr_methods(name, stream))
        # Add some temporary attributes to the objects
        obj._objectTracerAttributes = {'depth': 0, 'class': obj.__class__}
        # Replace obj class by a new instrumented version
        obj.__class__ = type('Instrumented-'+str(obj.__class__), (object,), newmethods)


def clean(obj):
        """Remove all instrumentation set-up by 'instrument'"""
        # Reinit class
        obj.__class__ = obj._objectTracerAttributes['class']
        # Remove tempo attributes
        del(obj._objectTracerAttributes)
