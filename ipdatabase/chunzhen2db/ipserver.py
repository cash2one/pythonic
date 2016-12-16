# -*- coding:utf-8 -*-

import time
from statistics import Statistics

def _time_it(func):
    def _deco(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        print 'running time:', time.time() - start
        return ret

    return _deco


class IP2Address(Statistics):

    def gen_ip_view(self):
        """ IP地址段视图 """
        sql = """SELECT province_id, province_name, sip, eip FROM ifashion.ip_view
        WHERE show_status = '1' """
        result = self.dbi.query(sql).fetch_row(0, 1)

        ip_view = []
        for each in result:
            ip = self._string2intip(each["sip"])
            ip_view.append((ip, each["province_id"], each["province_name"]))
        return ip_view

    @staticmethod
    def _string2intip(s):
        """
        把一个字符串形式的ip地址转化为一个int值
        """
        ss = s.split('.')
        ip = 0
        for i in ss:
            ip = (ip << 8) + int(i)
        return ip

    @staticmethod
    def _intip2string(ip):
        """
        把一个int值形式的ip地址转化为一个字符串
        """
        a = (ip & 0xff000000) >> 24
        b = (ip & 0x00ff0000) >> 16
        c = (ip & 0x0000ff00) >> 8
        d = ip & 0x000000ff
        return "%d.%d.%d.%d" % (a, b, c, d)

    @staticmethod
    def _find(li, a):
        """
            二分法查找list中小于等于a的最大值的索引
        """
        l, r = 0, len(li) - 1
        if a < li[l][0] or a > li[r][0]:
            return -1

        m = (l + r) / 2
        while l < r:
            if li[m][0] <= a:
                l = m
                if li[m][0] == a or li[m + 1][0] > a:
                    return m
            else:
                r = m
                if li[m - 1][0] <= a:
                    return m - 1
            m = (l + r) / 2

    def get_ip_location(self, ip_view, query_ip):
        """ IP地址所在地 """
        ret = self._find(ip_view, self._string2intip(query_ip))
        if ip_view[ret][1] == "0":
            return None
        return {"province_id" : ip_view[ret][1], "province_name": ip_view[ret][2]}


if __name__ == '__main__':
    op = IP2Address()
    ip_view = op.gen_ip_view()
    iplocation = op.get_ip_location(ip_view, "123.59.24.231")
    if iplocation:
        print iplocation
    else:
        print "not find"
