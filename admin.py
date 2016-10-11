#!/usr/bin/env python
# coding=utf8

from flask import Flask
from flask import current_app

import view
import DbModel


app = Flask(__name__)

with app.app_context():
    current_app.DB_InfoSuc = DbModel.InfoSuc_Object
    current_app.DB_InfoFail = DbModel.InfoFail_Object
    current_app.DB_Uin = DbModel.Uin_Object

app.add_url_rule('/', view_func=view.index)
app.add_url_rule('/success', view_func=view.success)
app.add_url_rule('/fail', view_func=view.fail)
app.add_url_rule('/detail/<requestid>', view_func=view.detail)
app.add_url_rule('/fail', view_func=view.fail)

app.add_url_rule('/uin', view_func=view.uin)
app.add_url_rule('/uin/search/<uin>', view_func=view.uinSearch)

app.add_url_rule('/search', view_func=view.search)
app.add_url_rule('/search/uin/<uin>', view_func=view.searchUin)
app.add_url_rule('/search/msgid/<msgid>', view_func=view.searchMsgid)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8080)
