from time import time
import numpy as np
from numpy.testing import assert_almost_equal

from magicpandas.finance.cashflows import mortgage_cashflows
from magicpandas.finance.irr import pv, irr
from time import time
from magicpandas.finance.irr import pv, irr, mortgage_price, mortgage_yield
from magicpandas.finance.bc35 import bc35_price, bc35_yield
from magicpandas.finance.cashflows import mortgage_cashflows


def test_pv_v1():
    t0 = time()
    pmt = mortgage_cashflows(5, 360, 100000, smm=0.02, pmt_only=True)
    pv2 = pv(5/1200, pmt)
    assert abs(pv2-100000) < 0.0000001
    print('[{:,.2f} ms] '.format(1000*(time()-t0)), end='')


def test_irr_v1():
    t0 = time()
    pmt = mortgage_cashflows(5, 360, 100000, smm=0.02, pmt_only=True)
    irr2 = irr(100000, pmt)
    assert abs(irr2*1200-5) < 0.0000001
    print('[{:,.2f} ms] '.format(1000*(time()-t0)), end='')


def test_irr_numpy_financial():
    t0 = time()
    pmt = mortgage_cashflows(5, 360, 100000, smm=0.02, pmt_only=True)
    irr2 = irr(100000, pmt, use_scipy_optimize_root=False)
    assert abs(irr2*1200-5) < 0.0000001
    print('[{:,.2f} ms] '.format(1000*(time()-t0)), end='')


def test_mortgage_price_v1():
    t0 = time()
    pmt = mortgage_cashflows(5, 360, 100000, smm=0.02, pmt_only=True)
    yld = 200 * ((1 + 0.06 / 12) ** 6 - 1)
    v1 = mortgage_price(yld, 5, 100000, pmt, delay=30)
    cpr = 100*(1-(1-0.02)**12)
    v2, x, y = bc35_price(yld, 5, cpr, 0, 360, 360, delay=30)
    assert abs(v1-v2) < 0.000001
    print('[{:,.2f} ms] '.format(1000*(time()-t0)), end='')


def test_bond_yield_v1():
    t0 = time()
    pmt = mortgage_cashflows(5, 360, 100000, smm=0.02, pmt_only=True)
    cpr = 100*(1-(1-0.02)**12)
    v1 = mortgage_yield(101, 5, 100000, pmt, delay=44)
    v2 = bc35_yield(101, 5, cpr, 0, origfixedterm=360, origterm=360, delay=44)
    assert abs(v1-v2) < 0.000001
    print('[{:,.2f} ms] '.format(1000*(time()-t0)), end='')
