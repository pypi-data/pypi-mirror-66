import numpy as np
import numpy_financial as npf
from scipy import optimize
import warnings


def pv(irr: float, np_pmt, root=0):
    """
    Compute the present value of a stream of cash flows.
    Motivation: Unlike numpy_financial.npv, numpy_financial.pv doesn't support
        an arbitrary stream of cash flows.

    Parameters
    ----------
    irr : float
        Internal rate of return
    np_pmt : array_like
        A stream of cash flows
    root : float
        Used to invert the equation via optimize.root

    Returns
    -------
    float
        The present value of a stream of cash flows.
    """
    np_pmt = np.insert(np_pmt, 0, 0)
    pv = npf.npv(irr, np_pmt)
    return pv - root


def irr(presentvalue, np_pmt, use_scipy_optimize_root=True):
    """
    Return the Internal Rate of Return (IRR) of a stream of cash flows.

    Parameters
    ----------
    presentvalue : float
        The known present value of a stream of cash flows.
    np_pmt : array_like
        A stream of cash flows.
    use_scipy_optimize_root : bool
        If True, solvse for the IRR using scipy.optimize.root instead of
        numpy_financial.irr.

    Returns
    -------
    float
        Internal Rate of Return a stream of cash flows.

    Notes
    -----
    Note that the API is different than numpy_financial.irr.  Contains an option
    to solve for the IRR using scipy.optimize.root rather than
    numpy_financial.irr.  scipy.optimize.root with df-sane is typically much
    faster than numpy_financial.irr.
    """
    import warnings

    if use_scipy_optimize_root:
        with warnings.catch_warnings():
            # Original warning: numpy_financial\_financial.py:781:
            # RuntimeWarning: overflow encountered in power
            # return (values / (1+rate)**np.arange(0, len(values))).sum(axis=0)
            warnings.simplefilter('ignore')
            result = optimize.root(pv, 0, args=(np_pmt, presentvalue), method='df-sane')
        return result.x
    else:
        np_pmt = np.insert(np_pmt, 0, -presentvalue)
        irr = npf.irr(np_pmt)
        return irr


def mortgage_price(beyield, coupon, upb, np_pmt, dayofmonth=1,delay=47, root=0):
    """
    Compute the price of a mortgage loan or mortgage pool for an arbitary set
    of cash flows.

    Parameters
    ----------
    beyield : float
        The bond equivalent yield of a mortgage cash flow stream.
    coupon : float
        The annualized coupon of the pool.
    upb : float
        The unpaid principal balance of the mortgage pool.
    np_pmt : array_like
        A stream of monthly cash flows.
    dayofmonth : int
        The setlement date's day of month for clean price calculations.
    delay : int
        The cash flow delay assumption common in mortgage pool and mortgage
        backed security pricing.
    root : float
        Used to invert the equation via optimize.root.

    Returns
    -------
    float
        The price of the mortgage pool.

    Notes
    -----
    47 day delay is the market standard for loan trades according to Goldman
    Sachs' trading desk
    """
    monthly_coupon = coupon/1200
    irr = ((1+beyield/200)**(1/6)-1)
    dirty_price = pv(irr, np_pmt)/upb*100
    forward_price = dirty_price*(1+irr)**((dayofmonth-1+30-delay)/30)
    clean_price = forward_price - monthly_coupon*(dayofmonth-1)/360
    return clean_price - root


def mortgage_yield(price, coupon, upb, np_pmt, dayofmonth=1, delay=47):
    """
    Compute the price of a mortgage loan or mortgage pool for an arbitary set
    of cash flows.

    Parameters
    ----------
    price : float
        The price of a mortgage cash flow stream.
    coupon : float
        The annualized coupon of the pool.
    upb : float
        The unpaid principal balance of the mortgage pool.
    np_pmt : array_like
        A stream of monthly cash flows.
    dayofmonth : int
        The setlement date's day of month for clean price calculations.
    delay : int
        The cash flow delay assumption common in mortgage pool and mortgage
        backed security pricing.

    Returns
    -------
    float
        The price of the mortgage pool.

    Notes
    -----
    47 day delay is the market standard for loan trades according to Goldman
    Sachs' trading desk
    """
    result = optimize.root(mortgage_price, coupon,
                           args=(coupon, upb, np_pmt, dayofmonth, delay, price),
                           method='df-sane')
    return result.x
