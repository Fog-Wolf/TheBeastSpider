#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: wang
import sys
from TheBeastSpider.settings import USERNAME, PASSWORD


def get_session():
    from selenium import webdriver
    brower = webdriver.Chrome(executable_path="D:/python/chromedriver.exe")
    brower.get("http://www.thebeastshop.com/user/login.htm")
    brower.find_element_by_css_selector(".m-login .m-form-group #J_UserName").send_keys(USERNAME)
    brower.find_element_by_css_selector(".m-login .m-form-group #J_UserPassword").send_keys(PASSWORD)
    brower.find_element_by_css_selector(".m-login .m-form-group #J_Login").click()
    import time
    time.sleep(5)
    Cookies = brower.get_cookies()
    # get the session cookie
    cookie = [item["name"] + "=" + item["value"] for item in Cookies]
    # print cookie
    cookiestr = ';'.join(item for item in cookie)
    print(cookiestr)
    # 存放获取的有用COOKIES
    cookie_dict = {}
    import pickle
    for cookie in Cookies:
        # 写入文件
        f = open(sys.path[0] + "/cookies/" + cookie['name'] + ".beast", "wb")
        pickle.dump(cookie, f)
        f.close()
        cookie_dict[cookie['name']] = cookie["value"]
    brower.close()
    return cookiestr
