from django.http import HttpResponse
import os
from pathlib import Path as controlpath
import datetime
import subprocess
import tempfile
import math 
from collections import deque
import sqlite3
from datetime import datetime
import time
from django.views.generic import ListView
import glob
from django.shortcuts import render, redirect
from numpy.core.fromnumeric import size
from numpy.lib.type_check import imag
from .forms import *
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.conf import settings
import json  
def sagar(request):
    return render(request,"polls/sagar.html")
def loginPage(request):
    try: 
        if request.method =='POST':
            username=request.POST.get('username') 
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None: 
                login(request,user)
                if username[-1].lower()=="t":
                    return redirect(teacher)
                return redirect(student)

            else:
                messages.info(request, 'Username or password incorrect')
        context={}
        return render(request,'registration/login.html',context)
    except:
        return HttpResponse("404 network error")
def register(request):
    try:
        if request.method=='POST': 
            form=CustomUserCreationForm(request.POST)
            if form.is_valid():
                username=form.cleaned_data['username']
                password=form.cleaned_data['password1']
                if username.lower()[-1] !="s" and username.lower()[-1] !="t":
                    form =CustomUserCreationForm() 
                    context={"form":form,"wrong":"please use below format"}
                    return render(request,'registration/register.html',context)
                if username[-1].lower()=="s":
                    puser=username.lower() 
                    work=len(username.lower())
                    target=0
                    std=""
                    name=""
                    number=""
                    
                    for i in range(work):
                        if puser[i]=="/":
                            target=i
                            break
                        name=name+puser[i]
                    for i in range(target+1,work):
                        if puser[i]=="/":
                            target=i
                            break    
                        number=number+puser[i]
                    for i in range(target+1,work):
                        if puser[i]=="/":
                            target=i
                            break
                        std=std+puser[i]
                    if puser.count("/")!=3 or len(number)!=10 or int(std)<9 or int(std)>12 :
                        form =CustomUserCreationForm() 
                        context={"form":form,"wrong":"please use above format"}
                        return render(request,'registration/register.html',context) 
                    form.save()
                    user=authenticate(username=username,password=password)
                    redirect(student)
                if username[-1].lower()=="s":
                    puser=username[-1].lower()
                    work=len(username[-1].lower())
                    target=0
                    std=""
                    name=""
                    number=""
                    for i in range(work):
                        if puser[i]=="/":
                            target=i
                            break
                        name=name+puser[i]
                    for i in range(target+1,work):
                        if puser[i]=="/":
                            target=i
                            break
                        number=number+puser[i]
                    if puser.count("/")!=2 or len(number)!=10  :
                        form =CustomUserCreationForm() 
                        context={"form":form,"wrong":"please use above format"}
                        return render(request,'registration/register.html',context)
                
                user=authenticate(username=username,password=password)
                login(request,user)    
                form.save()
                return render(request,'polls/teacher.html')
        else:
            form =CustomUserCreationForm() 
        context={"form":form}
        return render(request,'registration/register.html',context)
    except:
        return HttpResponse("404 network error")
def teacher(request):
    try:
        path = settings.MEDIA_ROOT
        x=str(request.user.username)
        hook=os.listdir(path+"/doto/")    
        form = Hotel()
        if "monk1.json" in hook:
            with open(path+"/doto/monk1.json") as fz: 
                temp1=json.load(fz)
            with open(path+"/doto/monk.json") as fz: 
                temp=json.load(fz)
            if "monk" in str(request.POST):
                for i in temp[request.POST['monk']]['questions']:
                    os.remove(path+i.replace("media",""))
                temp.pop(request.POST['monk'])
                temp1[x].remove(request.POST['monk'])
                with open(path+"/doto/monk.json","w") as fz: 
                    json.dump(temp,fz,indent=4)
                with open(path+"/doto/monk1.json","w") as fz: 
                    json.dump(temp1,fz,indent=4)
            path=temp1[x]
        else:
            path=[]
        return render(request, 'polls/teacher.html', {'form' : form,'path':path})
    except:
        return HttpResponse("Hello, world. You're at the polls index.")
def test(request):
    try:
        path = settings.MEDIA_ROOT
        x=str(request.user.username)
        rusertest=str(request.POST['testpo'])
        with open(path+"/doto/monk.json") as fz:
            temp=json.load(fz)
        zx=[]
        return render(request,"polls/test.html",{"zx":[temp[rusertest]["questions"]],"rusertest":rusertest})
    except:
        return HttpResponse("404 network error")
