import pandas as pd
import numpy as np
import re
import json
import joblib
import datetime


def cal_ram_rom(df):
    ram_rom=[]
    try:
        for i in df.ram.split('/'):
            if i.endswith('MB'):
                ram_rom.append(float(i.replace('MB', ''))/1024)
            else:
                ram_rom.append(float(i.replace('GB', '')))
        for i in df.rom.split('/'):
            if i.endswith('MB'):
                ram_rom.append(float(i.replace('MB', ''))/1024)
            else:
                ram_rom.append(float(i.replace('GB', '')))
#         [i/1024 for i in df.ram.split('/') if i.endwiths('MB')]
#         dd=df.ram.replace('GB','').replace('MB','').split('/')
#         dd2=df.rom.replace('GB','').replace('MB','').split('/')
        return ram_rom
    except Exception as e:
        return 0, 0, 0, 0


def cal_res(df):
    return [float(i) for i in re.split('[ ×]',df.RESOLUTION)]


def get_feature(data):
    df = pd.DataFrame(json.loads(data.loc[0, 'APPLIST']))
    df['apply_time'] = data.loc[0, 'order_time']
    df['apply_time'] = pd.to_datetime(df['apply_time'])
    df['lastTime'] = pd.to_datetime(df['lastTime'])
    self_df = df[df.lastTime > datetime.datetime(2010, 1, 1)]

    day_tag = pd.DataFrame(pd.cut((self_df['apply_time'] - self_df['lastTime']).dt.days,
                                  bins=[0, 1, 3, 7, 15, 30, 60, np.inf], include_lowest=True,
                                  labels=['self_1', 'self_3', 'self_7', 'self_15', 'self_30', 'self_60',
                                          'self_90']).value_counts()).T
    day_tag.columns = day_tag.columns.tolist()
    self_comp = df[df.packageName.isin(comp.package)]
    comp_day_tag = pd.DataFrame(pd.cut((self_comp['apply_time'] - self_comp['lastTime']).dt.days,
                                       bins=[0, 1, 3, 7, 15, 30, 60, np.inf], include_lowest=True,
                                       labels=['comp_1', 'comp_3', 'comp_7', 'comp_15', 'comp_30', 'comp_60',
                                               'comp_90']).value_counts()).T
    comp_day_tag.columns = comp_day_tag.columns.tolist()
    day_tag['BUSI_ID'] = data.loc[0, 'BUSI_ID']
    #     day_tag['DB']=data.loc[0,'DB']
    day_tag['apply_time'] = data.loc[0, 'order_time']
    day_tag['all_self_cnt'] = self_df.shape[0]
    day_tag['all_self_comp_cnt'] = self_comp.shape[0]
    day_tag['all_cnt'] = df.shape[0]
    # add-------
    add_df = pd.DataFrame(json.loads(data.loc[0, 'ADDLIST']))
    add_df['contain_chs'] = add_df['other_name'].str.extract(r'([\u4e00-\u9fa5]+)')
    lxr_num = add_df.shape[0]
    chs_lxr_num = add_df[~add_df.contain_chs.isnull()].shape[0]
    cnt = 0
    for j in add_df.other_mobile.tolist():
        if re.match('^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$', '%s' % j):
            cnt += 1
    add_df['apply_time'] = data.loc[0, 'order_time']
    add_df['apply_time'] = pd.to_datetime(add_df['apply_time'])
    add_df['last_time'] = pd.to_datetime(add_df['last_time'])
    add_day_tag = pd.DataFrame(pd.cut((add_df['apply_time'] - add_df['last_time']).dt.days,
                                      bins=[0, 1, 3, 7, 15, 30, 60, np.inf], include_lowest=True,
                                      labels=['self_1_add', 'self_3_add', 'self_7_add', 'self_15_add', 'self_30_add',
                                              'self_60_add', 'self_90_add']).value_counts()).T
    add_day_tag.columns = add_day_tag.columns.tolist()

    add_day_tag[['lxr_num', 'chs_lxr_num', 'cnt']] = [lxr_num, chs_lxr_num, cnt]
    all_tag = pd.concat([day_tag, add_day_tag, comp_day_tag], axis=1)
    return all_tag


