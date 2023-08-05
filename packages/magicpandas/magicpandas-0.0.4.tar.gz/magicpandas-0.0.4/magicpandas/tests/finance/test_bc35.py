# from pprint import pprint; pprint(locals()); assert False
from magicpandas.finance.bc35 import bc35_price, bc35_yield
import numpy as np


def test_that_bc35_price_is_invertible_with_scalars():
    scalar_price = bc35_price(6, 5, 15, 0, 360, 360)[0]
    scalar_yield = bc35_yield(scalar_price, 5, 15, 0, 360, 360)
    assert abs(scalar_yield - 6) < 0.000000001


def test_that_bc35_price_works_with_numpy_arrays():
    scalar_result_0 = bc35_price(6, 5, 15, 0, 360, 360)
    scalar_result_1 = bc35_price(7, 5, 15, 0, 360, 360)
    beyield = np.array([6, 7])
    coupon = np.array([5, 5])
    cpr = np.array([15, 15])
    age = np.array([0, 0])
    origfixedterm = np.array([360, 360])
    origterm = np.array([360, 360])
    array_result = bc35_price(beyield, coupon, cpr, age, origfixedterm, origterm)
    assert scalar_result_0[0] == array_result[0][0]
    assert scalar_result_0[1] == array_result[1][0]
    assert scalar_result_0[2] == array_result[2][0]
    assert scalar_result_1[0] == array_result[0][1]
    assert scalar_result_1[1] == array_result[1][1]
    assert scalar_result_1[2] == array_result[2][1]


def test_that_bc35_price_is_invertible_with_numpy_arrays():
    beyield = np.array([5, 6])
    coupon = np.array([5, 5])
    cpr = np.array([15, 15])
    age = np.array([0, 0])
    origfixedterm = np.array([360, 360])
    origterm = np.array([360, 360])
    price_array = bc35_price(beyield, coupon, cpr, age, origfixedterm, origterm)
    yield_array = bc35_yield(price_array[0], coupon, cpr, age, origfixedterm, origterm)
    assert abs(yield_array[0] - 5) < 0.000000001
    assert abs(yield_array[1] - 6) < 0.000000001
