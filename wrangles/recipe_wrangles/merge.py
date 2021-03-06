"""
Functions to merge data from one or more columns into a single column
"""
import pandas as _pd
from .. import format as _format
from typing import Union as _Union
import fnmatch as _fnmatch


def coalesce(df: _pd.DataFrame, input: list, output: str) -> _pd.DataFrame:
    """
    type: object
    description: Take the first non-empty value from a series of columns
    additionalProperties: false
    required:
      - input
      - output
    properties:
      input:
        type: array
        description: List of input columns
      output:
        type: string
        description: Name of the output columns
    """
    # NOTE: cleaner implementations that I've found implemented directly in pandas do not work with empty strings
    # If a better solution found, replace but ensure it works with all falsy values in python
    df[output] = _format.coalesce(df[input].fillna('').values.tolist())
    return df


def concatenate(df: _pd.DataFrame, input: _Union[str, list], output: str, char: str = ',') -> _pd.DataFrame:
    """
    type: object
    description: Concatenate a list of columns or a list within a single column
    additionalProperties: false
    required:
      - input
      - output
      - char
    properties:
      input:
        type: 
          - array
          - string
        description: Either a single column name or list of columns
      output:
        type: string
        description: Name of the output column
      char:
        type: string
        description: (Optional) Character to add between successive values
    """
    if isinstance(input, str):
        df[output] = _format.join_list(df[input].tolist(), char)
    elif isinstance(input, list):
        df[output] = _format.concatenate(df[input].astype(str).values.tolist(), char)
    else:
        raise ValueError('Unexpected data type for merge.concatenate / input')
    return df


def lists(df: _pd.DataFrame, input: list, output: str, remove_duplicates: bool = False) -> _pd.DataFrame:
    """
    type: object
    description: Take lists in multiple columns and merge them to a single list
    additionalProperties: false
    required:
      - input
      - output
    properties:
      input:
        type: array
        description: List of input columns
      output:
        type: string
        description: Name of the output column
      remove_duplicates:
        type: boolean
        description: Whether to remove duplicates from the created list
    """
    output_list = []
    for row in df[input].values.tolist():
        output_row = []
        for col in row:
            if not isinstance(col, list): col = [str(col)]
            output_row += col
        # Use dict.fromkeys over set to preserve input order
        if remove_duplicates: output_row = list(dict.fromkeys(output_row))
        output_list.append(output_row)
    df[output] = output_list
    return df


def to_list(df: _pd.DataFrame, input: list, output: str, include_empty: bool = False) -> _pd.DataFrame:
    """
    type: object
    description: Take multiple columns and merge them to a list
    additionalProperties: false
    required:
      - input
      - output
    properties:
      input:
        type: array
        description: List of input columns
      output:
        type: string
        description: Name of the output column
      include_empty:
        type: boolean
        description: Whether to include empty columns in the created list
    """
    output_list = []
    for row in df[input].values.tolist():
        output_row = []
        for col in row:
            if col or include_empty: output_row.append(col)
        output_list.append(output_row)
    df[output] = output_list
    return df


def to_dict(df: _pd.DataFrame, input: list, output: str, include_empty: bool = False) -> _pd.DataFrame:
    """
    type: object
    description: Take multiple columns and merge them to a dictionary (aka object) using the column headers as keys
    additionalProperties: false
    required:
      - input
      - output
    properties:
      input:
        type: array
        description: List of input columns
      output:
        type: string
        description: Name of the output column
      include_empty:
        type: boolean
        description: Whether to include empty columns in the created dictionary
    """
    output_list = []
    column_headers = df[input].columns
    for row in df[input].values.tolist():
        output_dict = {}
        for col, header in zip(row, column_headers):
            if col or include_empty: output_dict[header] = col
        output_list.append(output_dict)
    df[output] = output_list
    return df


def key_value_pairs(df: _pd.DataFrame, input: dict, output: str) -> _pd.DataFrame:
    """
    type: object
    description: Create a dictionary from keys and values in paired columns e.g. COLUMN_NAME_1, COLUMN_VALUE_1, COLUMN_NAME_2, COLUMN_VALUE_2 ...
    additionalProperties: false
    required:
      - input
      - output
    properties:
      input:
        type: object
        description: Matched pairs of key and value columns
      output:
        type: string
        description: Name of the output column
    """
    pairs = {}

    # If user has used wildcards, expand out
    for key, val in input.items():
        if '*' in key and '*' in val:
            key_columns = _fnmatch.filter(df.columns, key)
            val_columns = _fnmatch.filter(df.columns, val)
            for key_col, val_col in zip(key_columns, val_columns):
                pairs[key_col] = val_col
        else:
            pairs[key] = val

    results = [{} for _ in range(len(df))]

    idx = 0
    for row in df.to_dict('records'):
      for key, val in pairs.items():
            if row[key] and row[val]:
                results[idx][row[key]] = row[val]
      idx+=1

    df[output] = results

    return df