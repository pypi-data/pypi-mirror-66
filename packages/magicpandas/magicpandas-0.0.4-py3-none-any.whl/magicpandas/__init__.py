import types
import functools
import pandas
from .frame import MagicDataFrame, MagicSeries


def magicpandify(func):
    """If an imported function returns DataFrame/Series, return
    a MagicDataFrame/MagicSeries instead"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        pandas_return_value = func(*args, **kwargs)
        if isinstance(pandas_return_value, pandas.DataFrame):
            return MagicDataFrame(pandas_return_value)
        elif isinstance(pandas_return_value, pandas.Series):
            return MagicSeries(pandas_return_value)
        else:
            return pandas_return_value
    return wrapper


def decorate_all_in_module(module, decorator):
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, types.FunctionType):
            setattr(module, name, decorator(obj))


decorate_all_in_module(pandas, magicpandify)
# 3 options with base classes: monkey patch or delete or leave unchanged
# pandas.DataFrame = MagicDataFrame
# pandas.Series = MagicSeries
# del pandas.DataFrame
# del pandas.Series
from pandas import *  # This has to come after decorate_all_in_module
