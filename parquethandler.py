import duckdb
from duckdb import DuckDBPyConnection

class ParquetHandler:

    def __init__(self, parquet_path: str):
        self.__conn: DuckDBPyConnection = duckdb.connect(':memory:')
        self.__conn.execute(
            f"CREATE TABLE parquets AS SELECT * FROM parquet_scan('{parquet_path}')")
        self.__table_description: list = self.__conn.execute('''
                                                             DESCRIBE SELECT * FROM parquets;
                                                             ''').fetchall()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__conn.close()

    def __get_table_description_as_str(self) -> str:
        answer: list = []
        for column in self.__table_description:
            answer.append(f'{column[0]} ({column[1]}) ')
        return ''.join(answer)

    def __get_tuples(self, sql_sentence: str) -> str:
        f"""
        Gets information about the "parquets" as requested by the user.
        args:
            sql_sentence (str): A SQL sentence for a table named "parquets" with the following columns:
            {self.__get_table_description_as_str()}
        """
        print(f'Assitant is tring to execute the following sql sentence: {sql_sentence}')
        result: list = self.__conn.execute(sql_sentence).fetchmany(size=20)
        return repr(result)

    def get_tools(self) -> list:
        return [self.__get_tuples]
