import requests
import csv
import config


Url = 'https://search.censys.io/api/v2'
ch = config.config()
api=ch[0]
secret=ch[1]
query=''
PageNm=int
CheckList=[]

def getIps(ips):
    with open('Hosts.txt','a') as f:
        f.write(f'{ips}\n')
        f.close


def LastActivity(PageNUM,LastPage,Next='N'):
    data=[query,PageNUM,LastPage,Next]
    with open('Info.csv','a') as csvfile:
        writer=csv.writer(csvfile)
        writer.writerow(data)
        csvfile.close()




def CheckInfo():
    
    with open ('Info.csv','r') as csvf :
        try:
            reader = csv.reader(csvf)
            for row in reader:
                if query in list(row):
                    CheckList.append(row)
            lastrow=list.pop(CheckList)
            if lastrow[3] == "Y":
                print(f"[!] The last page of this query ({lastrow[0]}) is {int(lastrow[1])}. The next page does not exist!")
                
                exit()
            x = input(f"[!] This query ({lastrow[0]}) has already been used for {lastrow[1]} pages. Do you want to start from page {int(lastrow[1])+1} onwards? (y/n): ").upper()

            if x== 'Y':
                return int(lastrow[1]) , lastrow[2]
            elif x=='N':
                return None
            if x!= 'Y' or 'N':
                exit()
            csvf.close()
        except IndexError :
            return None

def request():

    params = {'q':query,'per_page':0,'virtual_hosts':'EXCLUDE'}
    res = requests.post(Url+'/hosts/search',json=params,auth=(api,secret))
    payload = res.json()
    CheckError(payload['code'])
    if payload['status']=='OK':
        result = payload["result"]
        page=result["links"]["next"] 
        return page



def getcursor1(pageNum):
    cn =1
    has_next_key = False
    next = ""
    params2 = {'cursor':request(),'q':query,'per_page':27,'virtual_hosts':'EXCLUDE'}
    res2 = requests.post(Url+'/hosts/search',json=params2,auth=(api,secret))
    payload2 = res2.json()
    if payload2['code'] ==200:
        result = payload2["result"]['hits']
        for reader in result:
            ip =reader['ip']
            services = reader['services']
            for port in services:
                if port['service_name'] == "HTTP":
                    print('%s:%s'%(ip,port['port']))
                    getIps('%s:%s'%(ip,port['port']))
        if 'next' in payload2['result']['links']:
            has_next_key = True
            next=payload2['result']['links']['next']


        else:
            CheckError(payload2['code'])
            
    while has_next_key and cn !=pageNum :
        
        
        params3 = {'cursor':next,'q':query,'per_page':25,'virtual_hosts':'EXCLUDE'}

        req =requests.post(Url+'/hosts/search',json=params3,auth=(api,secret))
        payload3 = req.json()
        CheckError(payload3['code'])
        result2 = payload3["result"]['hits']
        for reader2 in result2:
            ip =reader2['ip']
            services = reader2['services']
            for port in services:
                if port['service_name'] == "HTTP":
                    print('%s:%s'%(ip,port['port']))
                    getIps('%s:%s'%(ip,port['port']))
        if 'next' in payload3['result']['links']:
            next=payload3['result']['links']['next']
            cn +=1
        if cn ==pageNum:
            LastActivity(cn,next)
        if payload3['result']['links']['next'] == '':
            print('The next page does not exist')
            LastActivity(cn,next,'Y')
            exit()
            

def getcursor2(LastPage,cursor,numbberOfpages):
    cn =LastPage
    flag= cn +numbberOfpages
    has_next_key = False
    next = ""
    params2 = {'cursor':cursor,'q':query,'per_page':25,'virtual_hosts':'EXCLUDE'}
    res2 = requests.post(Url+'/hosts/search',json=params2,auth=(api,secret))
    payload2 = res2.json()
    if payload2['code'] ==200:
        result = payload2["result"]['hits']
        for reader in result:
            ip =reader['ip']
            services = reader['services']
            for port in services:
                if port['service_name'] == "HTTP":
                    print('%s:%s'%(ip,port['port']))
                    getIps('%s:%s'%(ip,port['port']))
        if 'next' in payload2['result']['links']:
            has_next_key = True
            next=payload2['result']['links']['next']

            
        else:
            CheckError(payload2['code'])
            
    while has_next_key and cn !=flag :        
        params3 = {'cursor':next,'q':query,'per_page':25,'virtual_hosts':'EXCLUDE'}

        req =requests.post(Url+'/hosts/search',json=params3,auth=(api,secret))
        payload3 = req.json()
        CheckError(payload3['code'])
        result2 = payload3["result"]['hits']
        for reader2 in result2:
            ip =reader2['ip']
            services = reader2['services']
            for port in services:
                if port['service_name'] == "HTTP":
                    print('%s:%s'%(ip,port['port']))
                    getIps('%s:%s'%(ip,port['port']))
        if 'next' in payload3['result']['links']:
            next=payload3['result']['links']['next']
            cn +=1
        if cn ==flag:
            LastActivity(cn,next)
        if payload3['result']['links']['next'] == '':
            print('The next page does not exist')
            LastActivity(cn,next,'Y')
            exit()


def CheckError(Code):
    if Code==400:
        print('[!] Invalid search. Your query could not be parsed')
    elif Code==401:
        print('[!] You must authenticate with a valid API ID and secret.')
    elif Code==403:
        print('[!] Access was denied for this resource or feature.')
    elif Code==422:
        print('[!] Invalid cursor')
    elif Code==403:
        print('[!] Access was denied for this resource or feature.')
    elif Code==429:
        print('[!] You have used your full quota for this billing period')


def run():
    checker= CheckInfo()
    if checker ==None:
        getcursor1(PageNm)
        print('[+] Check Hosts.txt')
    elif checker != None:
        getcursor2(checker[0],checker[1],PageNm)
        print('[+] Check Hosts.txt')
        