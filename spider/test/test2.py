import random

import pymongo
import requests

client = pymongo.MongoClient("localhost", 27017)

db = client["soccerData"]
col_daxiao = db["91vsData"]

failList = set()


def index_of_str(s1, s2):
    lt = s1.split(s2, 1)
    if len(lt) == 1:
        return -1
    return len(lt[0])


daxiao = {'1': '2.50', '2': '2.75', '3': '2.25', '4': '3.00', '5': '3.25', '6': '2.00', '7': '3.50', '8': '3.75',
          '9': '4.00', '10': '1.75', '11': '0.25', '12': '0.50', '13': '0.75', '14': '1.00', '15': '1.25', '16': '1.50',
          '18': '4.25', '19': '4.50', '20': '4.75', '21': '5.00', '22': '5.25', '23': '5.50', '24': '5.75',
          '25': '6.00', '26': '6.25', '27': '6.50', '28': '6.75', '29': '7.00', '30': '7.25', '31': '7.50',
          '32': '7.75', '33': '8.00', '34': '8.25', '35': '8.50', '36': '8.75', '37': '9.00', '38': '9.25',
          '39': '9.50', '40': '9.75', '41': '10.00', '42': '10.25', '43': '10.50', '44': '10.75', '45': '11.00',
          '46': '11.25', '47': '11.50', '48': '11.75', '49': '12.00', '50': '12.25', '51': '12.50', '52': '12.75',
          '53': '13.00', '54': '13.25', '55': '13.50', '56': '13.75', '57': '14.00', '58': '14.25', '59': '14.50',
          '60': '14.75', '61': '15.00', '62': '15.25', '63': '15.50', '64': '15.75', '65': '16.00', '66': '16.25',
          '67': '16.50', '68': '16.75', '69': '17.00', '70': '17.25', '71': '17.50', '72': '17.75', '73': '18.00',
          '74': '18.25', '75': '18.50', '76': '18.75', '77': '19.00', '78': '19.25', '79': '19.50', '80': '19.75',
          '81': '20.0'}

yapan = {'0': "'0'", '1': '4.00', '3': '3.75', '4': '3.50', '5': '3.25', '6': '3.00', '7': '2.75', '8': '2.50',
         '9': '2.25', '10': '2.00', '11': '1.75', '12': '1.50', '13': '1.25', '14': '1.00', '15': '0.75', '16': '0.50',
         '17': '0.25', '19': '0.00', '31': '-0.25', '32': '-0.50', '33': '-0.75', '34': '-1.00', '35': '-1.25',
         '36': '-1.50', '37': '-1.75', '38': '-2.00', '39': '-2.25', '40': '-2.50', '41': '-2.75', '42': '-3.00',
         '43': '-3.25', '44': '-3.50', '45': '-3.75', '46': '-4.00', '47': '-4.25', '48': '-4.50', '49': '-4.75',
         '50': '-5.00', '51': '-5.25', '52': '-5.50', '53': '-5.75', '54': '-6.00', '55': '4.25', '56': '4.50',
         '57': '4.75', '58': '5.00', '59': '5.25', '60': '5.50', '61': '5.75', '62': '6.00', '67': '6.25',
         '68': '-6.25', '69': '6.50', '70': '-6.50', '71': '6.75', '72': '-6.75', '73': '7.00', '74': '-7.00',
         '75': '7.25', '76': '-7.25', '77': '7.50', '78': '-7.50', '79': '7.75', '80': '-7.75', '81': '8.00',
         '82': '-8.00', '83': '8.25', '84': '-8.25', '85': '8.50', '86': '-8.50', '87': '8.75', '88': '-8.75',
         '89': '9.00', '90': '-9.00', '91': '9.50', '92': '-9.50', '93': '9.75', '94': '-9.75', '95': '10.00',
         '96': '-10.00', '97': '10.25', '98': '-10.25', '99': '10.50', '100': '-10.50', '101': '10.75', '102': '-10.75',
         '103': '11.00', '104': '-11.00', '105': '11.25', '106': '-11.25', '107': '11.50', '108': '-11.50',
         '109': '11.75', '110': '-11.75', '111': '12.00', '112': '-12.00', '113': '12.25', '114': '-12.25',
         '115': '12.50', '116': '-12.50', '117': '12.75', '118': '-12.75', '119': '13.00', '120': '-13.00',
         '121': '13.25', '122': '-13.25', '123': '13.50', '124': '-13.50', '125': '13.75', '126': '-13.75',
         '127': '14.00', '128': '-14.00', '129': '14.25', '130': '-14.25', '131': '14.50', '132': '-14.50',
         '133': '14.75', '134': '-14.75', '135': '15.00', '136': '-15.00'}

