#!/usr/bin/env python
# coding=utf8

from flask import render_template, current_app


def fail():
    DB_InfoFail = current_app.DB_InfoFail
    infolist = DB_InfoFail.record_failed_select()
    return render_template('record_fail.html', infolist=infolist)
