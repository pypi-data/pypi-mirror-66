"""
Some operations applied to iterables / collections
"""

from functools import partial
from itertools import islice, chain
from typing import Sequence, Iterable, Sized, Hashable, Tuple

from funcy import merge_with, select_keys


def geti(seq: Sequence, i: int, default=None):
    """
    Behaves like dict.get but for sequences
    """
    if i < 0 or i >= len(seq):
        return default
    return seq[i]


def irange(itr: Sized) -> range:
    """

    :param itr: Any sizable collection
    :return: iterable range from 0 to len of itr
    """
    return range(len(itr))


def window(seq: Sequence, n=2) -> Iterable[tuple]:
    """
    Returns a sliding window (of width n) over data from the iterable
      s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...
    """
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def perms_as_stream(perms: Sequence[Sequence], l_pad=None, r_pad=None, pad_num=1) -> Iterable:
    """
    for a sequence of sequences return an item stream out of those sequences (like chain)
    padded by l_pad and r_pad:
    ex:
    for [[1,2], [3,4]] with default pads we would get:
    -> None, 1, 2, None, None, 3, 4, None

    this is useful when we want a context window over a collection,
    but don't want to miss the first / last chars as middle of the window
    """
    left_pad = [l_pad] * pad_num
    right_pad = [r_pad] * pad_num
    return chain(*[left_pad + list(p) + right_pad
                   for p in perms])


def neighbour_set(seq: Sequence[Hashable], item: Hashable) -> frozenset:
    """

    :param seq: any sequence of hashable items
    :param item: an item we expect to find in seq
    :return: all the neighbours of item in seq
    """
    indices = [i for i, x in enumerate(seq) if x == item]
    neighbour_indices = {
        x - 1 for x in indices if x > 0
    }.union({
        x + 1 for x in indices if x < len(seq) - 1
    })

    neighbours = frozenset(seq[idx] for idx in neighbour_indices)
    return neighbours


def is_seq_consecutive(it: Iterable[int]) -> bool:
    """

    :param it: any Iterable of integers
    :return: whether the iterable consists of consecutive numbers
    """
    sorted_list = sorted(it)
    consecutive_list = list(range(sorted_list[0], sorted_list[-1] + 1))
    return consecutive_list == sorted_list


def iter_item_occurrence(it: Iterable) -> Iterable[Tuple[object, int]]:
    """
    example:
    GeeeEEKKKss -> (G, 1), (e, 3), (E, 2), (K, 3), (s, 2)
    """
    idx = 0
    it = tuple(it) + ("#@$@#$@#$@#",)
    while idx < len(it) - 1:
        count = 1
        while it[idx] == it[idx + 1]:
            idx += 1
            count += 1

            if idx + 1 == len(it):
                break

        yield it[idx], count
        idx += 1


def invert_dict_multi_val(d: dict) -> dict:
    """
    example: {1:2, 3:2} -> {2, (1, 3)}
    """
    return merge_with(tuple, *({val: key} for key, val in d.items()))


def all_eq(*items) -> bool:
    """
    Tests whether all passed items are equal
    """
    return items.count(items[0]) == len(items)


def same_abc(its: Iterable[Iterable]) -> bool:
    """ Test whether the iterables consist of the same items """
    return all_eq(*map(frozenset, its))


def diff_abc(its: Iterable[Iterable]) -> bool:
    return not same_abc(its)


def same_len(collections: Iterable[Sized]) -> bool:
    return all_eq(*map(len, collections))


def diff_len(collections: Iterable[Sized]) -> bool:
    return not same_len(collections)


def sub_dicts_eq(keys: set, *objs: object) -> bool:
    """ Test whether sub dictionaries of dicts/objects are equal"""
    if not objs:
        return True

    eq_subset = partial(select_keys, keys)
    return all_eq(*map(eq_subset, objs))


def all_indices(it: Iterable, item: object) -> Iterable[int]:
    """ All indices of item in it """
    return (i for i, x in enumerate(it) if x == item)


def num_appear(it: Iterable, item: object) -> int:
    """ Number of times item appear in it """
    return len(tuple(all_indices(it, item)))
