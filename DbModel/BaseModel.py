#!/usr/bin/env python
# coding=utf8

import sqlalchemy
import ConfigParser
import logging

LOGGER = logging.getLogger(__name__)


class BaseModel(object):
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read("/data/market_server/conf/tipPlat.conf")

        self._host = cf.get("mysql", "host")
        self._port = cf.get("mysql", "port")
        self._username = cf.get("mysql", "user")
        self._password = cf.get("mysql", "pass")
        self._dbname = cf.get("mysql", "db")

        sqlschema = "mysql://%s:%s@%s:%s/%s" % (self._username,
                                                self._password,
                                                self._host,
                                                self._port,
                                                self._dbname)
        self._engine = sqlalchemy.create_engine(
            sqlschema,
            pool_recycle=180,
            poolclass=sqlalchemy.pool.NullPool
        )

        self._conn = self._engine.connect()

    def execute_sql(self, query):
        try:
            with self._conn.begin():
                result = self._conn.execute(query)
        except sqlalchemy.exc.DBAPIError as e:
            if e.connection_invalidated:
                LOGGER.info("Connection was invalidated!")
            self._conn = self._engine.connect()
            result = self._conn.execute(query)
        return result

    def close(self):
        self._conn.close()