def setup(request):
    try:
        path = settings.MEDIA_ROOT
        x=str(request.user.username)
        if request.method == 'POST':
            myfile = request.FILES.getlist("uploadfoles")
            fast=os.listdir(path+"/images/")
            arr={i:1 for i in fast}
            for f in myfile:
                working=Hotel(chooseIMG=f)
                working.save()
            arr1=os.listdir(path+"/images/")
            send=[]
            for i in arr1: 
                if i not in arr:
                    send.append("media/images/"+i)
            if len(send)==0:
                return render(request, 'polls/setup.html',{"send":send})
            path=settings.MEDIA_ROOT
            hook=os.listdir(path+"/doto/")
            if "monk1.json" in hook:
                with open(path+"/doto/monk1.json") as fz:
                    temp1=json.load(fz)
                if x not in temp1:
                    temp1[x]=[]
            else:
                temp1={}
                temp1[x]=[]
            if "monk.json" in hook:
                with open(path+"/doto/monk.json") as fz:
                    temp=json.load(fz)
                
                if len(temp)==0:
                    temp["test0"]={"questions":{i:0 for i in send}}
                    temp1[x].append("test0")
                else:
                    rselect=max(temp).replace("test","")
                    temp["test"+str(int(rselect)+1)]={"questions":{i:0 for i in send}}
                    temp1[x].append("test"+str(int(rselect)+1))
                with open(path+"/doto/monk.json","w") as fz:
                    json.dump(temp,fz,indent=4)
                with open(path+"/doto/monk1.json","w") as fz:
                    json.dump(temp1,fz,indent=4)
            else:
                temp={}
                temp["test0"]={"questions":{i:0 for i in send}}
                temp1[x].append("test0")
                with open(path+"/doto/monk.json","w") as fz:
                    json.dump(temp,fz,indent=4)
                with open(path+"/doto/monk1.json","w") as fz:
                    json.dump(temp1,fz,indent=4)
        return render(request, 'polls/setup.html',{"send":send})
    except:
        return HttpResponse("404 netwok error")
def select(request):
    try:
        if "str" not in str(request.POST) or "duration" not in str(request.POST):
                while(True):
                    if "str" not in str(request.POST) or "duration" not in str(request.POST):
                        break
        path=settings.MEDIA_ROOT
        with open(path+"/doto/monk.json") as fz:
            temp=json.load(fz)
        test=""
        check=os.listdir(path+"/images/")
        monkfast={i:1 for i in check}
        for i in temp:
            for j in temp[i]["questions"]:
                if 0 == temp[i]["questions"][j]:
                    test=i
                if j.replace("media/images/","") in monkfast:
                    monkfast.pop(j.replace("media/images/",""))
        for i in monkfast:
            if os.path.isfile(path+"/images/"+i):
                os.remove(path+"/images/"+i)
        try:
            for j in temp[test]["questions"]:
                temp[test]["questions"][j]=str(request.POST[j])
            temp[test]["duration"]=request.POST['duration']
            temp[test]["std"]=request.POST['std']
            temp[test]["meeting-time"]=request.POST['meeting-time']
            with open(path+"/doto/monk.json","w") as fz:
                json.dump(temp,fz,indent=4) 
            
            return redirect(teacher) 
        except:
            return redirect(teacher)
    except:
        return HttpResponse("Hello, world. You're at the polls index.")
def student(request): 
    path=settings.MEDIA_ROOT
    x1=str(request.user.username).split("/")
    path=settings.MEDIA_ROOT
    name=x1[0] 
    number=x1[1]
    std=x1[2]
    check=os.listdir(path+"/doto/")
    rf={}
    if "monk.json" in check:
        with open(path+"/doto/monk.json") as fz:
            temp=json.load(fz)
        for i in temp:
            if "monk2.json" in check:
                with open(path+"/doto/monk2.json") as fz:
                    temp2=json.load(fz)
                if str(request.user.username) in temp2:
                    if i not in temp2[str(request.user.username)]:
                        if temp[i]['std']==std:
                            fg=temp[i]["meeting-time"].split("T")
                            rf[i]=fg[0]+" "+fg[1]
                else:
                    if temp[i]['std']==std:
                        fg=temp[i]["meeting-time"].split("T")
                        rf[i]=fg[0]+" "+fg[1]
            else:
                    if temp[i]['std']==std:
                        fg=temp[i]["meeting-time"].split("T")
                        rf[i]=fg[0]+" "+fg[1]
    address=name.upper()
    return render(request,"polls/student.html",{"rf":[rf],"address":address,"number":number,"std":std}) 
