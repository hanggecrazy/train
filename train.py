#!/usr/bin/python3 
# -*-coding:utf-8-*-

import urllib.request,sys,json,ssl

from prettytable import PrettyTable

def get_station_list():
    f = open('stations.db')
    lines = f.readlines()
    dic = {}
    for line in lines:
        line = line.strip('\n')
        dic[line.split(' ')[0]] = line.split(' ')[1]
    return dic

def get_content(url):
    req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}
    req = urllib.request.Request(url, None, req_header)
    resp = urllib.request.urlopen(req,None,30)
    content = resp.read()
    return content

if __name__=='__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        train_date   = sys.argv[1]
        from_station = get_station_list()[sys.argv[2]]
        to_station   = get_station_list()[sys.argv[3]]
    except:
        print('usage: python train.py 201X-XX-XX 出发站 到到站')
        sys.exit(0)
        pass
    while 1 == 1:
        #os.system('clear')
        url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=' + train_date + '&leftTicketDTO.from_station=' + from_station + '&leftTicketDTO.to_station=' + to_station + '&purpose_codes=ADULT'

        content = get_content(url)
        j = json.loads(content)
        t = PrettyTable(["车次", "出发站", "到达站", "出发时间", "到达时间", "历时", "总站数", "商务座", "特等座", "一等座", "二等座", "软卧", "硬卧", "软座", "硬座", "无座"])
        t.align[u"出发站"] = "l" # Left align city names
        t.align[u'到达站'] = 'l'
        t.padding_width = 1 # One space between column edges and contents (default)
        if j == -1 or j['status'] == False: 
            print('接口输出错误')	
            sys.exit(0)
        if 'message' in j['data'] and j['data']['message'] is not '': 
            print (j['data']['message'])	
            sys.exit(0)
        print ('日期：\033[1;32;40m%s\033[0m    从 \033[1;31;40m%s\033[0m 到 \033[1;31;40m%s\033[0m'%(train_date, sys.argv[2], sys.argv[3]) + '    共计车次：［ \033[1;31;40m%s\033[0m'%(str(len(j['data']['result']))) + ' ］班')

        for sstr in j['data']['result']:
            item = sstr.split('|')
            url = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no=' + item[2]+'&from_station_no=' + item[16] + '&to_station_no=' + item[17] + '&seat_types=' + item[34] + '&train_date=' + train_date
            #print(url)
            #ct = get_content(url)
            #jl = json.loads(ct)
            #jl['data']
            t.add_row([
                item[3], #车次
                j['data']['map'][item[6]],#出发站
                j['data']['map'][item[7]],#到达站
                item[8] if item[8] is not '' else '--',#出发时间
                item[9] if item[9] is not '' else '--',#达到时间
                item[10] if item[10] is not '' else '--',#历时
                int(item[17]) - int(item[16]) if item[17] is not '' else '--',#总站数
                item[32] if item[32] is not '' else '--',#商务座
                item[25] if item[25] is not '' else '--',#特等座
                item[31] if item[31] is not '' else '--',#一等座
                item[30] if item[30] is not '' else '--',#二等座
                item[23] if item[23] is not '' else '--',#软卧
                item[28] if item[28] is not '' else '--',#硬卧
                item[27] if item[27] is not '' else '--',#软座
                item[29] if item[29] is not '' else '--',#硬座
                item[26] if item[26] is not '' else '--'#无座
            ])
            
        print(t)
        sys.exit(0)

