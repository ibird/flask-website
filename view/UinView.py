#!/usr/bin/env python
# coding=utf8

from flask import render_template, current_app
import json


def uin():
    return render_template('record_uin.html')

def uinSearch(uin):
    DB_Uin = current_app.DB_Uin
    uin = DB_Uin.table_uin_query(uin)
    return json.dumps(uin, ensure_ascii=False)
