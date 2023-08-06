"""Library for logical formulas.

Python library for building and working with propositional
formulas.
"""

from __future__ import annotations
from itertools import product
import doctest

class wff(dict):
    """
    Data structure for a logical formula.
    
    >>> wff.zero().evaluate()
    0
    >>> wff.one().evaluate()
    1
    >>> wff.zero() & wff.one()
    {(0, 0, 0, 1): [{(0,): []}, {(1,): []}]}
    >>> f = wff.zero() & wff.one()
    >>> f.evaluate()
    0
    >>> f = wff.var('x') & wff.one()
    >>> f.evaluate({'x':1})
    1
    >>> f = wff.var('x') | wff.var('y')
    >>> sorted(list(f.vars()))
    ['x', 'y']
    >>> f = (wff.var('x') | wff.var('y')) @ wff.one()
    >>> f.operations()
    {(1, 1, 1, 0), (0, 1, 1, 1), (1,)}
    >>> f.table()
    (1, 0, 0, 0)
    """

    @staticmethod
    def zero():
        return wff({(0,):[]})

    @staticmethod
    def one():
        return wff({(1,):[]})

    @staticmethod
    def var(key):
        return wff({key: []})

    @staticmethod
    def op(operation):
        return lambda *fs: wff({operation: fs})

    def __and__(self: wff, other: wff) -> wff:
        return wff({(0,0,0,1): [self, other]})

    def __gt__(self: wff, other: wff) -> wff:
        return wff({(0,0,1,0): [self, other]})

    def __lshift__(self: wff, other: wff) -> wff:
        return wff({(0,0,1,1): [self, other]})

    def __lt__(self: wff, other: wff) -> wff:
        return wff({(0,1,0,0): [self, other]})

    def __rshift__(self: wff, other: wff) -> wff:
        return wff({(0,1,0,1): [self, other]})

    def __xor__(self: wff, other: wff) -> wff:
        return wff({(0,1,1,0): [self, other]})

    def __or__(self: wff, other: wff) -> wff:
        return wff({(0,1,1,1): [self, other]})

    def __mod__(self: wff, other: wff) -> wff:
        return wff({(1,0,0,0): [self, other]})

    def __eq__(self: wff, other: wff) -> wff:
        return wff({(1,0,0,1): [self, other]})

    def __floordiv__(self: wff, other: wff) -> wff:
        return wff({(1,0,1,0): [self, other]})

    def __ge__(self: wff, other: wff) -> wff:
        return wff({(1,0,1,1): [self, other]})

    def __truediv__(self: wff, other: wff) -> wff:
        return wff({(1,1,0,0): [self, other]})

    def __le__(self: wff, other: wff) -> wff:
        return wff({(1,1,0,1): [self, other]})

    def __matmul__(self: wff, other: wff) -> wff:
        return wff({(1,1,1,0): [self, other]})

    def vars(self: wff) -> set:
        '''
        Collect the set of all variables in a formula.
        '''
        key = list(self.keys())[0]
        if not isinstance(key, tuple):
            return set([key])
        else:
            return set([x for f in self[key] for x in f.vars()])

    def operations(self: wff) -> set:
        '''
        Collect the set of all operations in a formula.
        '''
        key = list(self.keys())[0]
        if not isinstance(key, tuple):
            return set()
        else:
            return set([key]).union(set(o for f in self[key] for o in f.operations()))

    def embedded(self: wff, var = None) -> str:
        '''
        Build a string representation that is a valid Python
        expression (i.e.,  it can be evaluated using `eval()`).
        '''
        # Default embedding functions for base cases.
        if var is None:
            var = lambda key: "var(" + str(key) + ")"
        infix = {
            (0,0,0,1): '&',
            (0,0,1,0): '>',
            (0,1,0,0): '<',
            (0,1,1,0): '^',
            (0,1,1,1): '|',
            (1,0,0,0): '%',
            (1,0,0,1): '==',
            (1,0,1,1): '>=',
            (1,1,0,1): '<=',
            (1,1,1,0): '@'
        }

        # Build the embedding.
        key = list(self.keys())[0]
        if isinstance(key, tuple) and len(key) == 4:
            return "(" +\
                self[key][0].embedded(var = var) +\
                " " + infix[key] + " " +\
                self[key][1].embedded(var = var) +\
            ")"
        else:
            return var(key)

    def evaluate(self: wff, env = None):
        '''
        Evaluate a formula to obtain a value.
        '''
        key = list(self.keys())[0]
        if isinstance(key, tuple): # Key is an operation's output column.
            operation = key
            if len(operation) == 1:
                return operation[0]
            elif len(operation) == 4:
                vs = tuple(f.evaluate(env) for f in list(self.values())[0])
                return operation[list(product(*[[0,1]]*2)).index(vs)]
        else: # Key is an index into the environment (of any type).
            return env[key]

    def table(self: wff) -> tuple:
        '''
        Build the output column of a truth table for the formula.
        '''
        xs = self.vars()
        envs = [dict(zip(xs,vs)) for vs in product(*[[0,1]]*len(xs))]
        return tuple(self.evaluate(env) for env in envs)

# Useful synonyms.
zero = wff.zero()
one = wff.one()
var = wff.var
op = wff.op

if __name__ == "__main__":
    doctest.testmod()
