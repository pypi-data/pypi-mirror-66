"""
Copyright 2020 Pauli Henrikki Rikula

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from typing import List
from enum import Enum, auto
import abc
from collections import defaultdict

class MaxMin(Enum):
    MAX = 1
    MIN = 2
    SKIP = 3

    def __repr__(self) -> str:
        return self.name

class MaxMinList:
    def __init__(self, *target_list: List[MaxMin], none_is_good=False):
        """
        >>> MaxMinList(MaxMin.MAX, MaxMin.MIN)
        MaxMinList[MAX ,MIN]
        """
        self._target_list = target_list
        self._dim = len(target_list)
        self._none_is_good = none_is_good

    def __repr__(self) -> str:
        return "MaxMinList[{}]".format(" ,".join([i.__repr__() for i in self._target_list]))
    
    @property
    def dim(self) -> int: return self._dim

    @property
    def list(self) -> List[MaxMin]:
        return self._target_list
    
    @property
    def none_is_good(self):
        return self._none_is_good

class Domination(Enum):
    GREATER = 1
    EQUAL = 0
    LESS = -1
    
    def __repr__(self) -> str:
        return self.name

def by_none(a, b) -> Domination:
    """
    >>> by_none(None, 1)
    GREATER
    >>> by_none(1, None)
    LESS
    >>> by_none(None, None)
    EQUAL
    >>> by_none(1, 1)
    EQUAL
    
    """
    if a is None and b is not None:
        return Domination.GREATER
    if b is None and a is not None:
        return Domination.LESS
    return  Domination.EQUAL

def by_value(a, b) -> Domination:
    """
    >>> by_value(2, 1)
    GREATER
    >>> by_value(1, 2)
    LESS
    >>> by_value(2, 2)
    EQUAL
    >>> by_value(1, 1)
    EQUAL
    
    """
    if a > b:
        return Domination.GREATER
    if a < b:
        return Domination.LESS
    return  Domination.EQUAL

def cmp_to_target(a, b, cmp, target: MaxMin, none_is_good) -> Domination:
    """
    >>> cmp_to_target(2, 1, by_value, MaxMin.MAX, False)
    GREATER
    >>> cmp_to_target(1, 2, by_value, MaxMin.MAX, False)
    LESS
    >>> cmp_to_target(2, 2, by_value, MaxMin.MAX, False)
    EQUAL
    >>> cmp_to_target(1, 1, by_value, MaxMin.MAX, False)
    EQUAL
    >>> cmp_to_target(2, 1, by_value, MaxMin.MIN, False)
    LESS
    >>> cmp_to_target(1, 2, by_value, MaxMin.MIN, False)
    GREATER
    >>> cmp_to_target(2, 2, by_value, MaxMin.MIN, False)
    EQUAL
    >>> cmp_to_target(1, 2, by_value, MaxMin.SKIP, False)
    EQUAL
    >>> cmp_to_target(None, 1, by_value, MaxMin.MIN, False)
    LESS
    >>> cmp_to_target(1, None, by_value, MaxMin.MIN, False)
    GREATER
    >>> cmp_to_target(None, None, by_value, MaxMin.MIN, False)
    EQUAL
    >>> cmp_to_target(None, 1, by_none, MaxMin.MAX, False)
    LESS
    >>> cmp_to_target(1, None, by_none, MaxMin.MAX, False)
    GREATER
    >>> cmp_to_target(None, None, by_none, MaxMin.MAX, False)
    EQUAL

    """
    if target is MaxMin.SKIP:
        return Domination.EQUAL
    if a is None and b is not None:
        return Domination.LESS if not none_is_good else Domination.GREATER
    if a is not None and b is None:
        return Domination.GREATER if not none_is_good else Domination.LESS
   
    if a is None and b is None:
        return Domination.EQUAL

    cmp_result = cmp(a ,b)
    if target is MaxMin.MAX:
        return cmp_result
    else:
        if cmp_result is Domination.LESS:
            return Domination.GREATER
        elif cmp_result is Domination.GREATER:
            return Domination.LESS
        else:
            return Domination.EQUAL

def dominates(a: list, b: list, cmp, targets: MaxMinList) -> Domination:
    """
    >>> a = [None]
    >>> b = [1]
    >>> target = MaxMinList(MaxMin.MIN)
    >>> dominates(a, a, by_none, target)
    EQUAL
    >>> dominates(a, b, by_none, target)
    LESS
    >>> dominates(b, a, by_none, target)
    GREATER
    >>> dominates(b, b, by_none, target)
    EQUAL
    >>> a = [1, None]
    >>> b = [1, 1]
    >>> target = MaxMinList(MaxMin.MIN, MaxMin.MIN)
    >>> dominates(a, a, by_none, target)
    EQUAL
    >>> dominates(a, b, by_none, target)
    LESS
    >>> dominates(b, a, by_none, target)
    GREATER
    >>> dominates(b, b, by_none, target)
    EQUAL
    >>> dominates([1, None], [None, 1], by_none, target)
    EQUAL
    >>> a = [2, 1]
    >>> b = [2, 2]
    >>> target = MaxMinList(MaxMin.MAX, MaxMin.MAX)
    >>> dominates(a, a, by_value, target)
    EQUAL
    >>> dominates(a, b, by_value, target)
    LESS
    >>> dominates(b, a, by_value, target)
    GREATER
    >>> dominates(b, b, by_value, target)
    EQUAL
    >>> dominates([1, 0], [0, 1], by_value, target)
    EQUAL

    """
    results = list()
    for d in range(targets.dim):
        results.append(cmp_to_target(a[d], b[d], cmp, targets.list[d], targets.none_is_good))
    
    is_greater_in_any = False
    for r in results:
        if r is Domination.GREATER:
            is_greater_in_any = True
            break

    is_less_in_any = False
    for r in results:
        if r is Domination.LESS:
            is_less_in_any = True
            break

    if is_greater_in_any and not is_less_in_any:
        return Domination.GREATER
    if is_less_in_any and not is_greater_in_any:
        return Domination.LESS
    return Domination.EQUAL


def find_dimension_maxmin_set(values, cmp, targets: MaxMinList):
    """
    Pareto front can be made by doing first the splitting by just 
    getting the best of each dimenstion to a separate group. This group might still
    contain some sub pareto sets.

    >>> values = [(0,0,1), (0,1,0), (1,0,0), (0,0,0)]
    >>> cmp = by_value
    >>> targets = MaxMinList(MaxMin.MAX, MaxMin.MAX, MaxMin.MAX)
    >>> find_dimension_maxmin_set(values, cmp, targets)
    [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    >>> values = [(0,0,1), (0,1,0), (1,0,0), (1,1,1)]
    >>> find_dimension_maxmin_set(values, cmp, targets)
    [(1, 0, 0), (1, 1, 1), (0, 0, 1), (0, 1, 0)]
    """
    dimension_maxmin_set = set([])
    if values is None or len(values) == 0:
        return []
    
    for d in range(targets.dim):
        target = targets.list[d]
        if target is MaxMin.SKIP:
            continue
        
        max_set = [values[0]]
        for value in values:
            cmp_result = cmp_to_target(max_set[0][d], value[d], cmp, targets.list[d], targets.none_is_good)
            if cmp_result is Domination.GREATER:
                continue
            elif cmp_result is Domination.EQUAL:
                max_set.append(value)
            else:
                max_set = [value]
        dimension_maxmin_set = dimension_maxmin_set.union(max_set)
    
    return list(dimension_maxmin_set)

def split_by_dimensions(values, cmp, targets: MaxMinList):
    """
    Pareto fronts can be made by doing first the splitting by just 
    getting the best of each dimenstion to a separate group. 
    This groups might still contain some sub pareto groups in them.
    >>> values = [(2,2,2), (0,1,1), (0,0,1), (0,1,0), (1,0,0), (0,0,0)]
    >>> cmp = by_value
    >>> targets = MaxMinList(MaxMin.MAX, MaxMin.MAX, MaxMin.MAX)
    >>> split_by_dimensions(values, cmp, targets)
    [[(2, 2, 2)], [(1, 0, 0), (0, 1, 1), (0, 1, 0), (0, 0, 1)], [(0, 0, 0)]]


    """
    if values is None or len(values) == 0:
        return []
    if len(values) == 1:
        return [values]
    
    splitted = []
    while True:
        top_group = find_dimension_maxmin_set(values, cmp, targets)
        if len(top_group) > 0:
            splitted.append(top_group)
            for v in top_group:
                values.remove(v)
            continue
        if len(values) > 0:
            splitted.append(values)
        break
    return splitted


def get_dominating_set(values, dominates):
    """
    >>> cmp = by_value
    >>> targets = MaxMinList(MaxMin.MAX, MaxMin.MAX, MaxMin.MAX)
    >>> dominates = Comparison(cmp, targets).compare
    >>> get_dominating_set([(2,2,2), (0,1,1), (0,0,1), (0,1,0), (1,0,0), (0,0,0)], dominates)
    [(2, 2, 2)]
    >>> get_dominating_set([(0,1,1), (0,0,1), (0,1,0), (1,0,0), (0,0,0)], dominates)
    [(1, 0, 0), (0, 1, 1)]
    >>> get_dominating_set([(0,0,1), (0,1,0), (0,0,0)], dominates)
    [(0, 1, 0), (0, 0, 1)]
    >>> get_dominating_set([(0,0,0)], dominates)
    [(0, 0, 0)]

    """
    if values is None or len(values) == 0:
        return []
    
    max_set = [values[0]]
    for value in values:
        cmp_result = dominates(max_set[0], value)
        if cmp_result is Domination.GREATER:
            continue
        elif cmp_result is Domination.EQUAL:
            max_set.append(value)
        else:
            max_set = [value]
    
    return list(set(max_set))


def split_by_pareto(values, dominates):
    """
    Pareto fronts can be made by doing first the splitting by just 
    getting the best of each dimenstion to a separate group. 
    This groups might still contain some sub pareto groups in them.


    >>> values = [(2,2,2), (0,1,1), (0,0,1), (0,1,0), (1,0,0), (0,0,0)]
    >>> targets = MaxMinList(MaxMin.MAX, MaxMin.MAX, MaxMin.MAX)
    >>> dominates = Comparison(by_value, targets).compare
    >>> split_by_pareto(values, dominates)
    [[(2, 2, 2)], [(1, 0, 0), (0, 1, 1)], [(0, 1, 0), (0, 0, 1)], [(0, 0, 0)]]

    >>> values = [(0, 1, 1), (1, 0, 0), (0, 0, 1), (None, 1, 1), (0, 1, 0), (None, 0, 1)]
    >>> targets = MaxMinList(MaxMin.MAX, MaxMin.MAX, MaxMin.MAX)
    >>> dominates = Comparison(by_value, targets).compare
    >>> split_by_pareto(values, dominates)
    [[(1, 0, 0), (0, 1, 1)], [(0, 1, 0), (None, 1, 1), (0, 0, 1)], [(None, 0, 1)]]


    >>> values = [(1, 1, 1), (1, 1, 1)]
    

    """
    if values is None or len(values) == 0:
        return []
    if len(values) == 1:
        return [values]

    splitted = []
    while True:
        top_group = get_dominating_set(values, dominates)
        if len(top_group) > 0:
            splitted.append(top_group)
            for v in top_group:
                values.remove(v)
            continue
        if len(values) > 0:
            splitted.append(values)
        break
    return splitted

class Cmp(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def compare(self, a, b) -> Domination:
        raise NotImplementedError
    
    @abc.abstractclassmethod
    def is_pareto(self) -> bool:
        raise NotImplementedError
    
    @abc.abstractclassmethod
    def is_group(self) -> bool:
        raise NotImplementedError

    @abc.abstractclassmethod
    def group(self, a) -> int:
        raise NotImplementedError

class GroupNones(Cmp):
    def __init__(self, targets: MaxMinList):
        self._targets = targets
    @property
    def targets(self):
        return self._targets
    def compare(self, a, b) -> Domination:
        raise NotImplementedError
    def is_pareto(self) -> bool:
        return False
    def is_group(self) -> bool:
        return True

    def group(self, a) -> int:
        """
        GroupNones(MaxMinList(MaxMin.MIN, MaxMin.MIN, MaxMin.MIN)).group((0,None,None))
        -2
        """
        noneSum = 0
        for d in range(self.targets.dim):
            if self.targets.list[d] is MaxMin.SKIP:
                continue
            if self.targets.list[d] is MaxMin.MAX and a[d] is None:
                noneSum += 1
            if self.targets.list[d] is MaxMin.MIN and a[d] is None:
                noneSum -= 1
        return noneSum
    
    def and_then(self, c: Cmp) -> Cmp:
        return ComparisonChain(self, c)
    
    def as_chain(self):
        return ComparisonChain(self)


class Comparison(Cmp):
    def __init__(self, cmp, targets: MaxMinList):
        self._cmp = cmp
        self._targets = targets
    
    def is_pareto(self) -> bool: return True
    def is_group(self) -> bool: return False
    def group(self, a) -> int: return 1

    @property
    def cmp(self):
        return self._cmp

    @property
    def targets(self):
        return self._targets

    def compare(self, a,b) -> Domination:
        return dominates(a, b, self.cmp, self.targets)

    def and_then(self, c: Cmp) -> Cmp:
        return ComparisonChain(self, c)
    
    def as_chain(self):
        return ComparisonChain(self)

class ComparisonChain:
    def __init__(self, *chain: List[Comparison]):
        self._chain = chain

    @property
    def chain(self) -> List[Comparison]:
        return self._chain

    def compare(self, a, b) -> Domination:
        for c in self.chain[:-1]:
            if not c.is_pareto():
                continue
            result = c.compare(a, b)
            if result == Domination.EQUAL:
                continue
            return result
        return self.chain[-1].compare(a, b)
    
    def and_then(self, c: Cmp) -> Cmp:
        return ComparisonChain(self, *self.chain, c)

    def pre_split(self, values):
        """
        Before doing the N^2 pareto splits, split the values to preliminary groups by using thi function.

        >>> values = [(0,None,None), (2,2,2), (0,1,1), (0,0,1), (None,0,1), (0,1,0), (None,1,1), (1,0,0), (0,0,0)]
        >>> chain = Comparison(by_value, MaxMinList(MaxMin.MAX, MaxMin.MAX, MaxMin.MAX)).as_chain()
        >>> chain.pre_split(values)
        [[(2, 2, 2)], [(0, 1, 1), (1, 0, 0), (0, 0, 1), (None, 1, 1), (0, 1, 0), (None, 0, 1)], [(0, 0, 0), (0, None, None)]]

        >>> chain = GroupNones(MaxMinList(MaxMin.MIN, MaxMin.MIN, MaxMin.MIN)).as_chain()
        >>> values = [(0,None,None), (2,2,2), (0,1,1), (0,0,1), (None,0,1), (0,1,0), (None,1,1), (1,0,0), (0,0,0)]
        >>> chain.pre_split(values)
        [[(2, 2, 2), (0, 1, 1), (0, 0, 1), (0, 1, 0), (1, 0, 0), (0, 0, 0)], [(None, 0, 1), (None, 1, 1)], [(0, None, None)]]

        """
        splitted = [values]
        for comparison in self.chain:
            if comparison.is_pareto():
                new_splitted = []
                while len(splitted) > 0:
                    group = splitted.pop(0)
                    new_groups = split_by_dimensions(group, comparison.cmp, comparison.targets)
                    new_splitted.extend(new_groups)
                splitted = new_splitted
            elif comparison.is_group():
                new_splitted = []
                while len(splitted) > 0:
                    group = splitted.pop(0)
                    group_dict = defaultdict(list)
                    for a in group:
                        group_dict[comparison.group(a)].append(a)
                    keys = list(group_dict.keys())
                    keys.sort()
                    keys.reverse()
                    new_groups = [group_dict[k] for k in keys]
                    
                    new_splitted.extend(new_groups)
                splitted = new_splitted
        return splitted
    
    def split_by_pareto(self, values):
        """ComparisonChain.split_by_pareto performs the pareto front split fronts.

Currently this works only for unique rows. You can add id as the last row (and not sort by it) to work around this restriction.

Here the None means just inferior value:

    >>> values = [(0,None,None), (2,2,2), (0,1,1), (0,0,1), (None,0,1), (0,1,0), (None,1,1), (1,0,0), (0,0,0)]
    >>> chain = Comparison(by_value, MaxMinList(MaxMin.MAX, MaxMin.MAX, MaxMin.MAX)).as_chain()
    >>> chain.split_by_pareto(values)
    [[(2, 2, 2)], [(1, 0, 0), (0, 1, 1)], [(0, 1, 0), (None, 1, 1), (0, 0, 1)], [(None, 0, 1)], [(0, 0, 0)], [(0, None, None)]]

Here one extra None means that the whole row is inferior:

    >>> values = [(0,None,None), (2,2,2), (0,1,1), (0,0,1), (None,0,1), (0,1,0), (None,1,1), (1,0,0), (0,0,0), (None, 0, None)]
    >>> chain = GroupNones(MaxMinList(MaxMin.MIN, MaxMin.MIN, MaxMin.MIN)).and_then(
    ...    Comparison(by_value, MaxMinList(MaxMin.MAX, MaxMin.MAX, MaxMin.MAX)))
    >>> chain.split_by_pareto(values)
    [[(2, 2, 2)], [(1, 0, 0), (0, 1, 1), (0, 1, 0), (0, 0, 1)], [(0, 0, 0)], [(None, 1, 1)], [(None, 0, 1)], [(None, 0, None), (0, None, None)]]
"""
        splitted = self.pre_split(values)
        new_splitted = []
        while len(splitted) > 0:
            group = splitted.pop(0)
            new_groups = split_by_pareto(group, self.compare)
            new_splitted.extend(new_groups)
        splitted = new_splitted
        return splitted




if __name__ == "__main__":
    import doctest
    doctest.testmod()