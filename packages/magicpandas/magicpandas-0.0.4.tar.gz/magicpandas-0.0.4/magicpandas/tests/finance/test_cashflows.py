from time import time
import numpy as np
from numpy.testing import assert_almost_equal

from magicpandas.finance.cashflows import mortgage_cashflows

# from pandicake.collateral import repline_cashflows # , pv, irr, bond_price, bond_yield
# from bc35 import bc35, bc35_yield

# def test_pmt_frame_v1():
#     t0 = time()
#     df = pmt_frame(5/1200, 360, -100000, smm=0.01)
#     last_ten_calced = np.array(df[-10:].pmt)
#     last_ten_true = np.array([17.331581352124402, 17.006374868980572, 16.6853128083522, 16.368348483412756, 16.05543570500424, 15.746528776479554, 15.44158248859752, 15.140552114470001, 14.843393404560556, 14.550062581734196])
#     assert_almost_equal(last_ten_calced, last_ten_true)
#     print('[{:,.2f} ms] '.format(1000*(time()-t0)), end='')


def test_mortgage_cashflows():
    t0 = time()
    pmt = mortgage_cashflows(5, 360, 100000, smm=0.01, pmt_only=True)
    last_ten_calced = pmt[-10:]
    last_ten_true = np.array([17.331581352124402, 17.006374868980572, 16.6853128083522, 16.368348483412756, 16.05543570500424, 15.746528776479554, 15.44158248859752, 15.140552114470001, 14.843393404560556, 14.550062581734196])
    assert_almost_equal(last_ten_calced, last_ten_true)
    print('[{:,.2f} ms] '.format(1000*(time()-t0)), end='')
