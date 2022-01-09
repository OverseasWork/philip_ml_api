# -*- coding: utf-8 -*-
# @Time    : 2021/11/8 10:43 下午
# @Author  : HuangSir
# @FileName: api.py
# @Software: PyCharm
# @Desc:老客信用分模型主程序

import warnings

warnings.filterwarnings('ignore')

from conf.log_config import log

from app.app.old_cust_ml.old_cust_model import OldCustModel

ocl = OldCustModel()

def old_cust_main(data):

    user_id = data['user_id']
    busi_id = data['busi_id']
    ml_data = data['data']
    log.logger.info(f"start predict old cust order:{busi_id} ---------------------------------------")
    try:
        score = ocl.predict(data=ml_data)
        msg = '处理成功'
        detail = ''
        code = 200
    except Exception as err:
        log.logger.error(f"未知错误: {str(err)}")
        score = -9999
        msg = '处理失败'
        detail = str(err)
        code = 400
    log.logger.info(f"end predict old cust order:{busi_id}, out score: {score} ---------------------------")
    return {'user_id': user_id,
            'busi_id': busi_id,
            'old_cust_score': score,
            'msg': msg,
            'code': code,
            'detail': detail}

