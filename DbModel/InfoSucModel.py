#!/usr/bin/env python
# coding=utf8

from BaseModel import BaseModel
import sqlalchemy
import datetime


class InfoSucModel(BaseModel):

    def __init__(self):
        super(InfoSucModel, self).__init__()

        metadata = sqlalchemy.MetaData()
        self._table = 'record_success'
        self._record_success = sqlalchemy.Table(self._table, metadata,
                                                sqlalchemy.Column('id',
                                                                  sqlalchemy.Integer,
                                                                  primary_key=True),
                                                sqlalchemy.Column('sendtime',
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
                                                sqlalchemy.Column('msgid',
                                                                  sqlalchemy.String(
                                                                      100),
                                                                  nullable=False),
                                                sqlalchemy.Column('requestid',
                                                                  sqlalchemy.String(
                                                                      32),
                                                                  nullable=False),
                                                sqlalchemy.Column('request',
                                                                  sqlalchemy.String(
                                                                      5000),
                                                                  nullable=False),
                                                sqlalchemy.Column('uin',
                                                                  sqlalchemy.String(
                                                                      40),
                                                                  nullable=True),
                                                sqlalchemy.Column('did',
                                                                  sqlalchemy.String(
                                                                      100),
                                                                  nullable=False),
                                                sqlalchemy.Column('recvtime',
                                                                  sqlalchemy.DateTime),
                                                sqlalchemy.Column('retmessage',
                                                                  sqlalchemy.String(5000)),
                                                sqlalchemy.Column('code',
                                                                  sqlalchemy.Integer),
                                                sqlalchemy.Column('costtime',
                                                                  sqlalchemy.Integer),
                                                sqlalchemy.Column('status',
                                                                  sqlalchemy.String(32)))
        metadata.create_all(self._engine)

    def record_success_insertall(self, msgid, queue,
                                 message, requestid, request, uin, did,
                                 retmessage, code, costtime, status):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = self._record_success.insert().values(msgid=msgid,
                                                     sendtime=now,
                                                     queue=queue,
                                                     message=message,
                                                     requestid=requestid,
                                                     request=request,
                                                     uin=uin,
                                                     did=did,
                                                     recvtime=now,
                                                     retmessage=retmessage,
                                                     code=code,
                                                     costtime=costtime,
                                                     status=status)
        result = self.execute_sql(query)
        result.close()

    def record_success_insert(self, msgid, queue,
                              message, requestid, request, uin, did):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = self._record_success.insert().values(msgid=msgid,
                                                     sendtime=now,
                                                     queue=queue,
                                                     message=message,
                                                     requestid=requestid,
                                                     request=request,
                                                     uin=uin,
                                                     did=did)
        result = self.execute_sql(query)
        result.close()

    def record_success_update(self, requestid, retmessage,
                              code, costtime, status):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = self._record_success.update(
        ).where(
            self._record_success.c.requestid == requestid
        ).values(
            recvtime=now,
            retmessage=retmessage,
            code=code,
            costtime=costtime,
            status=status)
        result = self.execute_sql(query)
        result.close()

    def generateDict(self, row):
        result = {}
        result['msgid'] = row[self._record_success.c.msgid]
        result['sendtime'] = row[self._record_success.c.sendtime].strftime(
            "%Y-%m-%d %H:%M:%S")
        result['recvtime'] = row[self._record_success.c.recvtime].strftime(
            "%Y-%m-%d %H:%M:%S")
        result['requestid'] = row[self._record_success.c.requestid]
        result['queue'] = row[self._record_success.c.queue]
        result['message'] = row[self._record_success.c.message].decode("unicode-escape")
        result['request'] = row[self._record_success.c.request].decode("unicode-escape")
        result['uin'] = row[self._record_success.c.uin]
        result['did'] = row[self._record_success.c.did]
        result['code'] = str(row[self._record_success.c.code])
        result['costtime'] = str(row[self._record_success.c.costtime])
        result['status'] = row[self._record_success.c.status]

        if row[self._record_success.c.retmessage] is None:
            result['retmessage'] = 'None'
        else:
            result['retmessage'] = row[self._record_success.c.retmessage].decode("unicode-escape")
        return result

    def record_success_select(self):
        query = sqlalchemy.sql.select(
            [self._record_success]
        ).where(
            self._record_success.c.status is not None
        ).order_by(
            self._record_success.c.sendtime.desc()
        ).limit(20)
        rows = self.execute_sql(query)

        results = []
        for row in rows:
            result = self.generateDict(row)
            results.append(result)

        rows.close()
        return results

    def record_success_query(self, requestid):
        query = sqlalchemy.sql.select(
            [self._record_success]
        ).where(
            self._record_success.c.requestid == requestid)
        rows = self.execute_sql(query)
        row = rows.fetchone()
        result = self.generateDict(row)

        rows.close()
        return result

    def record_search(self, key, value):
        query = sqlalchemy.sql.select(
            [self._record_success]
        ).where(
            self._record_success.c[key] == value)
        rows = self.execute_sql(query)

        results = []
        for row in rows:
            result = self.generateDict(row)
            results.append(result)

        rows.close()
        return results

    def close(self):
        self.execute_sql('select 1 from %s' % self._table)
        self._conn.close()
