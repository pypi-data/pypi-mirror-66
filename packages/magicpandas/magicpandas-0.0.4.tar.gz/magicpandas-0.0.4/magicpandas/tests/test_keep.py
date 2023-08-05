from magicpandas.frame import MagicDataFrame
import warnings
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    import statsmodels.api as sm


def test_keep():
    df = sm.datasets.get_rdataset("Duncan", "carData").data
    df = MagicDataFrame(df)
    df = df.keep('*e', axis=1)
    assert list(df.columns) == ['type', 'income', 'prestige']
    assert len(df.columns) == 3
