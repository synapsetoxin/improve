import os
import sqlite3
import logging
import datetime

from typing import Any, Optional, List, Tuple
from dataclasses import dataclass, field


class Database:
    def __init__(self):
        self.db_path: os.path = 'db.sqlite'
        self.schema_path: os.path = 'app/configs/schema.sql'

    @property
    def connection(self):
        return sqlite3.connect(self.db_path)

    def execute(self, statement: str, parameters: Optional[List[Any]] = None,
                fetchone=False, fetchall=False, commit=False) -> Optional[Any]:
        if not parameters:
            parameters = tuple()

        with self.connection as con:
            cursor = con.cursor()
            data: Optional[Any] = None
            cursor.execute(statement, parameters)

            if commit:
                con.commit()
            if fetchone:
                data = cursor.fetchone()
            if fetchall:
                data = cursor.fetchall()

        return data

    @staticmethod
    def format_args(statement: str, parameters: dict):
        # usage: sql, params = self.format_args(sql, params)
        statement += ' '
        statement += " AND ".join([f'{item} = ?' for item in parameters])
        return statement, tuple(parameters.values())

    def create_tables(self):
        """
        Create tables from schema.sql file
        """
        logging.info('INIT DB')
        with self.connection as con:
            cur = con.cursor()
            with open(self.schema_path, encoding='utf-8') as schema:
                cur.executescript(schema.read())
                logging.info('INIT DB SUCCESS')

    def __del__(self):
        self.connection.close()


@dataclass
class User:
    userid: int
    username: str = field(default=None)
    balance: float = field(default=0.0)
    dotaid: Optional[int] = field(default=None)
    created_at: datetime = field(default=None)

    def __post_init__(self):
        db = Database()
        try:
            utcnow = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
            sql = 'INSERT INTO users (userid, join_date) VALUES (?, ?);'
            db.execute(sql, [self.userid, utcnow], commit=True)
        except sqlite3.IntegrityError:
            pass
        finally:
            # Getting all rows from the database and assigning
            sql = 'SELECT * FROM users WHERE userid=?'
            fill = iter(db.execute(sql, [self.userid], fetchall=True)[0])
            for attr in self.__dict__:
                setattr(self, attr, next(fill))
            if self.locations:
                self.locations = self.locations.split('&')

    def __del__(self):
        db = Database()
        if self.locations:
            self.locations = '&'.join(self.locations)
        keys = ','.join(f'{k}=?' for k in self.__dict__)
        sql = f'UPDATE users SET {keys} WHERE userid = ?'
        # self.premium_expire = self.premium_expire.strftime("%Y-%m-%dT%H:%M:%S")
        db.execute(sql, [*self.__dict__.values(), self.userid], commit=True)

    def send_money(self, amount: float) -> None:
        pass

    def delete(self):
        db = Database()
        sql = 'DELETE FROM users WHERE userid = ?;'
        db.execute(sql, [self.userid], commit=True)


@dataclass
class Tournament:
    count: int = field(default=0)
    cost: float = field(default=0.0)
    users: List[Tuple[int, str, int]] = field(default=None)

    def reglist(self) -> str:
        """
        Стоимость: N
        Участников: X
        =====zxc eblany:=====
        :return:
        """
        # todo: rename
        pass


@dataclass
class ShopRole:
    role_id: int
    cost: float
    seller_id: int
    expired_at: datetime
    sales: int
    active: bool

    def extend(self, days: int) -> None:
        pass

    def delete(self):
        pass


@dataclass
class Shop:
    roles: List[ShopRole]


