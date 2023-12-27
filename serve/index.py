# -*- coding: UTF-8 -*-
import requests
import re
from http.server import BaseHTTPRequestHandler
import json

def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]

# 安全转换字符串到整数，遇到无法转换的字符串返回0
def safe_int_conversion(s):
    try:
        return int(s)
    except ValueError:
        return 0

def getdata(name):
    gitpage = requests.get("https://github.com/" + name)
    data = gitpage.text
    datadatereg = re.compile(r'data-date="(.*?)" id="contribution-day-component')
    datacountreg = re.compile(r'<tool-tip .*?class="sr-only position-absolute">(.*?) contribution')
    datadate = datadatereg.findall(data)
    datacount = datacountreg.findall(data)
    
    # 使用safe_int_conversion函数转换datacount中的每个项
    datacount = [safe_int_conversion(i) for i in datacount]

    # 将datadate和datacount按照字典序排序
    sorted_data = sorted(zip(datadate, datacount))
    datadate, datacount = zip(*sorted_data)
    
    contributions = sum(datacount)
    datalist = []
    for index, item in enumerate(datadate):
        itemlist = {"date": item, "count": datacount[index]}
        datalist.append(itemlist)
    datalistsplit = list_split(datalist, 7)
    returndata = {
        "total": contributions,
        "contributions": datalistsplit
    }
    return returndata

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        user = path.split('?')[1]
        data = getdata(user)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
        return
