# -*- coding: utf-8 -*-
# @Time    : 2021/12/27 6:12 下午
# @Author  : HuangSir
# @FileName: api.py
# @Software: PyCharm
# @Desc: 风险评分评级

from .risk_score import risk_score


def risk_main(data: dict):
    res = risk_score(data)
    return res