ips = []


def get_one_match(id, companyId):
    key = {}
    item = {}
    proxies = {
        "http": "45.169.16.1:8080",
    }
    url = ("http://www.baidu.com")
    resp = requests.get(url, proxies=proxies)
    resp.encoding = 'utf-8'
    content = resp.text
    print(content)

    info = content.split(';')[0]
    start_index = index_of_str(info, '[')
    time = info[start_index + 1:].split(',')[7][:11] + " " + info[start_index + 1:].split(',')[7][16:-1] + ":00"
    maGoal = info[start_index + 1:].split(',')[10]
    geGoal = info[start_index + 1:].split(',')[11]
    lianShai = content.split(';')[2]
    start_index = index_of_str(lianShai, '[')
    lianShai = lianShai[start_index:-1][1:-1].split(',')[1][1:-1]

    key['lianShai'] = lianShai
    key['time'] = time
    key['maGoal'] = maGoal
    key['geGoal'] = geGoal

    url = ("http://neiye.90vs.com:3389/odds_new/mingxi/" + companyId + "/a_e_b/1/1/" + id[
                                                                                       :5] + "/" + id + "?d=1632568514490")

    resp = requests.get(url)
    resp.encoding = 'utf-8'
    content = resp.text
    lin_odds = content.split(';')

    yapan_odds = []
    daxiao_odds = []
    oupei_odds = []
    for i in lin_odds:
        if 'd1' in i:
            yapan_odds.append(i)
        if 'd2' in i:
            daxiao_odds.append(i)
        if 'd3' in i:
            oupei_odds.append(i)

    def realOdd(info):
        start_index = index_of_str(info, '(')
        list = info[start_index + 2:].split(',')[:3]
        list[2] = yapan.get(list[2], list[2])
        return list

    def realDaxiao(info):
        start_index = index_of_str(info, '(')
        list = info[start_index + 2:].split(',')[:3]
        list[2] = daxiao.get(list[2], list[2])
        return list

    def realOupei(info):
        start_index = index_of_str(info, '(')
        list = info[start_index + 2:].split(',')[:3]
        return [list[0], list[2], list[1]]

    lin_yanpan_start_info = []
    lin_yanpan_end_info = []
    lin_daxiao_start_info = []
    lin_daxiao_end_info = []
    lin_oupei_start_info = []
    lin_oupei_end_info = []
    type = "lin"
    num = "1"

    if len(yapan_odds) != 0:
        lin_yanpan_start_info = realOdd(yapan_odds[0])
        lin_yanpan_end_info = realOdd(yapan_odds[len(yapan_odds) - 1])
        item['ya_' + type + '_start_maOdd_' + num] = lin_yanpan_start_info[0]
        item['ya_' + type + '_start_geOdd_' + num] = lin_yanpan_start_info[1]
        item['ya_' + type + '_start_pan_' + num] = lin_yanpan_start_info[2]

        item['ya_' + type + '_end_maOdd_' + num] = lin_yanpan_end_info[0]
        item['ya_' + type + '_end_geOdd_' + num] = lin_yanpan_end_info[1]
        item['ya_' + type + '_end_pan_' + num] = lin_yanpan_end_info[2]
    if len(daxiao_odds) != 0:
        lin_daxiao_start_info = realDaxiao(daxiao_odds[0])
        lin_daxiao_end_info = realDaxiao(daxiao_odds[len(daxiao_odds) - 1])
        item['da_' + type + '_start_maOdd_' + num] = lin_daxiao_start_info[0]
        item['da_' + type + '_start_geOdd_' + num] = lin_daxiao_start_info[1]
        item['da_' + type + '_start_pan_' + num] = lin_daxiao_start_info[2]

        item['da_' + type + '_end_maOdd_' + num] = lin_daxiao_end_info[0]
        item['da_' + type + '_end_geOdd_' + num] = lin_daxiao_end_info[1]
        item['da_' + type + '_end_pan_' + num] = lin_daxiao_end_info[2]

    if len(oupei_odds) != 0:
        lin_oupei_start_info = realOupei(oupei_odds[0])
        lin_oupei_end_info = realOupei(oupei_odds[len(oupei_odds) - 1])
        item['ou_' + type + '_start_maOdd_' + num] = lin_oupei_start_info[0]
        item['ou_' + type + '_start_pinOdd_' + num] = lin_oupei_start_info[1]
        item['ou_' + type + '_start_geOdd_' + num] = lin_oupei_start_info[2]
        item['ou_' + type + '_end_maOdd_' + num] = lin_oupei_end_info[0]
        item['ou_' + type + '_end_pinOdd_' + num] = lin_oupei_end_info[1]
        item['ou_' + type + '_end_geOdd_' + num] = lin_oupei_end_info[2]

    url = ("http://neiye.90vs.com:3389/odds_new/mingxi/" + companyId + "/a_e_b_z/1/1/" + id[
                                                                                         :5] + "/" + id + "?d=1632568514490")
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    content = resp.text
    lin_odds = content.split(';')

    yapan_odds = []
    daxiao_odds = []
    oupei_odds = []
    for i in lin_odds:
        start_index = index_of_str(i, '(')
        if 'd4' in i and 'h' in i[start_index:]:
            yapan_odds.append(i)
        if 'd5' in i and 'h' in i[start_index:]:
            daxiao_odds.append(i)
        if 'd6' in i and 'h' in i[start_index:]:
            oupei_odds.append(i)

    lin_yanpan_start_info = []
    lin_yanpan_end_info = []
    lin_daxiao_start_info = []
    lin_daxiao_end_info = []
    lin_oupei_start_info = []
    lin_oupei_end_info = []
    type = 'mid'

    if len(yapan_odds) != 0:
        midInfo = yapan_odds[len(yapan_odds) - 1]
        start_index = index_of_str(midInfo, '(')
        list = midInfo[start_index + 2:].split(',')[4:6]
        item['mid_maGoal'] = list[0]
        item['mid_geGoal'] = list[1]

        lin_yanpan_start_info = realOdd(yapan_odds[0])
        lin_yanpan_end_info = realOdd(yapan_odds[len(yapan_odds) - 1])
        item['ya_' + type + '_start_maOdd_' + num] = lin_yanpan_start_info[0]
        item['ya_' + type + '_start_geOdd_' + num] = lin_yanpan_start_info[1]
        item['ya_' + type + '_start_pan_' + num] = lin_yanpan_start_info[2]

        item['ya_' + type + '_end_maOdd_' + num] = lin_yanpan_end_info[0]
        item['ya_' + type + '_end_geOdd_' + num] = lin_yanpan_end_info[1]
        item['ya_' + type + '_end_pan_' + num] = lin_yanpan_end_info[2]

    if len(daxiao_odds) != 0:
        lin_daxiao_start_info = realDaxiao(daxiao_odds[0])
        lin_daxiao_end_info = realDaxiao(daxiao_odds[len(daxiao_odds) - 1])
        item['da_' + type + '_start_maOdd_' + num] = lin_daxiao_start_info[0]
        item['da_' + type + '_start_geOdd_' + num] = lin_daxiao_start_info[1]
        item['da_' + type + '_start_pan_' + num] = lin_daxiao_start_info[2]

        item['da_' + type + '_end_maOdd_' + num] = lin_daxiao_end_info[0]
        item['da_' + type + '_end_geOdd_' + num] = lin_daxiao_end_info[1]
        item['da_' + type + '_end_pan_' + num] = lin_daxiao_end_info[2]

    if len(oupei_odds) != 0:
        lin_oupei_start_info = realOupei(oupei_odds[0])
        lin_oupei_end_info = realOupei(oupei_odds[len(oupei_odds) - 1])
        item['ou_' + type + '_start_maOdd_' + num] = lin_oupei_start_info[0]
        item['ou_' + type + '_start_pinOdd_' + num] = lin_oupei_start_info[1]
        item['ou_' + type + '_start_geOdd_' + num] = lin_oupei_start_info[2]

        item['ou_' + type + '_end_maOdd_' + num] = lin_oupei_end_info[0]
        item['ou_' + type + '_end_pinOdd_' + num] = lin_oupei_end_info[1]
        item['ou_' + type + '_end_geOdd_' + num] = lin_oupei_end_info[2]

    url = ("http://neiye.90vs.com:3389/odds_new/mingxi/" + companyId + "/a_e_b/1/2/" + id[
                                                                                       :5] + "/" + id + "?d=1632568514490")

    resp = requests.get(url)
    resp.encoding = 'utf-8'
    content = resp.text
    lin_odds = content.split(';')

    yapan_odds = []
    daxiao_odds = []
    for i in lin_odds:
        start_index = index_of_str(i, '(')
        if 'd1' in i:
            yapan_odds.append(i)
        if 'd2' in i:
            daxiao_odds.append(i)

    lin_yanpan_start_info = []
    lin_yanpan_end_info = []
    lin_daxiao_start_info = []
    lin_daxiao_end_info = []
    type = 'lin'
    num = '2'

    if len(yapan_odds) != 0:
        lin_yanpan_start_info = realOdd(yapan_odds[0])
        lin_yanpan_end_info = realOdd(yapan_odds[len(yapan_odds) - 1])
        item['ya_' + type + '_start_maOdd_' + num] = lin_yanpan_start_info[0]
        item['ya_' + type + '_start_geOdd_' + num] = lin_yanpan_start_info[1]
        item['ya_' + type + '_start_pan_' + num] = lin_yanpan_start_info[2]

        item['ya_' + type + '_end_maOdd_' + num] = lin_yanpan_end_info[0]
        item['ya_' + type + '_end_geOdd_' + num] = lin_yanpan_end_info[1]
        item['ya_' + type + '_end_pan_' + num] = lin_yanpan_end_info[2]

    if len(daxiao_odds) != 0:
        lin_daxiao_start_info = realDaxiao(daxiao_odds[0])
        lin_daxiao_end_info = realDaxiao(daxiao_odds[len(daxiao_odds) - 1])
        item['da_' + type + '_start_maOdd_' + num] = lin_daxiao_start_info[0]
        item['da_' + type + '_start_geOdd_' + num] = lin_daxiao_start_info[1]
        item['da_' + type + '_start_pan_' + num] = lin_daxiao_start_info[2]

        item['da_' + type + '_end_maOdd_' + num] = lin_daxiao_end_info[0]
        item['da_' + type + '_end_geOdd_' + num] = lin_daxiao_end_info[1]
        item['da_' + type + '_end_pan_' + num] = lin_daxiao_end_info[2]

    url = ("http://neiye.90vs.com:3389/odds_new/mingxi/" + companyId + "/a_e_b_z/1/2/" + id[
                                                                                         :5] + "/" + id + "?d=1632568514490")

    resp = requests.get(url)
    resp.encoding = 'utf-8'
    content = resp.text
    lin_odds = content.split(';')

    yapan_odds = []
    daxiao_odds = []
    for i in lin_odds:
        start_index = index_of_str(i, '(')
        if 'd4' in i and 'h' in i[start_index:]:
            yapan_odds.append(i)
        if 'd5' in i and 'h' in i[start_index:]:
            daxiao_odds.append(i)

    lin_yanpan_start_info = []
    lin_yanpan_end_info = []
    lin_daxiao_start_info = []
    lin_daxiao_end_info = []
    type = 'mid'

    if len(yapan_odds) != 0:
        lin_yanpan_start_info = realOdd(yapan_odds[0])
        lin_yanpan_end_info = realOdd(yapan_odds[len(yapan_odds) - 1])
        item['ya_' + type + '_start_maOdd_' + num] = lin_yanpan_start_info[0]
        item['ya_' + type + '_start_geOdd_' + num] = lin_yanpan_start_info[1]
        item['ya_' + type + '_start_pan_' + num] = lin_yanpan_start_info[2]

        item['ya_' + type + '_end_maOdd_' + num] = lin_yanpan_end_info[0]
        item['ya_' + type + '_end_geOdd_' + num] = lin_yanpan_end_info[1]
        item['ya_' + type + '_end_pan_' + num] = lin_yanpan_end_info[2]

    if len(daxiao_odds) != 0:
        lin_daxiao_start_info = realDaxiao(daxiao_odds[0])
        lin_daxiao_end_info = realDaxiao(daxiao_odds[len(daxiao_odds) - 1])
        item['da_' + type + '_start_maOdd_' + num] = lin_daxiao_start_info[0]
        item['da_' + type + '_start_geOdd_' + num] = lin_daxiao_start_info[1]
        item['da_' + type + '_start_pan_' + num] = lin_daxiao_start_info[2]

        item['da_' + type + '_end_maOdd_' + num] = lin_daxiao_end_info[0]
        item['da_' + type + '_end_geOdd_' + num] = lin_daxiao_end_info[1]
        item['da_' + type + '_end_pan_' + num] = lin_daxiao_end_info[2]
    if len(item) != 0:
        col_daxiao.update_one(key,
                              {'$set': item},
                              upsert=True)
    print(key, item)
    return id

get_one_match("12058589", "397")
get_one_match("12058589", "470")
get_one_match("12058589", "589")
get_one_match("12058589", "516")
