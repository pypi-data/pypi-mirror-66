"""
使用三方库pymysql操作MySQL(MariaDB)
"""
import logging
from typing import List

import pymysql
from pymysql.cursors import Cursor, DictCursor


class MySQL:
    """
    db_cfg = {
        host: str,
        port: int,
        user: str,
        password: str,
        [database: str,]
        [charset: str,]
        [cursorclass: DictCursor,]
    }
    db_cfg的参数名必须保持一致

    with MySQL(db_cfg, True) as db:
        re, msg = db.fetchone("
            select * from cbms.alarm_act where alarm_id in %s order by alarm_id desc
        ", (['55476'],))
        print(re, msg)

    pymysql使用 '%s' 作为占位符

    """

    def __init__(self, db_cfg: dict, show_dict=False):
        self.db_cfg = db_cfg
        self.show_dict = show_dict
        self.conn = None

    def connect(self):
        if self.show_dict:
            self.db_cfg['cursorclass'] = DictCursor
        self.conn = pymysql.connect(**self.db_cfg)

    def close(self):
        self.conn.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def commit(self):
        self.conn.commit()

    def _do_execute(self, cur: Cursor, sql, params) -> int:
        if params:
            return cur.execute(sql, params)
        else:
            return cur.execute(sql)

    def _do_executemany(self, cur: Cursor, sql, params) -> int:
        return cur.executemany(sql, params)

    def _execute(self, sql, params=None, auto_commit=True) -> (bool, int):
        try:
            with self.conn.cursor() as cur:
                cnt = self._do_execute(cur, sql, params)
                if auto_commit:
                    self.conn.commit()
                return True, cnt
        except Exception as e:
            logging.exception(e)
            self.conn.rollback()
            return False, f'sql执行失败 {e} -> "{sql}" [params:{params}]'

    def _executemany(self, sql, params, auto_commit=True) -> (bool, int):
        try:
            with self.conn.cursor() as cur:  # type: Cursor
                cnt = self._do_executemany(cur, sql, params)
                if auto_commit:
                    self.conn.commit()
                return True, cnt
        except Exception as e:
            logging.exception(e)
            self.conn.rollback()
            return False, f'sql执行失败 {e} -> "{sql}" [params:{params}]'

    def execute(self, sql, params: tuple = None) -> (bool, int):
        return self._execute(sql, params, auto_commit=False)

    def execute_auto_commit(self, sql, params: tuple = None) -> (bool, int):
        return self._execute(sql, params, auto_commit=True)

    def executemany(self, sql, params: List[tuple] = None) -> (bool, int):
        return self._executemany(sql, params, auto_commit=False)

    def executemany_auto_commit(self, sql, params: List[tuple] = None) -> (bool, int):
        return self._executemany(sql, params, auto_commit=True)

    def fetchone(self, sql, params: tuple = None) -> (bool, list):
        try:
            with self.conn.cursor() as cur:
                self._do_execute(cur, sql, params)
                self.conn.commit()
                row = cur.fetchone()
                return True, row
        except Exception as e:
            logging.exception(e)
            return False, f'查询异常 {e} -> "{sql}" [params:{params}]'

    def fetchall(self, sql, params: tuple = None) -> (bool, list):
        try:
            with self.conn.cursor() as cur:
                self._do_execute(cur, sql, params)
                self.conn.commit()
                rows = cur.fetchall()
                return True, rows
        except Exception as e:
            logging.exception(e)
            return False, f'查询异常 {e} -> "{sql}" [params:{params}]'
