from django.http import HttpResponse
from django.shortcuts import render
import pymysql
db = pymysql.connect(host="localhost",user="lisu",password="Ls3314188",database="mahjong")
cursor = db.cursor()

def translate(a):
    tmp = 0
    for x in a:
        tmp = 5*tmp + int(x)
    return tmp
def search_(pai):
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
    

def search(request):
    ctx = {}
    ctx["x"] = [3,1,1,1,1,1,1,1,3] + 18*[0]
    if request.POST:
        arr = request.POST.getlist("q",[])
        pai = translate(arr)
        ctx["result"] = str(search_(pai))
        ctx["x"] = arr 
    return render(request,"index.html",ctx)