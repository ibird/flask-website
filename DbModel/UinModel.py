#!/usr/bin/env python
# coding=utf8

import sqlalchemy
from BaseModel import BaseModel


class UinModel(BaseModel):
    def __init__(self):
        super(UinModel, self).__init__()

        metadata = sqlalchemy.MetaData()
        self._table = 'table_uin'

        self._table_uin = sqlalchemy.Table(
            self._table,
            metadata,
            sqlalchemy.Column('id',
                              sqlalchemy.Integer,
                              primary_key=True),
            sqlalchemy.Column('uin',
                              sqlalchemy.String(40),
                              nullable=False),
            sqlalchemy.Column('channel',
                              sqlalchemy.String(40),
                              nullable=False),
            sqlalchemy.Column('token',
                              sqlalchemy.String(100),
                              nullable=False))

        metadata.create_all(self._engine)

    def generateDict(self, row):
        result = {}

        if row is None:
            return result

        result['uin'] = row[self._table_uin.c.uin]
        result['channel'] = row[self._table_uin.c.channel]
        result['token'] = row[self._table_uin.c.token]
        return result

    def table_uin_insert(self, uin, channel, token):
        is_exists = self.table_uin_fetchone(uin, channel)
        if is_exists:
            return False

        query = self._table_uin.insert().values(uin=uin,
                                                channel=channel,
                                                token=token)
        result = self.execute_sql(query)
        result.close()
        return True

    def table_uin_query(self, uin):
        query = sqlalchemy.sql.select(
            [self._table_uin]
        ).where(
            self._table_uin.c.uin == uin
        )

        rows = self.execute_sql(query)
        results = []
        for row in rows:
            result = self.generateDict(row)
            results.append(result)

        rows.close()
        return results

    def table_uin_fetchone(self, uin, channel):
        query = sqlalchemy.sql.select(
            [self._table_uin]
        ).where(
            self._table_uin.c.uin == uin
        ).where(
            self._table_uin.c.channel == channel
        )

        rows = self.execute_sql(query)
        row = rows.fetchone()

        result = self.generateDict(row)

        rows.close()
        return result

    def close(self):
        self.execute_sql('select 1 from %s' % self._table)
        self._conn.close()
