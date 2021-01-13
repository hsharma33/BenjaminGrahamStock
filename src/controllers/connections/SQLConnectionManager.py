import pandas
import pyodbc
import pandas as pd
from config import DATABASE_CONFIG
import sqlalchemy
import pyodbc
from sqlalchemy import create_engine
import urllib


class SQLConnectionManager:

    def __init__(self):
        self.conn_string = urllib.parse.quote_plus(
            'DRIVER={SQL Server};SERVER=' + DATABASE_CONFIG["server"] + ';DATABASE=' + DATABASE_CONFIG["database"] +
            ';UID=' + DATABASE_CONFIG["username"] + ';PWD=' + DATABASE_CONFIG["password"])
        self.engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(self.conn_string))

    def insert_or_update(self, df, table_name, chunk_size=200, method="multi", index=False, if_exists="append"):
        index_labels = list(df.columns)
        df.to_sql(table_name, schema='dbo', con=self.engine, chunksize=chunk_size, method=method, index=index,
                  index_label=index_labels,
                  if_exists=if_exists)

    def read(self, query_str, res_count=10):
        with self.engine.connect() as conn:
            res = conn.execute(query_str)
            counter = 1
            for id, row in enumerate(res):
                print(id, row)
                if res_count != "ALL":
                    counter = counter + 1
                if counter > res_count:
                    break
