"""
Create a test dataframe
"""
import pandas as _pd


_schema = {}


def read(rows: int, values: dict) -> _pd.DataFrame:
    """
    Create a test dataframe

    >>> from wrangles.connectors import test
    >>> df = test.read(rows=5, values={'header1':'a','header2':'b'})

    :param rows: Number of rows to include in the created dataframe
    :param values: Dictionary of header and fixed values
    :return: Pandas Dataframe of the created data
    """
    data = {}
    for key, val in values.items():
        data[key] = [val for _ in range(rows)]

    df = _pd.DataFrame(data)
    return df


_schema['read'] = """
type: object
description: Create a test dataframe
required:
  - rows
  - values
properties:
  rows:
    type: integer
    description: Number of rows to include in the generated dataframe
  values:
    type: string
    description: Dictionary of columns and values
"""