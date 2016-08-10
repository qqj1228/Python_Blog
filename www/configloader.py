#!/usr/bin/env python3
# coding:utf-8

import json
import os


class DotDict(dict):
    '''
    Simple dict but support access as x.y style.
    '''

    def __init__(self, names=(), values=(), **kw):
        super().__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'DotDict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


def merge(default, user):
    r = {}
    for k, v in default.items():
        if k in user:
            if isinstance(v, dict):
                r[k] = merge(v, user[k])
            else:
                r[k] = user[k]
        else:
            r[k] = v
    return r


def toDotDict(d):
    D = DotDict()
    for k, v in d.items():
        D[k] = toDotDict(v) if isinstance(v, dict) else v
    return D

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')


# 因json不支持注释，故每读取一行判断是否为注释，最后再转换json
with open(path + '/default.cfg', 'r') as fp:
    s = ''
    for line in fp.readlines():
        if line.strip().startswith('//'):
            continue
        s = s + line.strip()
    configs = json.loads(s)

try:
    with open(path + '/user.cfg', 'r') as fp:
        s = ''
        for line in fp.readlines():
            if line.strip().startswith('//'):
                continue
            s = s + line.strip()
        user_cfg = json.loads(s)
        configs = merge(configs, user_cfg)
except IOError:
    pass

configs = toDotDict(configs)
