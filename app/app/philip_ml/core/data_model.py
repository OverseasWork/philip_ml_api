# -*- coding: utf-8 -*-
# @Time    : 2022/02/21 3:58 下午
# @Author  : HuangSir
# @FileName: data_model.py
# @Software: PyCharm
# @Desc:

from pydantic import BaseModel, Field
from typing import List
from app.app.philip_ml.core import appListExample, addListExample


class AddList(BaseModel):
    """通讯录"""
    last_time: str = Field(default=None, title='更新时间', example='2020-06-25 09:39:24',
                           description='yyyy-mm-dd HH:MM:SS')
    other_mobile: str = Field(default=None, title='对方号码', example='4250719194',
                              description='对方号码')
    other_name: str = Field(default=None, title='对方姓名', example='กรุง',
                            description='对方姓名')


class AppList(BaseModel):
    """appList数据模型"""
    firstTime: str = Field(default=None, title='首次安装时间', example='2020-06-25 09:39:24',
                           description='yyyy-mm-dd HH:MM:SS')
    lastTime: str = Field(default=None,title='最近更新时间', example='2020-06-25 09:39:24',
                          description='yyyy-mm-dd HH:MM:SS')

    name: str = Field(default=None, title='名称', example='โคลนโทรศัพท์', description='app名称')
    packageName: str = Field(default=None,title='包名', example='com.coloros.backuprestore', description='包名')
    # systemApp: str = Field(default=None, title='系统版本', example='1', description='')
    # versionCode: str = Field(default=None, title='5.0.50', example='1', description='')


class CustData(BaseModel):
    BUSI_ID: str = Field(default=None,title='订单号', example='1020211106012142000000153', description='唯一标识符')
    order_time: int = Field(default=None, title='订单时间', example=1462084086000, description='订单时间戳')
    ADDLIST: List[AddList] = Field(default=..., example=addListExample, title='通讯录', description='联系人列表')
    APPLIST: List[AppList] = Field(default=..., example=appListExample, title='appList', description='app列表')
    MOBILE: str = Field(default=None, title='手机号码', example='4250719194', description='手机号码')
    sex:int = Field(default=1,title='性别',description='1:男性,2:女性')
    marry:int = Field(default=1,title='婚姻状态',description='1:单身,2:已婚,3:离婚,4:丧偶')
    age:int = Field(default=25,title='年龄',description='下单日期-生日,取整')
    brands: str = Field(default=None, title='手机BRANDS', example='realme', description='手机品牌')
    mobile_model: str = Field(default=None, title='手机mobile_model', example='RMX1911', description='手机型号')
    cpu_core: int = Field(default=None, title='cpu核数')
    RAM: str = Field(default=None, title='RAM', example='564 MB/2.77 GB')
    ROM: str = Field(default=None, title='ROM', example='38.60 GB/53.11 GB')
    RESOLUTION: str = Field(default=None,title='RESOLUTION', example='720\u00d71600 -320')
    campaign_name: str = Field(default=None, title='渠道名', example='vfineads')
    WHITE: int = Field(default=None, title='是否白名单', example=1, description='1 表示白名单，0 表示非白名单')
    is_new: int = Field(default=None,title='是否新客', example=1, description='1 表示新客，0 表示老客')