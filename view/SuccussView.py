#!/usr/bin/env python
# coding=utf8

from flask import render_template, current_app


def success():
    DB_InfoSuc = current_app.DB_InfoSuc

    infolist = DB_InfoSuc.record_success_select()
    return render_template('record_success.html', infolist=infolist)
