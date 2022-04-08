import pytest

from ip_wolf_goat_kabbage import leftright


def test_leftright():
    left, right = leftright([1, 0, 1])
    print(left, right)
    assert left == 'wk'
    assert right == 'g'
    left, right = leftright([0, 0, 0])
    print(left, right)
    assert left == ''
    assert right == 'wgk'
    left, right = leftright([1, 1, 1])
    print(left, right)
    assert left == 'wgk'
    assert right == ''
