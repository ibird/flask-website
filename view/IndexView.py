#!/usr/bin/env python
# coding=utf8

from flask import render_template


def index():
        return render_template('index.html')