def feature_step2(new):
    new['self_3_all']=new[['self_1','self_3']].sum(axis=1)
    new['self_7_all']=new[['self_1','self_3','self_7']].sum(axis=1)
    new['self_15_all']=new[['self_1','self_3','self_7','self_15']].sum(axis=1)
    new['self_30_all']=new[['self_1','self_3','self_7','self_15','self_30']].sum(axis=1)
    new['self_60_all']=new[['self_1','self_3','self_7','self_15','self_30','self_60']].sum(axis=1)
    new['comp_3_all']=new[['comp_1','comp_3']].sum(axis=1)
    new['comp_7_all']=new[['comp_1','comp_3','comp_7']].sum(axis=1)
    new['comp_15_all']=new[['comp_1','comp_3','comp_7','comp_15']].sum(axis=1)
    new['comp_30_all']=new[['comp_1','comp_3','comp_7','comp_15','comp_30']].sum(axis=1)
    new['comp_60_all']=new[['comp_1','comp_3','comp_7','comp_15','comp_30','comp_60']].sum(axis=1)
    new['self_1_pct']=new['self_1']/new['all_self_cnt']
    new['self_3_all_pct']=new['self_3_all']/new['all_self_cnt']
    new['self_7_all_pct']=new['self_7_all']/new['all_self_cnt']
    new['self_15_all_pct']=new['self_15_all']/new['all_self_cnt']
    new['self_30_all_pct']=new['self_30_all']/new['all_self_cnt']
    new['self_60_all_pct']=new['self_60_all']/new['all_self_cnt']
    new['all_self_pct']=new['all_self_cnt']/new['all_cnt']
    new['1_pct']=new['self_1']/new['all_cnt']
    new['3_all_pct']=new['self_3_all']/new['all_cnt']
    new['7_all_pct']=new['self_7_all']/new['all_cnt']
    new['15_all_pct']=new['self_15_all']/new['all_cnt']
    new['30_all_pct']=new['self_30_all']/new['all_cnt']
    new['60_all_pct']=new['self_60_all']/new['all_cnt']
    new['comp_3_pct']=new['comp_3_all']/new['self_3_all']
    new['comp_7_pct']=new['comp_7_all']/new['self_7_all']
    new['comp_15_pct']=new['comp_15_all']/new['self_15_all']
    new['comp_30_pct']=new['comp_30_all']/new['self_30_all']
    new['comp_60_pct']=new['comp_60_all']/new['self_60_all']
    new['all_self_comp_pct']= new['all_self_comp_cnt']/new['all_cnt']
    # add
    new['self_3_add_all']=new[['self_1_add','self_3_add']].sum(axis=1)
    new['self_7_add_all']=new[['self_1_add','self_3_add','self_7_add']].sum(axis=1)
    new['self_15_add_all']=new[['self_1_add','self_3_add','self_7_add','self_15_add']].sum(axis=1)
    new['self_30_add_all']=new[['self_1_add','self_3_add','self_7_add','self_15_add','self_30_add']].sum(axis=1)
    new['self_60_add_all']=new[['self_1_add','self_3_add','self_7_add','self_15_add','self_30_add','self_60_add']].sum(axis=1)
    new['self_3_add_pct']=new['self_3_add_all']/new['lxr_num']
    new['self_7_add_pct']=new['self_7_add_all']/new['lxr_num']
    new['self_15_add_pct']=new['self_15_add_all']/new['lxr_num']
    new['self_30_add_pct']=new['self_30_add_all']/new['lxr_num']
    new['self_60_add_pct']=new['self_60_add_all']/new['lxr_num']
    return new


# def load_txt_feat(file: str):
#     with open(file, 'r', encoding='utf-8') as f:
#         feature = f.read().split('\n')
#         feature = [i for i in feature if i]
#         return feature


# def prob2Score(prob, basePoint=550, PDO=30, odds=20):
#     # 将概率转化成分数且为正整数
#     y = np.log(prob / (1 - prob))
#     a = basePoint - y * np.log(odds)
#     y2 = a - PDO / np.log(2) * (y)
#     score = y2.astype('int')
#     return score



