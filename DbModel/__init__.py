#!/usr/bin/env python
# coding=utf8


from UinModel import UinModel
from InfoSucModel import InfoSucModel
from InfoFailModel import InfoFailModel

InfoSuc_Object = InfoSucModel()
InfoFail_Object = InfoFailModel()
Uin_Object = UinModel()

def close():
    InfoSuc_Object.close()
    InfoFail_Object.close()
    Uin_Object.close()
