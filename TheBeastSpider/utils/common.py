#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: wang
import hashlib


def get_md5(url):
    # 判断参数是否为unicode
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def con_dic(url,dic,suffix):
    new_url = []
    for value in dic:
        new_url.append(url+value+'.'+suffix)

    return new_url