if __name__=="__main__":
    """
    BUSI_ID:订单号
    order_time：订单时间
    ADDLIST：联系人列表
    APPLIST：app列表
    MOBILE: 手机号码
    brands：手机BRANDS
    mobile_model：手机mobile_model
    cpu_core：CPU_CORE
    RAM：RAM
    ROM:ROM
    RESOLUTION:RESOLUTION
    campaign_name:渠道名
    WHITE：1表示白名单，0表示非白名单
    is_new：1表示新客，0表示老客
    """

    # 读取测试数据
    with open('wh_df.json','r') as f:
        a=json.loads(''.join(f.readlines()))
    # 转换成dataframe
    data=pd.DataFrame(json.loads(a),index=[0])

    # 处理标签
    camp_maps = {'Organic': 0,
            'vfineads': 1,
            '24h-peso-ad02': 2,
            '24h-peso-ad01': 3,
            'indexplusads': 999,
            'adsnova': 999,
            'xinmiaohudong': 999,
            'yojoy': 999,
            '24h-peso-ad04': 999}

    data[['ram_x', 'ram_y', 'rom_x', 'rom_y']] = data.apply(cal_ram_rom, result_type="expand", axis=1)
    data[['res1', 'res2', 'res3']] = data.apply(cal_res, axis=1, result_type="expand")
    data['ram_pct']=data['ram_x']/data['ram_y']
    data['rom_pct'] = data['rom_x'] / data['rom_y']
    comp = pd.read_excel('philp.xlsx')
    data2=get_feature(data.reset_index(drop=True))
    feature_step2(data2)
    data3 = pd.merge(data[['BUSI_ID', 'WHITE','is_new', 'brands', 'mobile_model',
                           'ram_x', 'ram_y', 'rom_x',
                           'rom_y', 'res1', 'res2', 'res3','campaign_name', 'ram_pct', 'cpu_core']], data2, on='BUSI_ID', how='right')

    ##老客
    if all(data3['is_new']==0):
        lgb_model = joblib.load("old_cust_20220218.pkl")
        in_model_col = load_txt_feat("old_cust_20220218.txt")

        with open('ledict3.json', 'r') as f:
            brand_tran = json.loads(f.read())
        with open('ledict33.json', 'r') as f:
            model_tran = json.loads(f.read())
        model_data = data3[in_model_col]
        # model_data['campaign_name'] = model_data.apply(lambda x: camp_maps.get(x['campaign_name'], 999), axis=1)
        model_data['brands'] = model_data.apply(lambda x: brand_tran.get(x['brands'].lower(), 999), axis=1)
        model_data['mobile_model'] = model_data.apply(lambda x: model_tran.get(x['mobile_model'].lower(), 999), axis=1)
        model_data.fillna(0, inplace=True)
        print(model_data)
        lgb_prob = np.mean([i.predict(model_data) for i in lgb_model], axis=0)[0]
        score = prob2Score(lgb_prob)
        print({'prob': score, 'msg': 'success', 'status_code': 100, })

    # 新客白名单
    elif all(data3['WHITE']==1) and all(data3['is_new']==1):
        lgb_model=joblib.load("new_cust_white_20220219.pkl")
        in_model_col=load_txt_feat("new_cust__white_20220219.txt")

        with open('ledict.json', 'r') as f:
            brand_tran = json.loads(f.read())
        with open('ledict11.json', 'r') as f:
            model_tran = json.loads(f.read())

        model_data=data3[in_model_col]
        model_data['campaign_name']=model_data.apply(lambda x: camp_maps.get(x['campaign_name'],999),axis=1)
        model_data['brands']=model_data.apply(lambda x:brand_tran.get(x['brands'].lower(),999),axis=1)
        model_data['mobile_model']=model_data.apply(lambda x:model_tran.get(x['mobile_model'].lower(),999),axis=1)
        model_data.fillna(0,inplace=True)
        print(model_data)
        lgb_prob = np.mean([i.predict(model_data) for i in lgb_model], axis=0)[0]
        score = prob2Score(lgb_prob)
        print( {'prob': score, 'msg': 'success', 'status_code': 100,})

    # 新客非白名单
    if all(data3['WHITE']==0) and all(data3['is_new']==1):
        lgb_model=joblib.load("new_cust_20220219.pkl")
        in_model_col=load_txt_feat("new_cust_20220219.txt")

        with open('ledict2.json', 'r') as f:
            brand_tran = json.loads(f.read())
        with open('ledict22.json', 'r') as f:
            model_tran = json.loads(f.read())

        model_data=data3[in_model_col]
        model_data['campaign_name']=model_data.apply(lambda x: camp_maps.get(x['campaign_name'],999),axis=1)
        model_data['brands']=model_data.apply(lambda x:brand_tran.get(x['brands'].lower(),999),axis=1)
        model_data['mobile_model']=model_data.apply(lambda x:model_tran.get(x['mobile_model'].lower(),999),axis=1)
        model_data.fillna(0,inplace=True)
        print(model_data)
        lgb_prob = np.mean([i.predict(model_data) for i in lgb_model], axis=0)[0]
        score = prob2Score(lgb_prob)
        print( {'prob': score, 'msg': 'success', 'status_code': 100,})

