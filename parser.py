import pandas as pd
import ast
import json
import requests
import xmltodict
from pandas.io.json import json_normalize #package for flattening json in pandas df


pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 40)


df2 = pd.DataFrame()

def find_str(l, subs):
    for i, s in enumerate(l):
        if subs in s:
              return s
    return ""
itemz = []

with open('app3.log') as f:
   items = f.read().split("**********************************************")[1:]
   print (len(items))
   i = 0 
   for s in items:
          i+=1 
          if (i%1000 ==0 ):
             print("i " + str(i))
             df = pd.DataFrame(itemz)
             df.to_csv('DF32.csv')
          item = {}
          lines = s.splitlines()
          if ("Forwarded:" in s):
              item['path'] = find_str(lines, "/img/").lstrip("/img/")
              item['date'] = find_str(lines, "time").lstrip('time: ')[:10]
              item['time'] = find_str(lines, "time").lstrip('time: ')[11:]
              #item['Referer'] = lines[5].lstrip('Referer: ')
              item['User-Agent'] = find_str(lines, "User-Agent").lstrip('User-Agent: ')
              item['Connection'] = find_str(lines, "Connection").lstrip('Connection: ')
              item['cookie'] = find_str(lines, "MMM COOKIE").lstrip("MMM COOKIE ").rstrip("@@@")
              #item['Upgrade-Insecure-Requests'] = lines[10].strip('Upgrade-Insecure-Requests: ')
              item['Accept']          = find_str(lines, "Accept:").lstrip('Accept: ')
              item['Accept-Language'] = find_str(lines, "Accept-Language:").lstrip('Accept-Language: ')
              item['Accept-Encoding'] = find_str(lines, "Accept-Encoding:").lstrip('Accept-Encoding: ')
              url = "https://freegeoip.app/xml/"
              ip = find_str(lines, "Forwarded: for=").lstrip('Forwarded: for="').rstrip('"')
              ipp = [itm for itm in itemz if itm["IP"] == ip]
              item['IP'] = ip
              if bool(ipp):
                  ipp = ipp[0]
                  
                  item['CountryCode'] = ipp['CountryCode']
                  item['RegionCode'] = ipp['RegionCode']
                  item['City'] = ipp['City']
                  item['ZipCode'] = ipp['ZipCode']
              else:  
                  response = requests.get(url+ip)
                  try:
                    response = xmltodict.parse(response.text)['Response']
                  except:
                    print("error parsing XML dict!")
                    print(s + " @@@\n")
                    print(response.text + " @@@\n")
                    print(ip + " @@@\n")
                    continue

                  item['IP'] = ip
                  item['CountryCode'] = response['CountryCode']
                  item['RegionCode'] = response['RegionCode']
                  item['City'] = response['City']
                  item['ZipCode'] = response['ZipCode']
              itemz.append(item)


df = pd.DataFrame(itemz)
df.to_csv('DF2_new.csv') 


df


