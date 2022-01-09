# -*- coding: utf-8 -*-
# @Time    : 2021/11/8 3:58 下午
# @Author  : HuangSir
# @FileName: data_model.py
# @Software: PyCharm
# @Desc:

from pydantic import BaseModel, Field
from typing import List
from app.app.applist_ml.core import AppList, AdList,appListExample,adListExample


class DataMl(BaseModel):
    """老客数据模型"""
    now_od_num: int = Field(default=None,example=0,title='当前在途订单数量')

    re_30d_apply_num: int = Field(default=None, title='近30天申请次数', example=0, description='0,1,2,3 ...')

    now_co_apply_amount: float = Field(default=None, example=0, title='当前共债金额')

    re_7d_apply_num: int = Field(default=None, title='近7天申请次数', example=0, description='0,1,2,3 ...')

    his_sum_rej_cnt: int = Field(default=None, title='历史累计拒绝次数', example=0)

    emergency_con_num: int = Field(default=None, title='紧急联系人关联用户数量',example=0,description='所有注册用户')

    education: int = Field(default=None, title='教育程度', example=5,
                           description='1:小学、2:初中、3:高中 4:大专、 5:本科、6:其他')

    re_24h_apply_num: int = Field(default=None, title='近24小时申请次数', example=0, description='0,1,2,3 ...')

    cust_type: int = Field(default=None, title='用户类型', example=2,
                           description='1:私营业主、2:上班族、3:自由职业(摩的司机/农民/渔夫等) 4:退休/待业/无业/家庭主妇')

    ram_y: float = Field(default=None, title='RAM_Y', example=8.01, description='RAM: 3.25 GB/8.01 GB, 截取第二个值')

    ram_x: float = Field(default=None, title='RAM_X', example=3.25, description='RAM: 3.25 GB/8.01 GB, 截取第一个值')

    age: int = Field(default=None, title='年龄',example=35,description="下单时间减去 - 出生日期")

    emergency_return_con_num: float = Field(default=None,example = 0,title='紧急联系人关联还款用户数量', description='有借款还款记录客户')

    income: float = Field(default=None, title='月收入',
                          description='1:8000以下 、2:在8000和15000之间 、 3:15000以上')

    apply_time: str = Field(default=None, title='申请时间', example='2021-06-25 09:39:24',
                            description='yyyy-mm-dd HH:MM:SS')

    app_list: List[AppList] = Field(default=..., example=appListExample, title='appList', description='applist详情')

    add_list: List[AdList] = Field(default=..., example=adListExample, title='通讯录',description='通讯录详情')


class OldCustData(BaseModel):
    user_id: str = Field(default='83595', title='用户id,可用手机号')
    busi_id: str = Field(default='1020210717125639000083595', title='交易订单号')
    data: DataMl = Field(default=..., title='模型数据')
