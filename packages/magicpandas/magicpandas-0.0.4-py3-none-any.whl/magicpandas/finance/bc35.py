"""
bc35 is named after a Bloomberg terminal calculator of the same name.

irr.py: Perform IRR calculations on as arbitrary set of cash flows.
cashflows.py: Create mortgage cash flows (pools not bonds) based on a small set
    of scalars.
bc35.py: Combine irr.py and cashflows.py i.e., perform IRR calculations on
    mortgage cash flows, which are defined based on a small number of scalars.

It turns out that BC35 calculations can be performed using a closed form
    formula.  This calculation is alternative method that can be used to improve
    execution time as well as for unit testing.
"""

import numpy as np
import numpy_financial as npf
from scipy import optimize
import warnings

'''
# BC35
def bc35_price(yld, rate, nper, upb, cpr, servicing_fee=0.0):
    # UNDER CONSTRUCTION
    smm = 1 - (1-cpr/100)**(1/12)
    pmt = pmt_array(rate/1200, nper, -upb, smm=smm, servicing_fee=servicing_fee/1200) # , current_pandi=None, return_frame=False)
    return price
'''


def bc35_price(beyield, coupon, cpr, age, origfixedterm, origterm, dayofmonth=1,
               delay=47, servicing_fee=0, root=None):  # 47 is market standard according to Goldmach Sachs
    '''
    This implements BC35 in core Python (vs columnwise in a pandas.DataFrame)
    '''
    epsilon = servicing_fee/1200

    r = coupon/1200
    y = ((1+beyield/200)**(1/6)-1)
    s = (1-(1-cpr/100)**(1/12))

    m = (origfixedterm - age)
    n = (origterm - age)

    qn = (1 - 1/(1+r)**n)
    l1 = (r*(1-s)-epsilon+s*(1+r))/qn  												# lambda 1
    l2 = (s*(1+r)-epsilon)*(1-1/qn)													# lambda 2
    l3 = ((1-1/qn)*((1+r)*(1-s))**m+(1/qn)*(1-s)**m)							# lambda 3

    pvl1 = (l1/(y+s))*(1-((1-s)/(1+y))**m)							# PV of lamda 1 term
    pvl2 = (l2/(y-(1+r)*(1-s)+1))*(1-((1+r)*(1-s)/(1+y))**m)		# PV of lamda 2 term
    pvb = (l3/(1+y)**m)													# PV of the balloon term
    price = 100*(pvl1+pvl2+pvb)

    # Mod Durn
    dvl1 = (l1/(y+s))*((m/(1+y))*((1-s)/(1+y))**m)-(l1/(y+s)**2)*(1-((1-s)/(1+y))**m)
    dvl2 = (l2/(y-(1+r)*(1-s)+1))*((m/(1+y))*((1+r)*(1-s)/(1+y))**m)-(l2/(y-(1+r)*(1-s)+1)**2)*(1-((1+r)*(1-s)/(1+y))**m)
    dvb = (-m*l3/(1+y)**(m+1))
    adjfactor = (12*(1+beyield/200)**(5/6))
    staticdv01 = -(dvl1 + dvl2 + dvb)/adjfactor  # adjustment factor to reflect derivative based on bond equivalent yield (using the chain rule)
    moddurn = staticdv01/(price/100)

    # WAL
    l1 = (r*(1-s)+s*(1+r))/qn  												# HACK: lambda 1 assuming no servicing fee; price/moddurn fine withou the servicing fee adjustment, but the WAL math breaks
    l2 = (s*(1+r))*(1-1/qn)													# HACK: lambda 2 assuming no servicing fee; price/moddurn fine withou the servicing fee adjustment, but the WAL math breaks
    multl1 = (l1-r/qn)
    wall1 = ((1-((1-s))**(m+1))/(1-((1-s)))-(m+1)*((1-s))**m)/(1-((1-s)))
    multl2 = (l2+(r/qn)/(1+r)**n)
    wall2 = ((1-((1-s)*(1+r))**(m+1))/(1-((1-s)*(1+r)))-(m+1)*((1-s)*(1+r))**m)/(1-((1-s)*(1+r)))

    qnlessm = (1 - 1/(1+r)**(n-m))
    walb = (m*qnlessm/qn*(1-s)**(m))

    wal = (multl1*wall1+multl2*wall2+walb)/12  # wal1+wal2+walb

    # day and delay adjustments
    forwardprice = price*(1+y)**((dayofmonth-1+30-delay)/30)
    cleanprice = forwardprice - coupon*(dayofmonth-1)/360

    waladjustment = (dayofmonth-1+30-delay)/360
    adjwal = wal - waladjustment
    adjmoddurn = moddurn - waladjustment/(1+beyield/200)

    if root is None:
        return (cleanprice, adjmoddurn, adjwal)
    else:
        return cleanprice - root


def bc35_yield(price, coupon, cpr, age, origfixedterm, origterm, dayofmonth=1,
               delay=47, servicing_fee=0):
    # 47 is the market standard according to Goldman Sachs' loan trader
    result = optimize.root(bc35_price, coupon,
                           args=(coupon, cpr, age, origfixedterm,
                                 origterm, dayofmonth, delay,
                                 servicing_fee, price), method='df-sane')

    try:
        # if result.x is a scalar
        # if result.x is np.array or pd.Series, then float returns a TypeError
        return float(result.x)
    except TypeError:
        return result.x
