#!/usr/bin/env python
# coding=utf8

from BaseModel import BaseModel
import sqlalchemy
import datetime


class InfoFailModel(BaseModel):

    def __init__(self):
        super(InfoFailModel, self).__init__()

        metadata = sqlalchemy.MetaData()
        self._table = 'record_failed'

        self._record_failed = sqlalchemy.Table(self._table, metadata,
                                               sqlalchemy.Column('id',
                                                                 sqlalchemy.Integer,
                                                                 primary_key=True),
                                               sqlalchemy.Column('msgid',
                                                                 sqlalchemy.String(
                                                                     100),
                                                                 nullable=False),
                                               sqlalchemy.Column('datetime',
                                                                 sqlalchemy.DateTime,
                                                                 nullable=False),
                                               sqlalchemy.Column('queue',
                                                                 sqlalchemy.String(
                                                                     40),
                                                                 nullable=False),
                                               sqlalchemy.Column('message',
                                                                 sqlalchemy.String(
                                                                     5000),
                                                                 nullable=False),
                                               sqlalchemy.Column('cause',
                                                                 sqlalchemy.String(
                                                                     5000),
                                                                 nullable=False))
        metadata.create_all(self._engine)

    def record_failed_insert(self, msgid, queue, message, cause):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = self._record_failed.insert().values(datetime=now,
                                                    msgid=msgid,
                                                    queue=queue,
                                                    message=message,
                                                    cause=cause)
        result = self.execute_sql(query)
        result.close()

    def record_failed_select(self):
        query = sqlalchemy.sql.select(
            [self._record_failed]
        ).order_by(
            self._record_failed.c.datetime.desc()
        ).limit(20)

        results = []
        rows = self.execute_sql(query)
        for row in rows:
            result = {}
            result['msgid'] = row[self._record_failed.c.msgid]
            result['datetime'] = row[self._record_failed.c.datetime].strftime(
                "%Y-%m-%d %H:%M:%S")
            result['message'] = row[self._record_failed.c.message]
            result['queue'] = row[self._record_failed.c.queue]
            result['cause'] = row[self._record_failed.c.cause]
            results.append(result)

        rows.close()
        return results

    def close(self):
        self.execute_sql('select 1 from %s' % self._table)
        self._conn.close()
