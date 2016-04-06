# -*- coding:utf-8 -*-

import requests

PHONE_ATTR_JUHE = """http://apis.juhe.cn/mobile/get?phone={phone}&dtype=&key=820a01a91cbf7a04aecb62cf9a229670"""
PHONE_ATTR_360 = """http://cx.shouji.360.cn/phonearea.php?number={phone}"""
IP_INFO_TAOBAO = "http://ip.taobao.com/service/getIpInfo.php?ip={ip}"


def get_number_attribution_360(phone):
    """360查询号码归属地"""

    r = requests.get(PHONE_ATTR_360.format(phone=phone))
    result = r.json()

    province = result.get("data").get("province")

    if isinstance(province, unicode):
        province = province.encode("utf-8")
    else:
        province = province

    if not province:
        province = "null"
        city = "null"
    else:
        if province in ("北京", "天津", "上海", "重庆"):
            city = province
        else:
            city = result.get("data").get("city")

        if isinstance(city, unicode):
            city = city.encode("utf-8")
        else:
            city = city

    return {"phone": phone, "province": province, "city": city}


def get_number_attribution(phone):
    """号码归属地查询
    1。聚合API
    2.360API"""
    try:
        phone = int(phone)
    except ValueError:
        return {"phone": phone, "province": "", "city": ""}

    r = requests.get(PHONE_ATTR_JUHE.format(phone=phone))
    result = r.json()

    if result.get("resultcode") == "200":
        province = result.get("result").get("province")
        city = result.get("result").get("city")

        if isinstance(province, unicode):
            province = province.encode("utf-8")
        else:
            province = province

        if isinstance(city, unicode):
            city = city.encode("utf-8")
        else:
            city = city

        res = {"phone": phone, "province": province, "city": city}
    else:
        res = get_number_attribution_360(phone)

    return res


def get_ip_info(ip):
    """IP地址归属地"""
    r = requests.post(IP_INFO_TAOBAO.format(ip=ip))
    content = r.json()
    print content

    if content.get("code"):
        return {"ip": ip, "region": -1, "region_id": -1}

    region = content.get("data").get("region")
    region_id = content.get("data").get("region_id")

    if isinstance(region, unicode):
        region = region.encode("utf-8")
    else:
        region = region

    if isinstance(region_id, unicode):
        region_id = region_id.encode("utf-8")
    else:
        region_id = region_id

    return {"ip": ip, "region": region, "region_id": region_id}


def chinese_zodiac(year):
    """生肖"""
    return u'猴鸡狗猪鼠牛虎兔龙蛇马羊'[year%12]


def zodiac(month, day):
    """星座"""
    n = (u'摩羯座',u'水瓶座',u'双鱼座',u'白羊座',u'金牛座',u'双子座',
         u'巨蟹座',u'狮子座',u'处女座',u'天秤座',u'天蝎座',u'射手座')
    d = ((1,20),(2,19),(3,21),(4,21),(5,21),(6,22),(7,23),(8,23),(9,23),(10,23),(11,23),(12,23))
    return n[len(filter(lambda y:y<=(month,day), d))%12]


if __name__ == "__main__":
    print get_number_attribution(phone="13716710140")
    print chinese_zodiac(2016)
    print zodiac(04, 06)
    print get_ip_info("")