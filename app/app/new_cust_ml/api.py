# -*- coding: utf-8 -*-
# @Time    : 2021/11/8 6:49 下午
# @Author  : HuangSir
# @FileName: api.py
# @Software: PyCharm
# @Desc: 新客信用分模型主程序
import warnings

warnings.filterwarnings('ignore')

from conf.log_config import log
from app.app.new_cust_ml.new_cust_model import NewCustModel

ncl = NewCustModel()


def new_cust_main(data):
    user_id = data['user_id']
    busi_id = data['busi_id']
    ml_data = data['data']
    log.logger.info(f"start predict new cust order:{busi_id} ---------------------------------------")
    try:
        score = ncl.predict(data=ml_data)
        msg = '处理成功'
        detail = ''
        code = 200
    except Exception as err:
        log.logger.error(f"未知错误: {str(err)}")
        score = -9999
        msg = '处理失败'
        detail = str(err)
        code = 400
    log.logger.info(f"end predict new cust order:{busi_id}, out score: {score} ---------------------------")
    return {'user_id': user_id,
            'busi_id': busi_id,
            'new_cust_score': score,
            'msg': msg,
            'code': code,
            'detail': detail}
