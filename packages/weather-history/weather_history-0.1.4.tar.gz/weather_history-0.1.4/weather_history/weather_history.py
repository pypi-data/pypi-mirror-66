from urllib.request import urlopen
import re
import pandas as pd
def history_data(city='beijing',year=2019,month=11):
    year=str(year)
    if month<10:
        month="0"+str(month)
    else:
        month=str(month)
    url="http://www.tianqihoubao.com/lishi/"+city+"/month/"+year+month+".html"
    
    page=urlopen(url).read().decode('gbk')
    
    tables=re.findall(r'<table(.*?)</table>',page,re.S)
    
    val1=re.findall(r'<tr(.*?)</tr>',tables[0],re.S)
    
    data=[]
    for v in val1[1:]:
        b=re.findall(r'<td>(.*?)</td>',v,re.S)
        d=re.findall(r'title=(.*)</a>',b[0],re.S)
        date=re.search(r'\d{4}年\d{1,2}月\d{1,2}日',d[0]).group()
        s=';'.join(i.replace("\r\n","").replace(" ","") for i in b[1:])
        sl=s.split(";")
        weather=sl[0]
        temp=sl[1]
        wind=sl[2]
        data.append({"日期":date,
                     "天气":weather,
                     "温度":temp,
                     "风向":wind})
    
    data=pd.DataFrame(data)
    data=data[['日期','天气','温度','风向']]
    return data

if __name__=='__main__':
    data2=history_data(year=2020,month=1)
