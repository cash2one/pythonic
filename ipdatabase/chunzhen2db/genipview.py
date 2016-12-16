# -*- coding:utf-8 -*-

base = ""

def get_school_dict():
    """ 高校映射 """

    school_dict = {}
    fr = open("{0}/school".format(base), "r")
    for line in fr:
        lines = line.strip().split()
        school = lines[0]
        province = lines[1]
        school_dict[school] = province
    fr.close()
    return school_dict


def get_city_dict():
    """ 城市映射 """
    city_dict = {}
    fr = open("{0}/city".format(base), "r")

    for col, line in enumerate(fr):
        lines = line.split("\n")[0].strip().split(",") 
        if "省" in lines[1]:
            _short_name = lines[1].split("省")

        elif "自治区" in lines[1]:
            _short_name = lines[1].split("自治区")

        elif "特别行政区" in lines[1]:
            _short_name = lines[1].split("特别行政区")

        else:
            _short_name = lines[1].split("市")
        
        short_name = _short_name[0].replace("壮族", "").replace("回族", "").replace("维吾尔", "")

        city_dict[short_name] = lines[0:2] + [lines[2].upper()]
        
    fr.close()     
    return city_dict


def gen_ipview(city_dict):    
    """ 获取IP地址段 """  

    school_dict = get_school_dict()
    city_dict = get_city_dict()

    ipview = [["province_id", "province_name", "short_name", "sip", "eip", "detail", "show_status"]]

    fr = open("{0}/czip".format(base), "r")
    for col, line in enumerate(fr):
        lines = line.split()
        if len(lines) < 2:
            print lines
            continue

        sip = lines[0]       
        eip = lines[1]
        location = lines[2]
        detail = "".join(lines[2:])
        
        is_find = False
        for short_name in city_dict:
            if short_name not in location:
                continue
            is_find = True
            info = city_dict.get(short_name, []) + [sip, eip, detail]
            ipview.append(info)
            break
 
        if "大学" in location:
            short_name = school_dict.get(location, None)
            if short_name:
                info = city_dict.get(short_name, []) + [sip, eip, detail]
                ipview.append(info)
                is_find = True

        if not is_find:
            ipview.append(["0", "0", "", sip, eip, detail])

    fr.close()

    fw = open("{0}/ipview".format(base), "w")
    for line in ipvew:
        fw.write("\t".join(map(str, line + ["1"])) + "\n")
    fw.close()


gen_ipview()

