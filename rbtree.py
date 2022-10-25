"""
Rewrite from
https://github.com/koka-lang/koka/blob/master/test/bench/koka/rbtree.kk

"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Callable, Literal, TypeVar

sys.setrecursionlimit(10000000)


Color = Literal["Red", "Black"]


@dataclass
class Node:
    color: Color
    left: tree
    key: int
    value: bool
    right: tree


@dataclass
class Leaf:
    ...


tree = Node | Leaf


def is_red(t: tree) -> bool:
    match t:
        case Node("Red"):
            return True
        case _:
            return False


def balance_left(l: tree, k: int, v: bool, r: tree) -> tree:
    match l:
        case Node(_, Node("Red", lx, kx, vx, rx), ky, vy, ry):
            return Node(
                "Red",
                Node("Black", lx, kx, vx, rx),
                ky,
                vy,
                Node("Black", ry, k, v, r),
            )
        case Node(_, ly, ky, vy, Node("Red", lx, kx, vx, rx)):
            return Node(
                "Red",
                Node("Black", ly, ky, vy, lx),
                kx,
                vx,
                Node("Black", rx, k, v, r),
            )
        case Node(_, lx, kx, vx, rx):
            return Node("Black", Node("Red", lx, kx, vx, rx), k, v, r)
        case Leaf():
            return Leaf()


def balance_right(l: tree, k: int, v: bool, r: tree) -> tree:
    match r:
        case Node(_, Node("Red", lx, kx, vx, rx), ky, vy, ry):
            return Node(
                "Red",
                Node("Black", l, k, v, lx),
                kx,
                vx,
                Node("Black", rx, ky, vy, ry),
            )
        case Node(_, lx, kx, vx, Node("Red", ly, ky, vy, ry)):
            return Node(
                "Red",
                Node("Black", l, k, v, lx),
                kx,
                vx,
                Node("Black", ly, ky, vy, ry),
            )
        case Node(_, lx, kx, vx, rx):
            return Node("Black", l, k, v, Node("Red", lx, kx, vx, rx))
        case Leaf():
            return Leaf()


def ins(t: tree, k: int, v: bool) -> tree:
    match t:
        case Node("Red", l, kx, vx, r):
            if k < kx:
                return Node("Red", ins(l, k, v), kx, vx, r)
            elif k > kx:
                return Node("Red", l, kx, vx, ins(r, k, v))
            else:
                return Node("Red", l, k, v, r)
        case Node("Black", l, kx, vx, r):
            if k < kx:
                if is_red(l):
                    return balance_left(ins(l, k, v), kx, vx, r)
                else:
                    return Node("Black", ins(l, k, v), kx, vx, r)
            elif k > kx:
                if is_red(r):
                    return balance_right(l, kx, vx, ins(r, k, v))
                else:
                    return Node("Black", l, kx, vx, ins(r, k, v))
            else:
                return Node("Black", l, k, v, r)
        case Leaf():
            return Node("Red", Leaf(), k, v, Leaf())


def set_black(t: tree) -> tree:
    match t:
        case Node(_, l, k, v, r):
            return Node("Black", l, k, v, r)
        case _:
            return t


def insert(t: tree, k: int, v: bool) -> tree:
    return set_black(ins(t, k, v))


a = TypeVar("a")


def fold(t: tree, b: a, f: Callable[[int, bool, a], a]) -> a:
    match t:
        case Node(_, l, k, v, r):
            return fold(r, f(k, v, fold(l, b, f)), f)
        case Leaf():
            return b


def make_tree_aux(n: int, t: tree) -> tree:
    if n <= 0:
        return t
    n1 = n - 1
    return make_tree_aux(n - 1, insert(t, n1, n1 % 10 == 0))


def make_tree(n: int) -> tree:
    return make_tree_aux(n, Leaf())


def main():
    t = make_tree(13)
    print(t)
    v = fold(t, 0, lambda k, v, a: a + 1 if v else a)
    print(v)


main()
