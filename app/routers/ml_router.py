# -*- coding: utf-8 -*-
# @Time    : 2021/11/6 11:35 下午
# @Author  : HuangSir
# @FileName: ml_router.py
# @Software: PyCharm
# @Desc: 风险分模型路由


from fastapi import APIRouter

from app.app.philip_ml.core import CustData
from app.app import risk_score

ml_router = APIRouter()


@ml_router.post('/v1/score', tags=['风险评分'])
async def cust_risk_score(data: CustData):
    data = data.dict()
    res = risk_score(data)
    return res

