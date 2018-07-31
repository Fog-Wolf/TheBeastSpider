#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: wang

import os, sys
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "Flower"])
execute(["scrapy", "crawl", "Goods"])
