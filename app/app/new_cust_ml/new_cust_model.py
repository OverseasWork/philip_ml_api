# -*- coding: utf-8 -*-
# @Time    : 2021/11/8 5:35 下午
# @Author  : HuangSir
# @FileName: new_cust_model.py
# @Software: PyCharm
# @Desc: 新客模型

import sys

sys.path.append('..')
import warnings

warnings.filterwarnings('ignore')

from conf.log_config import log
import joblib
import re
from datetime import datetime
import pandas as pd
import numpy as np
from utils import load_txt_feature, prob2Score
from app.app.new_cust_ml.core import FeatMap


class NewCustModel:
    """新客模型"""

    def __init__(self):
        # 加载模型相关文件
        self.lgb_model = joblib.load('app/app/new_cust_ml/static/newModel.pkl')
        self.lr_model = joblib.load('app/app/new_cust_ml/static/newModel_lr.pkl')
        self.hxy_feat = load_txt_feature('app/app/new_cust_ml/static/newFeat.txt')
        self.cl_feat = load_txt_feature('app/app/new_cust_ml/static/newFeat2.txt')
        self.comp = pd.read_excel('app/app/new_cust_ml/static/comp.xlsx', names=['package', 'name'])
        self.all_feat = load_txt_feature('app/app/new_cust_ml/static/new_cust_20220104.txt')

    def __get_feat(self, data: dict):
        """获取特征"""
        # 获取appList+adBook模型变量
        # --------------------------------------------------------------------------------
        if len(data['app_list']) == 0 or len(data['add_list']) == 0:  # 为空
            log.logger.warning('app_list or add_list is empty, fill cl feat -999')
            all_tag_dict = {k: -999 for k in self.cl_feat}
            all_tag = pd.DataFrame([all_tag_dict])
        else:  # 不为空
            df = pd.DataFrame(data['app_list'])
            df['apply_time'] = data['apply_time']
            try:
                df['apply_time'] = pd.to_datetime(df['apply_time'])
            except Exception as err:
                log.logger.error(f"申请时间戳转换错误: {str(err)},{data['apply_time']}")
                df['apply_time'] = datetime.now()

            df['lastTime'] = pd.to_datetime(df['lastTime'])
            self_df = df[df.lastTime > datetime(2010, 1, 1)]
            day_tag = pd.DataFrame(pd.cut((self_df['apply_time'] - self_df['lastTime']).dt.days,
                                          bins=[0, 1, 3, 7, 15, 30, 60, np.inf], include_lowest=True,
                                          labels=['self_1', 'self_3', 'self_7', 'self_15', 'self_30', 'self_60',
                                                  'self_90']).value_counts()).T
            day_tag.columns = day_tag.columns.tolist()
            self_comp = df[df.packageName.isin(self.comp.package)]
            comp_day_tag = pd.DataFrame(pd.cut((self_comp['apply_time'] - self_comp['lastTime']).dt.days,
                                               bins=[0, 1, 3, 7, 15, 30, 60, np.inf], include_lowest=True,
                                               labels=['comp_1', 'comp_3', 'comp_7', 'comp_15', 'comp_30', 'comp_60',
                                                       'comp_90']).value_counts()).T
            comp_day_tag.columns = comp_day_tag.columns.tolist()
            day_tag['all_self_cnt'] = self_df.shape[0]
            day_tag['all_self_comp_cnt'] = self_comp.shape[0]
            day_tag['all_cnt'] = df.shape[0]

            # 获取add联系人数目
            add_df = pd.DataFrame(data['add_list'])
            add_df['apply_time'] = data['apply_time']
            try:
                add_df['apply_time'] = pd.to_datetime(df['apply_time'])
            except Exception as err:
                log.logger.error(f"申请时间戳转换错误:{str(err)},{data['apply_time']}")
                add_df['apply_time'] = datetime.now()

            add_df['contain_chs'] = add_df['other_name'].str.extract(r'([\u4e00-\u9fa5]+)')
            lxr_num = add_df.shape[0]
            chs_lxr_num = add_df[~add_df.contain_chs.isnull()].shape[0]
            cnt = 0
            for j in add_df.other_mobile.tolist():
                if re.match('^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$', '%s' % j):
                    cnt += 1
            try:
                add_df['last_time'] = pd.to_datetime(add_df['last_time'])
            except Exception as err:
                log.logger.error(f"申请时间戳转换错误:{str(err)},{add_df['last_time']}")
                add_df['last_time'] = datetime.now()

            add_day_tag = pd.DataFrame(pd.cut((add_df['apply_time'] - add_df['last_time']).dt.days,
                                              bins=[0, 1, 3, 7, 15, 30, 60, np.inf], include_lowest=True,
                                              labels=['self_1_add', 'self_3_add', 'self_7_add', 'self_15_add',
                                                      'self_30_add', 'self_60_add', 'self_90_add']).value_counts()).T

            add_day_tag.columns = add_day_tag.columns.tolist()
            add_day_tag[['lxr_num', 'chs_lxr_num', 'cnt']] = [lxr_num, chs_lxr_num, cnt]
            all_tag = pd.concat([day_tag, add_day_tag, comp_day_tag], axis=1)

            all_tag['self_3_all'] = all_tag[['self_1', 'self_3']].sum(axis=1)
            all_tag['self_7_all'] = all_tag[['self_1', 'self_3', 'self_7']].sum(axis=1)
            all_tag['self_15_all'] = all_tag[['self_1', 'self_3', 'self_7', 'self_15']].sum(axis=1)
            all_tag['self_30_all'] = all_tag[['self_1', 'self_3', 'self_7', 'self_15', 'self_30']].sum(axis=1)
            all_tag['self_60_all'] = all_tag[['self_1', 'self_3', 'self_7', 'self_15', 'self_30', 'self_60']].sum(
                axis=1)

            all_tag['comp_3_all'] = all_tag[['comp_1', 'comp_3']].sum(axis=1)
            all_tag['comp_7_all'] = all_tag[['comp_1', 'comp_3', 'comp_7']].sum(axis=1)
            all_tag['comp_15_all'] = all_tag[['comp_1', 'comp_3', 'comp_7', 'comp_15']].sum(axis=1)
            all_tag['comp_30_all'] = all_tag[['comp_1', 'comp_3', 'comp_7', 'comp_15', 'comp_30']].sum(axis=1)
            all_tag['comp_60_all'] = all_tag[['comp_1', 'comp_3', 'comp_7', 'comp_15', 'comp_30', 'comp_60']].sum(
                axis=1)

            all_tag['self_1_pct'] = all_tag['self_1'] / all_tag['all_self_cnt']
            all_tag['self_3_all_pct'] = all_tag['self_3_all'] / all_tag['all_self_cnt']
            all_tag['self_7_all_pct'] = all_tag['self_7_all'] / all_tag['all_self_cnt']
            all_tag['self_15_all_pct'] = all_tag['self_15_all'] / all_tag['all_self_cnt']
            all_tag['self_30_all_pct'] = all_tag['self_30_all'] / all_tag['all_self_cnt']
            all_tag['self_60_all_pct'] = all_tag['self_60_all'] / all_tag['all_self_cnt']
            all_tag['all_self_pct'] = all_tag['all_self_cnt'] / all_tag['all_cnt']

            all_tag['1_pct'] = all_tag['self_1'] / all_tag['all_cnt']
            all_tag['3_all_pct'] = all_tag['self_3_all'] / all_tag['all_cnt']
            all_tag['7_all_pct'] = all_tag['self_7_all'] / all_tag['all_cnt']
            all_tag['15_all_pct'] = all_tag['self_15_all'] / all_tag['all_cnt']
            all_tag['30_all_pct'] = all_tag['self_30_all'] / all_tag['all_cnt']
            all_tag['60_all_pct'] = all_tag['self_60_all'] / all_tag['all_cnt']

            all_tag['comp_3_pct'] = all_tag['comp_3_all'] / all_tag['self_3_all']
            all_tag['comp_7_pct'] = all_tag['comp_7_all'] / all_tag['self_7_all']
            all_tag['comp_15_pct'] = all_tag['comp_15_all'] / all_tag['self_15_all']
            all_tag['comp_30_pct'] = all_tag['comp_30_all'] / all_tag['self_30_all']
            all_tag['comp_60_pct'] = all_tag['comp_60_all'] / all_tag['self_60_all']
            all_tag['all_self_comp_pct'] = all_tag['all_self_comp_cnt'] / all_tag['all_cnt']

            # add

            all_tag['self_3_add_all'] = all_tag[['self_1_add', 'self_3_add']].sum(axis=1)
            all_tag['self_7_add_all'] = all_tag[['self_1_add', 'self_3_add', 'self_7_add']].sum(axis=1)
            all_tag['self_15_add_all'] = all_tag[['self_1_add', 'self_3_add', 'self_7_add', 'self_15_add']].sum(axis=1)
            all_tag['self_30_add_all'] = all_tag[
                ['self_1_add', 'self_3_add', 'self_7_add', 'self_15_add', 'self_30_add']].sum(axis=1)
            all_tag['self_60_add_all'] = all_tag[
                ['self_1_add', 'self_3_add', 'self_7_add', 'self_15_add', 'self_30_add', 'self_60_add']].sum(axis=1)

            all_tag['self_3_add_pct'] = all_tag['self_3_add_all'] / all_tag['lxr_num']
            all_tag['self_7_add_pct'] = all_tag['self_7_add_all'] / all_tag['lxr_num']
            all_tag['self_15_add_pct'] = all_tag['self_15_add_all'] / all_tag['lxr_num']
            all_tag['self_30_add_pct'] = all_tag['self_30_add_all'] / all_tag['lxr_num']
            all_tag['self_60_add_pct'] = all_tag['self_60_add_all'] / all_tag['lxr_num']

        # 提取基础入模变量
        # ------------------------------------------------------------
        hxy_data = {v: data[k] for k, v in FeatMap.items()}

        # 合并模型变量
        # ------------------------------------------------------------
        all_tag2 = pd.concat([all_tag[self.cl_feat], pd.DataFrame([hxy_data])], axis=1)
        return all_tag2[self.all_feat]

    def predict(self, data: dict):
        # 获取入模变量
        res_data = pd.DataFrame(self.__get_feat(data))
        res_data.fillna(-999, inplace=True)
        # 模型预测
        lgb_prob = np.nanmean([i.predict(res_data) for i in self.lgb_model], axis=0)[0]
        lr_prob = self.lr_model.predict_proba([[lgb_prob]])[:, 1][0]
        # 评分转换
        score = prob2Score(lr_prob, basePoint=600, PDO=50, odds=30)
        score = int(score)
        score = 300 if score < 300 else 850 if score > 850 else score
        return score
