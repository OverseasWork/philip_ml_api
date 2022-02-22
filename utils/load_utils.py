# -*- coding: utf-8 -*-
# @Time    : 2021/3/24 9:47 上午
# @Author  : HuangSir
# @FileName: load_utils.py
# @Software: PyCharm
# @Desc:

import sys
sys.path.append('..')


def load_txt_feat(file: str):
    with open(file, 'r', encoding='utf-8') as f:
        feature = f.read().split('\n')
        feature = [i for i in feature if i]
        return feature