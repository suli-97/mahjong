import os
x = os.popen("sudo netstat -atunp | grep 0.0.0.0:80").read()
end = x.find('/python')
i = end-1
while '0' <= x[i] <= '9':
    i-=1
i+=1
os.system("sudo kill "+x[i:end])
os.system("sudo nohup python3 manage.py runserver 0.0.0.0:80 &")
