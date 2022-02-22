# -*- coding: utf-8 -*-
# @Time    : 2022/02/21 6:12 下午
# @Author  : HuangSir
# @FileName: api.py
# @Software: PyCharm
# @Desc: 风险评分

from .risk_score import risk_score


def risk_main(data: dict):
    res = risk_score(data)
    return res
