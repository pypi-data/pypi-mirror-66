from __future__ import annotations
import subprocess
import os
import re
import warnings
import numpy as np
import pandas as pd
import functools
from magicpandas.utils import search_iterable
from magicpandas.easy_xlsxwriter import easy_xlsxwriter
import altair as alt
from magicpandas.chromify import chromify
from magicpandas.finance.bc35 import bc35_price, bc35_yield
import inspect


def preserve_magic_attributes(func, magic_attributes=[
    'verbose_labels'
]):
    """Decorator to preserve DataFrame object attributes when running a
    MagicDataFrame method."""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        # if isinstance(self, MagicDataFrame) or isinstance(self, MagicSeries):
        if issubclass(self.__class__, MagicDataFrame) or issubclass(self.__class__, MagicSeries):
            result = func(self, *args, **kwargs)
            # if isinstance(result, MagicDataFrame) or isinstance(result, MagicSeries):
            if issubclass(result.__class__, MagicDataFrame) or isinstance(result.__class__, MagicSeries):
                for magic_attribute in magic_attributes:
                    if hasattr(self, magic_attribute):
                        with warnings.catch_warnings():
                            warnings.simplefilter('ignore')
                            setattr(result, magic_attribute, getattr(self, magic_attribute))
            return result
        else:
            return func(self, *args, **kwargs)
    return wrapper


def for_all_methods(decorator, exclude=[None]):
    """A class decorator that decorates all methods with the same decorator,
    excluding dunder methods.

    References
    ----------
    https://stackoverflow.com/questions/6307761/how-to-decorate-all-functions-of-a-class-without-typing-it-over-and-over-for-eac
    """
    def decorate(cls):
        for attr in inspect.getmembers(cls, inspect.isfunction):
            # print(attr[0])
            # if attr[0] not in exclude:
            if attr[0] not in exclude and not re.match('^__.*__$', attr[0]):
                setattr(cls, attr[0], decorator(getattr(cls, attr[0])))
        return cls
    return decorate


class MagicSeries(pd.Series):
    @property
    def _constructor(self):
        return MagicSeries

    @property
    def _constructor_expanddim(self):
        return MagicDataFrame

    def pcut(self, step_size: float = None, bin_count: int = None,
             right: bool = True, format: str = '{:3.2f}') -> MagicSeries:
        """Pretty cut
        Converts MagicSeries of dtype float or int into a ordinal MagicSeries of
        dtype category that is formatted in a manner suitable for publishing in
        non-scientific contexts e.g., "1.001 - 2.000" vs (1.001, 2.000].

        Parameters
        ----------
        step_size : float
            The desired number of steps.  Note: must be None if bin_count is
            not None.
        bin_count : int
            The desired number of bins.  Note: must be None if step_size is
            not None.
        right : bool
            Indicates whether bins includes the rightmost edge or not.
        format : str
            Python style format string e.g., {:3.2f}

        Returns
        -------
        Categorical MagicSeries
            A MagicSeries representing the respective bin for each value of self.
        """
        if not self.dtype == 'float' and not self.dtype == 'int':
            raise TypeError('MagicSeries must of dtype float or int')

        if step_size is not None and bin_count is not None:
            raise ValueError('step_size is not None and bin_count is not None')
        elif step_size is None and bin_count is None:
            raise ValueError('step_size is None and bin_count is None')

        if bin_count is not None:
            step_size = (self.max() - self.min()) / (bin_count-1)
            step_size = round(step_size, 10)

        thisformat = format.replace('{:', '{0:') + ' - ' + format.replace('{:', '{1:')  # e.g., "{0:3.1f} - {1:3.1f}"
        delta = 1/10**int(re.findall(r'\.\d+', format)[0].replace('.', ''))  # e.g., 0.01

        minvalue = int(self.min()/step_size)*step_size
        maxvalue = int(self.max()/step_size+1)*step_size

        if right:
            bin_labels = [thisformat.format(i + delta, i + step_size) for i in
                          np.arange(minvalue, maxvalue, step_size)]
            bin_labels[0] = thisformat.format(minvalue, minvalue+step_size)
        else:
            bin_labels = [thisformat.format(i, i + step_size - delta) for i in
                          np.arange(minvalue, maxvalue, step_size)]

        return pd.cut(self, np.arange(minvalue, maxvalue+step_size, step_size),
                      right=right, labels=bin_labels, include_lowest=True)


