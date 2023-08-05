from magicpandas.frame import MagicDataFrame
import os
import warnings
from contextlib import suppress
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    import statsmodels.api as sm


def test_graph():
    import tempfile
    path_to_check = os.path.join(tempfile.gettempdir(), 'magicpandas_chromify.html')
    with suppress(FileNotFoundError):
        os.remove(path_to_check)
    df = sm.datasets.get_rdataset("Duncan", "carData").data
    df = MagicDataFrame(df)
    df.graph(run=False)
    assert os.path.exists(path_to_check)
