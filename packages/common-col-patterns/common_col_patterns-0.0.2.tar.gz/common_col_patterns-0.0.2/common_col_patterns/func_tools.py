"""
Mostly extensions of common functional tools

Glossary:
* functions prepended with t - will result in a tuple result
* functions prepended with s - will result in a set result
* functions appended with a number - will accept further arguments before the iterable:
    example:
    tmap1(list, 0, [1,2,3]) -> ([0,1], [0,2], [0,3])

* Function doc will be found in the basic example for each family
"""

import operator
from functools import partial
from typing import Iterable, Callable

from funcy import group_by, flatten


def tsorted(it: Iterable, key=None):
    return tuple(sorted(it, key=key))


def map1(f: Callable[[object, object], object], arg1: object, it: Iterable) -> map:
    """

    :param f: any function that will accept arg1, and an item from it and return something
    :param arg1: constant arg that will passed as first argument of f each time
    :param it: any iterable
    :return: map(f(arg1, x)) for an x in it
    """
    return map(partial(f, arg1), it)


def map2(f: Callable[[object, object], object], arg1: object, arg2: object, it: Iterable) -> map:
    return map(partial(f, arg1, arg2), it)


def tmap(f: Callable[[object], object], it: Iterable) -> tuple:
    return tuple(map(f, it))


def tmap1(f: Callable[[object, object], object], arg1: object, it: Iterable) -> tuple:
    return tmap(partial(f, arg1), it)


def tmap2(f: Callable[[object, object], object], arg1: object, arg2: object, it: Iterable) -> tuple:
    return tmap(partial(f, arg1, arg2), it)


def smap(f: Callable[[object], object], it: Iterable) -> set:
    return set(map(f, it))


def smap1(f: Callable[[object, object], object], arg1: object, it: Iterable) -> set:
    return smap(partial(f, arg1), it)


def smap2(f: Callable[[object, object], object], arg1: object, arg2: object, it: Iterable) -> set:
    return smap(partial(f, arg1, arg2), it)


def tfilter(pred: Callable[[object], bool], it: Iterable) -> tuple:
    return tuple(filter(pred, it))


def tfilter1(pred: Callable[[object, object], bool], arg1: object, it: Iterable) -> tuple:
    return tfilter(partial(pred, arg1), it)


def tfilter2(pred: Callable[[object, object, object], bool], arg1: object, arg2: object, it: Iterable) -> tuple:
    return tfilter(partial(pred, arg1, arg2), it)


def sfilter(pred: Callable[[object], bool], it: Iterable) -> set:
    return set(filter(pred, it))


def sfilter1(pred: Callable[[object, object], bool], arg1: object, it: Iterable) -> set:
    return sfilter(partial(pred, arg1), it)


def sfilter2(pred: Callable[[object, object, object], bool], arg1: object, arg2: object, it: Iterable) -> set:
    return sfilter(partial(pred, arg1, arg2), it)


def filter_attr_eq(attr: str, eq_to: object, it: Iterable) -> filter:
    """

    :param attr: a name of an attribute we expect to find on items in it
    :param eq_to: any comparable value
    :param it: any iterable
    :return: filter object with all x in it such as x.attr == eq_to
    """
    return filter(lambda x: getattr(x, attr) == eq_to, it)


def lfilter_attr_eq(attr: str, eq_to: object, it: Iterable) -> list:
    return list(filter_attr_eq(attr, eq_to, it))


def tfilter_attr_eq(attr: str, eq_to: object, it: Iterable) -> tuple:
    return tuple(filter_attr_eq(attr, eq_to, it))


def sfilter_attr_eq(attr: str, eq_to: object, it: Iterable) -> set:
    return set(filter_attr_eq(attr, eq_to, it))


def filter_f_eq(f: str, eq_to: object, it: Iterable) -> filter:
    """

    :param f: a name of an function we expect to find on items in it
    :param eq_to: any comparable value
    :param it: any iterable
    :return: filter object with all x in it such as x.f() == eq_to
    """
    return filter(lambda x: getattr(x, f)() == eq_to, it)


def lfilter_f_eq(f: str, eq_to: object, it: Iterable) -> list:
    return list(filter_f_eq(f, eq_to, it))


def tfilter_f_eq(f: str, eq_to: object, it: Iterable) -> tuple:
    return tuple(filter_f_eq(f, eq_to, it))


def sfilter_f_eq(f: str, eq_to: object, it: Iterable) -> set:
    return set(filter_f_eq(f, eq_to, it))


def filter_fx_eq(f: Callable, eq_to: object, it: Iterable) -> filter:
    """

    :param f: a name of an function we expect to find on items in it
    :param eq_to: any comparable value
    :param it: any iterable
    :return: filter object with all x in it such as f(x) == eq_to
    """
    return filter(lambda x: f(x) == eq_to, it)


def lfilter_fx_eq(f: Callable, eq_to: object, it: Iterable) -> list:
    return list(filter_fx_eq(f, eq_to, it))


def tfilter_fx_eq(f: Callable, eq_to: object, it: Iterable) -> tuple:
    return tuple(filter_fx_eq(f, eq_to, it))


def sfilter_fx_eq(f: Callable, eq_to: object, it: Iterable) -> set:
    return set(filter_fx_eq(f, eq_to, it))


def sflatten(it: Iterable) -> set:
    return set(flatten(it))


def flatmap(f: Callable, it: Iterable) -> Iterable:
    return flatten(map(f, it))


def flatmap1(f: Callable, arg1: object, it: Iterable) -> Iterable:
    return flatten(map1(f, arg1, it))


def flatmap2(f: Callable, arg1: object, arg2: object, it: Iterable) -> Iterable:
    return flatten(map2(f, arg1, arg2, it))


def lflatmap(f: Callable, it: Iterable) -> list:
    return list(flatmap(f, it))


def lflatmap1(f: Callable, arg1: object, it: Iterable) -> list:
    return list(flatmap1(f, arg1, it))


def lflatmap2(f: Callable, arg1: object, arg2: object, it: Iterable) -> list:
    return list(flatmap2(f, arg1, arg2, it))


def sflatmap(f: Callable, it: Iterable) -> set:
    return set(flatmap(f, it))


def sflatmap1(f: Callable, arg1: object, it: Iterable) -> set:
    return set(flatmap1(f, arg1, it))


def sflatmap2(f: Callable, arg1: object, arg2: object, it: Iterable) -> set:
    return set(flatmap2(f, arg1, arg2, it))


def group_by_attr(attr: str, it: Iterable) -> dict:
    """

    :param attr: attribute expected to be on any item in it
    :param it: any iterable
    :return: dict -> where any item x in it, will be in a bucket key of which is x.attr
    """
    return dict(group_by(operator.attrgetter(attr), it))
