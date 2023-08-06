"""
使用内置库sqlite3操作SQLite
"""

import logging
import sqlite3
from contextlib import closing
from typing import List


class SQLite3:
    """
    db_path = '/root/prokect/sqlite.db'
    with SQLite3(db_path) as db:
        re, msg = db.execute_auto_commit("insert into stu (name, age) values (?, ?)", ('测试', 23,))

    sqlite使用'?'作为占位符

    """

    def __init__(self, db_path, show_dict=False):
        self.db_path = db_path
        self.show_dict = show_dict
        self.conn = None

    def connect(self):
        self.conn: sqlite3.Connection = sqlite3.connect(self.db_path)
        if self.show_dict:
            self.conn.row_factory = SQLite3.dict_factory

    @staticmethod
    def dict_factory(cursor, row):
        """
        字典工厂，将输出结果展示为字典格式
        """
        d = {}
        for index, col in enumerate(cursor.description):
            d[col[0]] = row[index]
        return d

    def close(self):
        self.conn.close()

    def __enter__(self):
        self.connect()
        return self

    def commit(self):
        self.conn.commit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _do_execute(self, cur, sql, params):
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)

    def _do_executemany(self, cur, sql, params):
        if params:
            cur.executemany(sql, params)
        else:
            cur.executemany(sql)

    def execute(self, sql, params: tuple = None) -> (bool, int):
        return self._execute(sql, params, auto_commit=False)

    def execute_auto_commit(self, sql, params: tuple = None) -> (bool, int):
        return self._execute(sql, params, auto_commit=True)

    def executemany(self, sql, params: List[tuple] = None) -> (bool, int):
        return self._executemany(sql, params, auto_commit=False)

    def executemany_auto_commit(self, sql, params: List[tuple] = None) -> (bool, int):
        return self._executemany(sql, params, auto_commit=True)

    def _execute(self, sql, params=None, auto_commit=True) -> (bool, int):
        try:
            with closing(self.conn.cursor()) as cur:
                self._do_execute(cur, sql, params)
                if auto_commit:
                    self.conn.commit()
                return True, cur.rowcount
        except Exception as e:
            logging.exception(e)
            self.conn.rollback()
            return False, f'sql执行失败 {e} -> "{sql}" [params:{params}]'

    def _executemany(self, sql, params=None, auto_commit=True) -> (bool, int):
        try:
            with closing(self.conn.cursor()) as cur:  # type: sqlite3.Cursor
                self._do_executemany(cur, sql, params)
                if auto_commit:
                    self.conn.commit()
                return True, cur.rowcount
        except Exception as e:
            logging.exception(e)
            self.conn.rollback()
            return False, f'sql执行失败 {e} -> "{sql}" [params:{params}]'

    def fetchone(self, sql, params: tuple = None) -> (bool, list):
        try:
            with closing(self.conn.cursor()) as cur:
                self._do_execute(cur, sql, params)
                self.conn.commit()
                row = cur.fetchone()
                return True, row
        except Exception as e:
            logging.exception(e)
            return False, f'查询异常 {e} -> "{sql}" [params:{params}]'

    def fetchall(self, sql, params: tuple = None) -> (bool, list):
        try:
            with closing(self.conn.cursor()) as cur:
                self._do_execute(cur, sql, params)
                self.conn.commit()
                rows = cur.fetchall()
                return True, rows
        except Exception as e:
            logging.exception(e)
            return False, f'查询异常 {e} -> "{sql}" [params:{params}]'
