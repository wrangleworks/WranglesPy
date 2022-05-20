"""
Functions to create new columns
"""
import pandas as _pd
import uuid as _uuid
import numpy as _np
from typing import Union as _Union


def column(df: _pd.DataFrame, output: _Union[str, list], parameters: dict = {}) -> _pd.DataFrame:
    """
    Create column(s) with a user defined value. Defaults to None (empty).

    ```
    wrangles:
      - create.column:
          output: new column
          value: my value        # Optional
    ```

    :param df: Input Dataframe
    :param output: Name or list of names of new columns
    :param value: (Optional) Value to add in the new column(s). If omitted, defaults to None.
    """
    # If a string provided, convert to list
    if isinstance(output, str): output = [output]

    # Loop through and create new columns
    for output_column in output:
        df[output_column] = parameters.get('value', None)

    return df


def guid(df: _pd.DataFrame, output: _Union[str, list]) -> _pd.DataFrame:
    """
    Create column(s) with a GUID

    ```
    wrangles:
      - create.guid:
          output: new column
    ```

    :param df: Input Dataframe
    :param output: Name or list of names of new columns
    """
    return uuid(df, output)


def index(df: _pd.DataFrame, output: _Union[str, list], parameters: dict = {}) -> _pd.DataFrame:
    """
    Create column(s) with an incremental index.

    ```
    wrangles:
      - create.index:
          output: new column
          start: 1                  # Optional
          step: 1                   # Optional

    :param df: Input Dataframe
    :param output: Name or list of names for new column(s)
    :param start: (Optional; default 1) Starting number for the index
    :param step: (Optional; default 1) Step between successive rows
    ```
    """
    # Get start number if provided, default 1
    start = parameters.get('start', 1)

    # If a string provided, convert to list
    if isinstance(output, str): output = [output]

    # Loop through and create incremental index
    for output_column in output:
        df[output_column] = _np.arange(start, len(df) * parameters.get('step', 1) + start, step=parameters.get('step', 1))

    return df


def uuid(df: _pd.DataFrame, output: _Union[str, list]) -> _pd.DataFrame:
    """
    Create column(s) with a UUID

    ```
    wrangles:
      - create.uuid:
          output: new column
    ```

    :param df: Input Dataframe
    :param output: Name or list of names of new columns
    """
    # If a string provided, convert to list
    if isinstance(output, str): output = [output]

    # Loop through and create uuid for all requested columns
    for output_column in output:
        df[output_column] = [_uuid.uuid4() for _ in range(len(df.index))]

    return df