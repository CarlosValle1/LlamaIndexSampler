# parquethandler.py

import duckdb
from duckdb import DuckDBPyConnection
import pandas as pd


class ParquetHandler:

    def __init__(self, parquet_path: list):
        self.__conn: DuckDBPyConnection = duckdb.connect(':memory:')
        for path in parquet_path:
            self.__conn.execute(f"CREATE TABLE IF NOT EXISTS parquets AS SELECT * FROM parquet_scan('{path}')")
            self.__conn.execute(f"INSERT INTO parquets SELECT * FROM parquet_scan('{path}')")
        self.__table_description: list = self.__conn.execute('DESCRIBE SELECT * FROM parquets;').fetchall()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__conn.close()

    def get_schema(self) -> str:
        schema = "Table 'parquets' has the following columns:\n"
        for column in self.__table_description:
            schema += f"- {column[0]} ({column[1]})\n"
        return schema

    def get_data(self, sql_sentence: str) -> str:
        """
        Executes a SQL query on the 'parquets' table and returns the results.

        Args:
            sql_sentence (str): A SQL query to execute on the 'parquets' table.

        Returns:
            str: A string representation of the query results.
        """
        print(f'Assistant is trying to execute the following SQL query: {sql_sentence}')
        try:
            result = self.__conn.execute(sql_sentence).fetchdf()
            return result.to_string()
        except Exception as e:
            return f"Error executing SQL query: {str(e)}"