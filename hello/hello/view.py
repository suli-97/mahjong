from django.http import HttpResponse
from django.shortcuts import render
import pymysql
db = pymysql.connect(host="localhost",user="lisu",password="Ls3314188",database="mahjong")
cursor = db.cursor()

mapping = ["九万","八万","七万","六万","五万","四万","三万","二万","一万",
            "九条","八条","七条","六条","五条","四条","三条","二条","一条",
            "九筒","八筒","七筒","六筒","五筒","四筒","三筒","二筒","一筒"]

def translate(a):
    tmp = 0
    for x in a:
        tmp = 5*tmp + int(x)
    return tmp
def search(pai):
    s = set()
    tmp = 1
    for i in range(27):
        sql = f"select 1 from hu where pai='{pai+tmp}'"
        
        cursor.execute(sql)
        result = cursor.fetchone()
        tmp=tmp*5
        if result==None:
            continue
        s.add(i)
    return s

def response(request):
    if request.POST:
        d = request.POST
        arr = [0]*27
        for x in d['tong']:
            arr[int(x)-1] += 1
        for x in d['tiao']:
            arr[int(x)+8] += 1
        for x in d['wan']:
            arr[int(x)+17] += 1
        
        if len(d['tong'])+len(d['tiao'])+len(d['wan']) == 13:
            s = list(search(translate(arr)))
            s.sort(reverse=True)
            if not s:
                return HttpResponse("不能听牌")
            response = ""
            for x in s:
                response += mapping[x]
            return HttpResponse("可以听"+response)
        elif len(d['tong'])+len(d['tiao'])+len(d['wan']) == 14:
            response = ""
            for i in range(len(arr)):
                if(arr[i]):
                    arr[i]-=1
                    s = list(search(translate(arr)))
                    s.sort(reverse=True)   
                    if s:
                        s = "".join(list(map(lambda i :mapping[i],s)))
                        response += "可以打"+mapping[-i-1]+",听"+s+"<br>"
                    arr[i]+=1
            if response:
                return HttpResponse(response)
            else:
                return HttpResponse("差得远")
        else:
            return HttpResponse("")
    return render(request,"index.html")