# @for_all_methods(preserve_magic_attributes, ['__init__'])
@for_all_methods(preserve_magic_attributes)
class MagicDataFrame(pd.DataFrame):
    ############################################################################
    # methods to extend pandas.DataFrame
    ############################################################################
    @property
    def _constructor(self):
        return MagicDataFrame

    @property
    def _constructor_sliced(self):
        return MagicSeries

    ############################################################################
    # methods to set MagicDataFrame attributes e.g., verbose_labels
    ############################################################################
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, 'verbose_labels'):
            with warnings.catch_warnings():
                # warning message: Pandas doesn't allow columns to be created via a new attribute name
                warnings.simplefilter("ignore")
                self.verbose_labels = {x: x for x in self.columns}  # By default, labels are the same as the column names

    # def set_verbose_labels(self, new_verbose_labels: dict) -> None:
    #     """Modify labels"""
    #     self.verbose_labels.update(new_verbose_labels)
    #
    # def clear_verbose_labels(self):
    #     """Clear all labels i.e., set labels to column name"""
    #     self.verbose_labels = {x: x for x in self.columns}  # By default, labels are the same as the column names

    ############################################################################
    # methods which enhance the utility of existing DataFrame methods
    ############################################################################
    def drop(self, labels=None, axis=0, index=None, columns=None, level=None, inplace=False, errors="raise"):
        try:
            return super().drop(labels, axis, index, columns, level, inplace, errors)
        except KeyError as e:
            if str(e)[-18:-1] == "not found in axis":  # make sure it's not some other KeyError
                if labels and axis == 0:
                    labels = search_iterable(self.index, labels)
                elif labels and axis == 1:
                    labels = search_iterable(self.columns, labels)
                elif index:
                    index = search_iterable(self.index, index)
                elif columns:
                    columns = search_iterable(self.columns, columns)
                else:
                    raise KeyError(e)
            return super().drop(labels, axis, index, columns, level, inplace, errors)

    ############################################################################
    # New methods for data wrangling
    ############################################################################
    def keep(self, labels=None, axis=0, index=None, columns=None, level=None, inplace=False, errors="raise"):
        try:
            # test is labels, index, columns are accepted per pandas.DataFrame.drop
            super().drop(labels, axis, index, columns, level, inplace, errors)
            # if it is acceptable, then invert the list
            if labels and axis == 0:
                if type(labels) == str: labels = [labels]
                labels = [x for x in self.index if x not in labels]
            elif labels and axis == 1:
                if type(labels) == str: labels = [labels]
                labels = [x for x in self.columns if x not in labels]
            elif index:
                if type(index) == str: index = [index]
                index = [x for x in self.index if x not in index]
            elif columns:
                if type(columns) == str: columns = [columns]
                columns = [x for x in self.columns if x not in columns]
            else:
                raise KeyError(e)
            return super().drop(labels, axis, index, columns, level, inplace, errors)  # test is labels, index, columns are accepted per pandas.DataFrame.drop
        except KeyError as e:
            if str(e)[-18:-1] == "not found in axis":  # make sure it's not some other KeyError
                if labels and axis == 0:
                    labels = search_iterable(self.index, labels, subtract=True)
                elif labels and axis == 1:
                    labels = search_iterable(self.columns, labels, subtract=True)
                elif index:
                    index = search_iterable(self.index, index, subtract=True)
                elif columns:
                    columns = search_iterable(self.columns, columns, subtract=True)
                else:
                    raise KeyError(e)
            return super().drop(labels, axis, index, columns, level, inplace, errors)

    def gsort(self, varlist):
        """Implements Stata's gsort command
        Note Stata's different interpretation of the minus sign here
        Hence _parse_varlist isn't used

        >>> df.gsort('origfico -origltv')
        """
        df = self  # originally written as a function
        if type(varlist) == str:
            varlist = varlist.split()
        ascending_list =[]
        new_varlist = []
        for x in varlist:
            if x[:1]=='-':
                new_varlist.append(x[1:])
                ascending_list.append(False)
            elif x[:1]=='+':
                new_varlist.append(x[1:])
                ascending_list.append(True)
            else:
                new_varlist.append(x)
                ascending_list.append(True)
        return df.sort_values(new_varlist, ascending=ascending_list)  # .reset_index(drop=True)

    def order(self, varlist, refvar=None, after=True, last=False):
        """
        For whatever reason, it isn't that simple to order columns in pandas.
        This method corrects that.  Note: This currently only supports column
        ordering.

        Parameters
        ----------
        varlist : single label or list-like or magicpandas search string
            The columns to order.
        refvar str, default None
            A reference column e.g., to order after or before refvar
        after : bool, default True
            If True, order after the refvar
        last : bool, default False
            If True, place ordered columns at the end of the dataframe

        Returns
        -------
        MagicDataFrame
            DataFrame with ordered columns.
        """
        df = self
        if type(varlist) == str:
            varlist = varlist.split()
        # varlist = df._parse_varlist(varlist)
        varlist = search_iterable(df, varlist)

        assert type(after) == bool
        assert type(last) == bool
        assert last is False or refvar is None, \
            'last and refvar options cannot be use simultaneously'

        therest = [x for x in list(df.columns) if x not in varlist]

        if refvar is None:
            if len(therest) != 0:
                refvar = therest[0]
            after = False

        if last is True:
            after = True
            refvar = therest[-1]

        if len(therest) != 0:
            colnum = list(therest).index(refvar)
        else:
            colnum = 0

        if after is False:
            head = therest[:colnum]
            tail = therest[colnum:]
        else:
            head = therest[:colnum+1]
            tail = therest[colnum+1:]

        newlist = head
        newlist.extend(varlist)
        newlist.extend(tail)
        df = df[newlist]
        return df

    def weighted_average(self, weight=None, group_by=None):
        df = self.copy()

        if weight:
            if weight not in self.columns:
                raise ValueError(f'"f{weight}" is not a column in DataFrame object.')
            elif not self[weight].dtype == 'float' and not self[weight].dtype == 'int':
                raise TypeError(f'Column "{weight}" must be a float or int data type.')
            elif not isinstance(weight, str):
                raise TypeError(f'"weight" must be a string and refer to a column name.')
        else:
            weight = '__weight__'
            df[weight] = 1

        if group_by:
            if group_by not in self.columns:
                raise ValueError(f'"{group_by}" is not a column in DataFrame object.')
            elif self[group_by].dtype == 'float' or self[group_by].dtype == 'int':
                raise TypeError(f'Column "{group_by}" cannot be a float or int data type.')
            elif not isinstance(group_by, str):
                raise TypeError(f'"group_by" must be a string and refer to a column name.')
        else:
            group_by = '__groupby__'
            df[group_by] = ''

        weight_and_groupby_df = df[[weight, group_by]]
        weight_and_groupby_df = weight_and_groupby_df.groupby(group_by).sum()
        df = pd.merge(df, weight_and_groupby_df, how='left',
                      left_on=group_by, right_index=True,
                      suffixes=('', '_groupby_sum'))
        df[weight] = df[weight] / df[f"{weight}_groupby_sum"]
        del df[f"{weight}_groupby_sum"]
        weight_series = df[weight]
        groupby_series = df[group_by]
        df = df.drop([weight, group_by], axis=1)
        df_times_weights = df.apply(lambda x: x*weight_series)
        df_times_weights[group_by] = groupby_series
        final_grouped = df_times_weights.groupby(group_by)
        # df = df_times_weights.groupby(group_by).sum()
        df = final_grouped.sum()

        # cleanup
        if group_by == '__groupby__':
            df.index.name = ''

        # print(self.verbose_labels)
        # print(self.verbose_labels)
        # print(self.verbose_labels)
        # return MagicDataFrame(df, magic_frame_to_emulate=self)  # needed because groupby doesn't preserve object attributes
        return df

    # def srecode(self, varname, binsizes, right_columns, pyformats):
    #     """Implements Sean's srecode in Python
    #     Note: inplace=True is the default
    #
    #     step_size: default step_size
    #     """
    #     # TODO: convert to inplace=False to conform to pandas
    #     df = self
    #
    #     if varname in right_columns:
    #         right = True
    #     else:
    #         right = False
    #
    #     step_size = binsizes[varname]
    #
    #     fmt = pyformats[varname]  # e.g., {:3.2f}
    #     thisformat = fmt.replace('{:', '{0:') + ' - ' + fmt.replace('{:', '{1:')  # e.g., "{0:3.1f} - {1:3.1f}"
    #     delta = 1/10**int(re.findall(r'\.\d+', fmt)[0].replace('.', ''))  # e.g., 0.01
    #
    #     minvalue = int(df[varname].min()/step_size)*step_size
    #     maxvalue = int(df[varname].max()/step_size+1)*step_size
    #
    #     if right:
    #         bin_labels = [thisformat.format(i+delta, i+step_size) for i in np.arange(minvalue, maxvalue, step_size)]
    #         bin_labels[0] = thisformat.format(minvalue, minvalue+step_size)
    #     else:
    #         bin_labels = [thisformat.format(i, i+step_size-delta) for i in np.arange(minvalue, maxvalue, step_size)]
    #
    #     df['_'+varname] = pd.cut(self[varname], np.arange(minvalue, maxvalue+step_size, step_size), right=right, labels=bin_labels, include_lowest=True)
    #     # self['_' + varname] = self['_'+varname].cat.remove_unused_categories()
    #     # varlbl = labels.get(varname, None)
    #     # if varlbl :
    #     #     labels['_'+varname] = varlbl
    #     return df

    ############################################################################
    # New methods that support finance calculations e.g., IRR
    ############################################################################
    def bc35_price_gen(self, beyield='beyield', coupon='coupon', cpr='cpr',
                       age='age', origfixedterm='origfixedterm',
                       origterm='origterm', dayofmonth=1, delay=47,
                       servicing_fee='servicing_fee', price='price',
                       moodurn='moddurn', wal='wal'):
        cleanprice, adjmoddurn, adjwal = \
            bc35_price(beyield=self[beyield], coupon=self[coupon],
                       cpr=self[cpr], age=self[age],
                       origfixedterm=self[origfixedterm],
                       origterm=self[origterm], dayofmonth=dayofmonth,
                       delay=delay, servicing_fee=self[servicing_fee])
        df = self.copy()
        df[price] = MagicSeries(cleanprice)
        df[moodurn] = MagicSeries(adjmoddurn)
        df[wal] = MagicSeries(adjwal)
        return df

    def bc35_yield_gen(self, price='price', coupon='coupon', cpr='cpr',
                       age='age', origfixedterm='origfixedterm',
                       origterm='origterm', dayofmonth=1, delay=47,
                       servicing_fee='servicing_fee', beyield='beyield'):
        beyield_array = \
            bc35_yield(price=self[price], coupon=self[coupon],
                       cpr=self[cpr], age=self[age],
                       origfixedterm=self[origfixedterm],
                       origterm=self[origterm], dayofmonth=dayofmonth,
                       delay=delay, servicing_fee=self[servicing_fee])
        df = self.copy()
        df[beyield] = MagicSeries(beyield_array)
        return df
    ############################################################################
    # New methods that support I/O and visualization
    ############################################################################
    def browse(self, path: str = None, limit: int = None, run: bool = True,
               percentage_columns: list = None, autofit_columns: list = None,
               client: str = 'excel') -> None:
        if client == "excel":
            easy_xlsxwriter(self, path, limit, run, percentage_columns, autofit_columns)
        elif client == "webbrowser":
            # UNDER CONSTRUCTION
            from magicpandas.chromify import chromify
            chromify(self.to_html(), path, run)
        else:
            raise ValueError('Argument "client" must be either excel or webbrowser')

    def inspect_for_django(self, model_name='DjangoModel'):
        result = ''
        for label, verbose_label in self.verbose_labels.items():
            try:
                if self.dtypes[label] == 'object':  # i.e., a string
                    result += f"""    {label} = models.CharField(max_length=255, verbose_name="{verbose_label}", null=True)\n"""
                elif self.dtypes[label] == 'float64':
                    result += f"""    {label} = models.FloatField(verbose_name="{verbose_label}", null=True)\n"""
                elif self.dtypes[label] == 'datetime64[ns]':
                    result += f"""    {label} = models.DateField(verbose_name="{verbose_label}", null=True)\n"""
                elif self.dtypes[label] == 'bool':
                    result += f"""    {label} = models.BooleanField(verbose_name="{verbose_label}", null=True)\n"""
                elif self.dtypes[label] == 'int64':
                    result += f"""    {label} = models.BigIntegerField(verbose_name="{verbose_label}", null=True)\n"""
                else:
                    raise Exception(f"{label}: There is currently no support for type {self.dtypes[label]}")
            except KeyError as e:
                import warnings
                warnings.warn(f"{label} appears to be in the key file but not in the data file.", stacklevel=2)
        print(f'class {model_name}(models.Model):')
        print(result)

    def to_django(self, DjangoModel, if_exists='fail'):
        """Uses bulk_create to insert data to Django table
        if_exists: see pd.DataFrame.to_sql API

        Ref: https://www.webforefront.com/django/multiplemodelrecords.html
        """
        # TODO: How to I test this?
        if not if_exists in ['fail', 'replace', 'append']:
            raise Exception('if_exists must be fail, replace or append')

        if if_exists=="replace":
            DjangoModel.objects.all().delete()
        elif if_exists=="fail":
            if DjangoModel.objects.all().count()>0:
                raise ValueError('Data already exists in this table')
        else:
            pass

        dct = self.replace({np.nan: None}).to_dict('records') # replace NaN with None since Django doesn't understand NaN

        bulk_list = []
        for x in dct:
            bulk_list.append(DjangoModel(**x))
        DjangoModel.objects.bulk_create(bulk_list)
        print('Successfully saved DataFrame to Django table.')

    def get_dtype_dict(self):
        """
        Returns
        -------
        dict
            Return a dictionary whose keys are column types and values are a
            list containing column labels corresponding to that data type.

        Note: orginally developed for graph(), but no longer used
        """
        dtype_dict = {}
        column_types = self.dtypes.apply(lambda x: str(x)).to_dict()
        for column_label, column_type in column_types.items():
            if dtype_dict.get(column_type, None):
                list_of_columns = dtype_dict.get(column_type, None)
                list_of_columns.append(column_label)
                dtype_dict.update({column_type: list_of_columns})
            else:
                dtype_dict.update({column_type: [column_label]})
        return dtype_dict

    def graph(self, columns=None, mark='circle', facet_columns=1000, run=True):
        """
        Inspired by https://www.youtube.com/watch?v=vTingdk_pVM&t=1260s
        Imposes a clear hierarchy of encodings to make graphing as simple as df.graph()

        Five encodings are supported:
        1) x axis (Q or N)
        2) y axis (Q or N)
        3) facet (Q or N)
        4) size (Q or N)
        5) color (Q or N)
        """
        if not columns:
            columns = list(self.columns)
        if type(columns) == str:
            columns = search_iterable(self.columns, columns)
        df = self[columns].rename(columns=self.verbose_labels)

        encoding_dict = {}
        encoding_list = ['x', 'y', 'facet', 'size', 'color']
        column_list = list(df.columns)
        for i in range(len(column_list)):
            if len(encoding_list) > 0:
                this_encoding = encoding_list.pop(0)
                this_column = column_list.pop(0)
                if this_encoding == "facet":
                    encoding_dict.update({this_encoding: alt.Facet(this_column, columns=facet_columns)})
                elif this_encoding == "x":
                    encoding_dict.update({this_encoding: alt.X(this_column, scale=alt.Scale(zero=False))})
                elif this_encoding == "y":
                    encoding_dict.update({this_encoding: alt.Y(this_column, scale=alt.Scale(zero=False))})
                else:
                    encoding_dict.update({this_encoding: this_column})
            else:
                encoding_dict.update({'tooltip': column_list})
        print(encoding_dict)

        chart = alt.Chart(self)
        chart = getattr(chart, f'mark_{mark}')().encode(**encoding_dict).interactive()
        chromify(chart.to_html(), run=run)

    ############################################################################
    # Shortcut methods e.g., kord = keep & order
    ############################################################################
    def kord(self, varlist):  # , browser_sync=True):
        # keep & order
        df = self
        if type(varlist) == str:
            varlist = varlist.split()
        df = df.keep(varlist, axis=1).order(varlist)  # .reset_index(drop=True)
        return df