def originaltest(request):
    try:
        x1=str(request.user.username).split("/")
        path=settings.MEDIA_ROOT
        with open(path+"/doto/monk.json") as fz:
            temp=json.load(fz)
        time1=temp[request.POST['yomonk']]["meeting-time"].split("T")
        l=str(datetime.now())
        l=l.split(" ")[1]
        l=l.split(":")
        l=l[0]+":"+l[1]
        song=time1[1].split(":")
        if time1[1][0]=="0":
            song=str((int(song[0][1])+int(temp[request.POST['yomonk']]["duration"]))%24)+":"+song[1]
        else:
            song=str((int(song[0])+int(temp[request.POST['yomonk']]["duration"]))%24)+":"+song[1]
        if time1[0]<=datetime.today().strftime('%Y-%m-%d') and time1[1]<=l and  l<song:
            check=os.listdir(path+"/doto/") 
            if "monk2.json" in check :
                with open(path+"/doto/monk2.json") as fz:
                    temp2=json.load(fz)
                if str(request.user.username) in temp2:
                    for i in temp2[str(request.user.username)]:
                        wgi=i[1].split(" ")
                        if time1[0]==wgi[0] and time1[1]<=wgi[1] and  wgi[1]<song:

                            return redirect(aftertest)
            song=song.split(":")
            f=time1[0].split("-")
            if f[1][0]=="0":
                f[1]=f[1].replace("0","",1)
            if f[2][0]=="0":
                f[2]=f[2].replace("0","",1)
            if song[1][0]=="0":
                song1[1]=song[1].replace("0","",1)
            a=datetime(int(f[0]),int(f[1]),int(f[2]),int(song[0]),int(song[1]))
            b=datetime.now()
            c=a-b
            return render(request,"polls/originaltest.html",{"question":temp[request.POST['yomonk']]["questions"],"test":request.POST['yomonk'],"song":int(c.seconds)})
        return redirect(aftertest)
    except:
        return redirect(aftertest)
def aftertest(request): 
    try:         
        if "long" in request.POST:
            path=settings.MEDIA_ROOT
            with open(path+"/doto/monk.json") as fz:
                temp=json.load(fz)
            t=0
            for i in temp[request.POST['long']]["questions"]:
                if temp[request.POST['long']]["questions"][i]==str(request.POST[i]):
                    t=t+1
            time1=temp[request.POST['long']]["meeting-time"].split("T")
            l=str(datetime.now())
            l=l.split(" ")[1]
            l=l.split(":")
            l=l[0]+":"+l[1]
            song=time1[1].split(":")
            if time1[1][0]=="0":
                song=str((int(song[0][1])+int(temp[request.POST['long']]["duration"]))%24)+":"+song[1]
            else:
                song=str((int(song[0])+int(temp[request.POST['long']]["duration"]))%24)+":"+song[1]
            workload=temp[request.POST['long']]["questions"]
            check=os.listdir(path+"/doto/")
            if "monk2.json" in check :
                with open(path+"/doto/monk2.json") as fz:
                    temp2=json.load(fz)
                if str(request.user.username) in temp2:
                    for i in temp2[str(request.user.username)]:
                        wgi=i[1].split(" ")
                        if time1[0]<wgi[0]:
                            0/0
                        if time1[0]==wgi[0] and wgi[1]>song:
                            0/0
                        if time1[0]==wgi[0] and time1[1]<=wgi[1] and  wgi[1]<song:
                            0/0
                if str(request.user.username) in temp2:
                    temp2[str(request.user.username)].append([str((t/len(workload))*100),str(datetime.now())[:-10]])
                else:
                    temp2[str(request.user.username)]=[[str((t/len(workload))*100),str(datetime.now())[:-10]]]
                with open(path+"/doto/monk2.json","w") as fz:
                    json.dump(temp2,fz,indent=4)
            else:
                temp2={}
                temp2[str(request.user.username)]=[[str((t/len(workload))*100),str(datetime.now())[:-10]]]
                with open(path+"/doto/monk2.json","w") as fz:
                    json.dump(temp2,fz,indent=4)
        with open(path+"/doto/monk2.json") as fz:
                temp2=json.load(fz)
        with open(path+"/doto/monk.json","w") as fz:
                json.dump(temp,fz,indent=4)
        return render(request,"polls/aftertest.html",{"score":temp2[str(request.user.username)]})
    except:
        p=[]
        temp2={}
        path=settings.MEDIA_ROOT
        check=os.listdir(path+"/doto/")
        if "monk2.json" in check :
            with open(path+"/doto/monk2.json") as fz:
                temp2=json.load(fz)
        if str(request.user.username) not in temp2:
            temp2[str(request.user.username)]=[]

        return render(request,"polls/aftertest.html",{"score":temp2[str(request.user.username)]})
