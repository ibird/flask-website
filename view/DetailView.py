#!/usr/bin/env python
# coding=utf8

from flask import render_template, current_app


def detail(requestid):
    DB_InfoSuc = current_app.DB_InfoSuc
    info = DB_InfoSuc.record_success_query(requestid)
    return render_template('record_detail.html', info=info)
