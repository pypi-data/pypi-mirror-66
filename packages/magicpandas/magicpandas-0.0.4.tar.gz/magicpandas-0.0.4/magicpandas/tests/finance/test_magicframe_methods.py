# from pprint import pprint; pprint(locals()); assert False
import pytest
import numpy as np
import pandas as pd
from magicpandas import MagicDataFrame
from magicpandas.finance.bc35 import bc35_price, bc35_yield


@pytest.fixture
def df():
    return MagicDataFrame({
        'coupon': [5, 4.5, 4, 3.5, 3],
        'origfixedterm': [60, 84, 120, 180, 360],
        'origterm': [360, 360, 360, 180, 360],
        'age': [12, 12, 12, 12, 12],
        'cpr': [15, 15, 15, 15, 15],
        'origupb': [100, 200, 300, 400, 500],
        'upb': [100, 200, 300, 400, 500],
        'servicing_fee': [0, 0, 0, 0, 0],
    })


def test_bc35_price_gen(df):
    df['beyield'] = 5
    df = df.bc35_price_gen()
    # assert abs(df._price[0] - 99.901962) < 0.0001
    beyield = np.array(df.beyield)
    coupon = np.array(df.coupon)
    cpr = np.array(df.cpr)
    age = np.array(df.age)
    origfixedterm = np.array(df.origfixedterm)
    origterm = np.array(df.origterm)
    price_array = bc35_price(beyield, coupon, cpr, age, origfixedterm, origterm)[0]
    assert (np.array(df.price) == price_array).all()


def test_bc35_yield_gen(df):
    df['price'] = 99.901962
    df = df.bc35_yield_gen()
    # assert abs(df._price[0] - 99.901962) < 0.0001
    price = np.array(df.price)
    coupon = np.array(df.coupon)
    cpr = np.array(df.cpr)
    age = np.array(df.age)
    origfixedterm = np.array(df.origfixedterm)
    origterm = np.array(df.origterm)
    yield_array = bc35_yield(price, coupon, cpr, age, origfixedterm, origterm)
    assert (np.array(df.beyield) == yield_array).all()
