import numpy as np
# import pandas as pd  # pandas is only used to collate numpy arrays for summary purposes
# from pandicake.pandaslite import FastFrame
import numpy_financial as npf


def make_smm_array(smm, nper: int) -> np.array:
    """
    Specific the first few smm values to produce a numpy array of length nper.
    This is similar to Bloomberg's custom vectors.

    Parameters
    ----------
    smm : scalar or array_like
        The first
    nper : int
        The number of period of the resulting numpy array

    Returns
    -------
    out : ndarray, float
        A numpy array of length nper
    """
    if type(smm) == list:
        smm = np.array(smm)
    if type(smm) != np.ndarray:  # i.e., float or int
        np_smm = np.repeat(smm, nper)
    elif len(smm) < nper:  # i.e., only the first n periods are specified
        last_value = float(smm[-1:])
        tmp_smm = np.repeat(last_value, nper)
        np_smm = np.append(smm, tmp_smm[len(smm):])
    else:
        np_smm = smm
    return np_smm


def mortgage_cashflows(rate, nper, upb=1000000, smm=1-(1-15/100)**(1/12), sfee=0.0, pandi=None, pmt_only=False):
    """
    Produces an array representing repline cash flows.

    :param rate: The note rate of the mortgage
    :param nper: number of periods e.g., 360 is typical for a new mortgage
    :param upb: current unpaid principal balance
    :param smm: single month mortality rate
    :param current_pandi: optional parameter to specify P&I (for prior curtailments)
    :param return_frame: collates each numpy array and returns a pandas.DataFrame object
    :return: The monthly cash flows of a mortgage repline as a numpy array

    Notes:
    numpy is ~10x faster than the equivalent steps in pandas
    """
    monthly_rate = rate/1200
    monthly_sfee = sfee/1200
    # smm = 1 - (1-cpr/100)**(1/12)  # This is fairly slow if in a vector

    if pandi == None:
        pandi = npf.pmt(rate=monthly_rate, nper=nper, pv=-upb)
    np_smm = make_smm_array(smm, nper)

    np_period = np.arange(nper)
    np_zero_smm_bal = -npf.pv(monthly_rate, nper-np_period, pandi)
    np_period_factor = 1 - np_smm
    np_factor = np_period_factor.cumprod()
    np_factor = np.insert(np_factor, 0, 1)[:-1]
    np_upb = np_factor * np_zero_smm_bal
    np_pandi = npf.pmt(monthly_rate, nper-np_period, -np_upb) - monthly_sfee*np_upb
    np_ipmt = (monthly_rate - monthly_sfee)*np_upb
    np_ppmt = np_pandi - np_ipmt
    np_upmt = (np_upb - np_ppmt)*(1-np_period_factor)
    # np_end_bal = np_upb - np_ppmt - np_upmt  # This should be a test
    np_pmt = np_pandi + np_upmt
    if not pmt_only:
        # np_cpr = 100*(1-(1-np_smm)**12)
        # data = {
        #     # 'smm': np_smm,
        #     'cpr': np_cpr,
        #     'upb': np_upb,
        #     'pmt': np_pmt,
        #     'ipmt': np_ipmt,
        #     'ppmt': np_ppmt,
        #     'upmt': np_upmt,
        # }
        # arr = np.column_stack(tuple(data.values()))
        # return arr
        # return FastFrame(data)
        return np.column_stack((np_upb, np_ipmt, np_ppmt, np_upmt, np_pmt))
    else:
        return np_pmt

################################################################################
# This section is UNDER CONSTRUCTION
# def repline_cashflows(rate, nper, upb, cpr=0.00, sfee=0.0, pandi=None, to_frame=True):
#     return repline_cashflows_monthly(rate/1200, nper, upb,
#             smm=1-(1-cpr/100)**(1/12), monthly_sfee=sfee/1200, pandi=pandi, to_frame=to_frame)

def add_zeros_to_array(array, target_row_count=480):
    """I believe this adds zeros to avoid errors e.g., 30yr loan vs 40yr loan"""
    target_row_count = int(target_row_count)  # error without this
    row_count = np.ma.size(array, axis=0)
    col_count = np.ma.size(array, axis=1)
    additional_rows = target_row_count - row_count
    one_row = np.repeat(0, col_count)
    empty_rows = np.tile(one_row, (additional_rows, 1))
    new_array = np.append(array, empty_rows, axis=0)
    return new_array


def pool_cashflows(rate: np.ndarray, nper: np.ndarray, upb: np.ndarray,
                         smm: np.ndarray, sfee: np.ndarray, pandi: np.ndarray):
    """This produces cash flows for more than 1 loan"""
    # def repline_cashflows(rate, nper, upb=1000000, smm=1-(1-15/100)**(1/12), sfee=0.0, pandi=None, pmt_only=False):
    loan_count = len(rate)
    max_nper = nper.max()
    for j in range(loan_count):
        thispmt = mortgage_cashflows(rate[j], nper[j], upb[j], smm[j], sfee[j], pandi[j])
        thispmt = add_zeros_to_array(thispmt, max_nper)
        if j == 0:
            pmt = thispmt
        else:
            pmt += thispmt
    return pmt
