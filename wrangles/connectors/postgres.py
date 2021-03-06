"""
Connector to read/write from a PostgreSQL Database.
"""
import pandas as _pd
from typing import Union as _Union
import logging as _logging
import csv as _csv
from io import StringIO as _StringIO


_schema = {}


# Internal methods - custom sql callbacks 
def _psql_insert_copy(table, conn, keys, data_iter):
    """
    Execute SQL statement inserting data

    Parameters
    ----------
    table : pandas.io.sql.SQLTable
    conn : sqlalchemy.engine.Engine or sqlalchemy.engine.Connection
    keys : list of str
        Column names
    data_iter : Iterable that iterates the values to be inserted
    """
    # gets a DBAPI connection that can provide a cursor
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = _StringIO()
        writer = _csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ', '.join(['"{}"'.format(k) for k in keys])
        if table.schema:
            table_name = '{}.{}'.format(table.schema, table.name)
        else:
            table_name = table.name

        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)


# Public methods
def read(host: str, user: str, password: str, command: str, port = 5432, database: str = '', columns: _Union[str, list] = None) -> _pd.DataFrame:
    """
    Import data from a PostgreSQL database.

    >>> from wrangles.connectors import postgres
    >>> df = postgres.read(host='sql.domain', user='user', password='password', command='SELECT * FROM table')

    :param host: Hostname or IP of the database
    :param user: User with access to the database
    :param password: Password of user
    :param command: SQL command or table name
    :param port: (Optional) If not provided, the default port will be used
    :param database: (Optional) Database to be queried
    :param columns: (Optional) Subset of columns to be returned. This is less efficient than specifying in the SQL command.
    :return: Pandas Dataframe of the imported data
    """
    _logging.info(f": Importing Data :: {host}")

    conn = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    df = _pd.read_sql(command, conn)

    if columns is not None: df = df[columns]
    
    return df

_schema['read'] = """
type: object
description: Import data from a PostgreSQL Server
required:
  - host
  - user
  - password
  - command
properties:
  host:
    type: string
    description: Hostname or IP address of the server
  user:
    type: string
    description: The user to connect to the database with
  password:
    type: string
    description: Password for the specified user
  command:
    type: string
    description: Table name or SQL command to select data
  database:
    type: string
    description: The database to connect to
  port:
    type: integer
    description: The Port to connect to. Defaults to 5432.
  columns:
    type: array
    description: A list with a subset of the columns to import. This is less efficient than specifying in the command.
"""


def write(df: _pd.DataFrame, host: str, database: str, table: str, user: str, password: str, action = 'INSERT', port = 5432, columns: _Union[str, list] = None) -> None:
    """
    Export data to a PostgreSQL database.

    >>> from wrangles.connectors import postgres
    >>> postgres.write(df, host='sql.domain', database='database', table='table', user='user', password='password')

    :param df: Dataframe to be exported
    :param host: Hostname or IP of the database
    :param database: Database to be exported to
    :param table: Table to be exported to
    :param user: User with access to the database
    :param password: Password of user
    :param action: Only INSERT is supported at this time, defaults to INSERT
    :param port: (Optional) If not provided, the default port will be used
    :param columns: (Optional) Subset of the columns to be written. If not provided, all columns will be output
    """
    _logging.info(f": Exporting Data :: {host}/{table}")

    # Create appropriate connection string
    conn = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

    # Select only specific columns if user requests them
    if columns is not None: df = df[columns]

    if action.upper() == 'FAIL':
        df.to_sql(table, conn, if_exists='fail', index=False, method=_psql_insert_copy)
    elif action.upper() == 'REPLACE':
        df.to_sql(table, conn, if_exists='replace', index=False, method=_psql_insert_copy)
    elif action.upper() == 'EXPERIMENTAL':
        df.to_sql(table, conn, if_exists='append', index=False, method=_psql_insert_copy)
    elif action.upper() == 'INSERT':
        df.to_sql(table, conn, if_exists='append', index=False, method='multi', chunksize=1000)
    else:
        # TODO: Add UPDATE AND UPSERT
        raise ValueError('UPDATE and UPSERT are not implemented yet.') # pragma: no cover

_schema['write'] = """
type: object
description: Write data to a PostgreSQL Server
required:
  - host
  - user
  - password
  - database
  - table
properties:
  host:
    type: string
    description: Hostname or IP address of the server
  user:
    type: string
    description: The user to connect to the database with
  password:
    type: string
    description: Password for the specified user
  database:
    type: string
    description: The database to connect to
  table:
    type: string
    description: The name of the table to insert the data into
  port:
    type: integer
    description: The Port to connect to. Defaults to 5432.
  columns:
    type: array
    description: A list of the columns to write to the table. If omitted, all columns will be written.
"""