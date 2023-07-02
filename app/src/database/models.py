import os
import sqlite3
import logging
import datetime

from typing import Any, Optional, List, Tuple, Dict
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
            # utcnow = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
            sql = 'INSERT INTO users (userid) VALUES (?);'
            db.execute(sql, [self.userid], commit=True)
        except sqlite3.IntegrityError:
            pass
        finally:
            # Getting all rows from the database and assigning
            sql = 'SELECT * FROM users WHERE userid=?'
            fill = iter(db.execute(sql, [self.userid], fetchall=True)[0])
            for attr in self.__dict__:
                setattr(self, attr, next(fill))

    def __del__(self):
        db = Database()
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
class Shop(List[ShopRole]):
    pass


@dataclass
class Wallet:
    address: str
    name: str = field(default=None)

    def __post_init__(self):
        if type(self.address) == tuple:
            self.name = self.address[1]
            self.address = self.address[0]


@dataclass
class Wallets(List[Wallet]):
    __db = Database()

    def __post_init__(self):
        sql = 'SELECT address, name FROM wallets;'
        wallets = self.__db.execute(sql, fetchall=True)
        self.extend(list(map(Wallet, wallets)))

    def add(self, wallet: Wallet):
        self.append(wallet)
        try:
            sql = 'INSERT INTO wallets (address, name) VALUES (?, ?);'
            self.__db.execute(sql, [wallet.address, wallet.name], commit=True)
        except sqlite3.IntegrityError:
            sql = 'UPDATE wallets SET name = ? WHERE address = ?'
            self.__db.execute(sql, [wallet.name, wallet.address], commit=True)

    def remove(self, wallet: Wallet):
        self.remove(wallet)
        sql = 'DELETE FROM wallets WHERE address = ?;'
        self.__db.execute(sql, [wallet.address], commit=True)
