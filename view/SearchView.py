#!/usr/bin/env python
# coding=utf8

from flask import render_template, current_app
import json


def search():
    return render_template('record_search.html')


def searchUin(uin):
    DB_InfoSuc = current_app.DB_InfoSuc
    info = DB_InfoSuc.record_search('uin', uin)
    return json.dumps(info, ensure_ascii=False)


def searchMsgid(msgid):
    DB_InfoSuc = current_app.DB_InfoSuc
    info = DB_InfoSuc.record_search('msgid', msgid)
    return json.dumps(info, ensure_ascii=False)
