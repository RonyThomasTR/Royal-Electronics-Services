from django.shortcuts import render, redirect, get_object_or_404
from .forms import User_detail
from django.http import HttpResponse
from myapp.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from myapp.models import Appointment,Estimation
from operator import attrgetter



# Create your views here.


def myview(request):
    return render(request,'index.html')


def signin(request):
    if request.method == 'POST':
        usrn= request.POST.get('usrname')
        eml = request.POST.get('emil')
        phn = request.POST.get('ph_no')
        pss = request.POST.get('psword')
        pssc = request.POST.get('psword_confirmation')
        if pss==pssc:
            User.objects.create_user(username=usrn,phone=phn,email= eml,password=pss,usertype=3)
            usr=authenticate(request,username=usrn,password=pss)
            if usr is not None :
                request.session['cid']=usr.id
                login(request,usr)
                messages.add_message(request, messages.SUCCESS,'Account created, please login to your profile')
                return render(request,'user.html')
            else:
                return HttpResponse('error')
        else:
            messages.add_message(request, messages.SUCCESS,'Password Does Not Match.')
            return render(request,'signin.html')
    else:
        return render(request,'signin.html') 


def logins(request):
    if request.method=="POST":
        lusr=request.POST['usernm']
        lpss=request.POST['passwords']
        luser = authenticate(request,username=lusr,password=lpss)

        if luser is not None and luser.usertype == 3:
            request.session['cid']=luser.id 
            login(request,luser)
            return render(request,'aftersignin.html',{'data':luser})
        
        elif luser is not None and luser.usertype==2:
           request.session['sid']=luser.id
           login(request,luser)
           return render(request,'staffview.html',{'data':luser})
        
        elif luser is not None and luser.usertype==1:
           request.session['aid']=luser.id
           login(request,luser)
           return render(request,'adminview.html')
        else:
            data={'usr':luser}
            messages.add_message(request,messages.SUCCESS,'Incorrect Login Credentials')
            return render(request,'login.html',{'data':data})
    else:    
        return render(request,"login.html")

 
@login_required

def appointment(request):
    if request.method=="POST":
        dev=request.POST.get('device')
        brnd=request.POST.get('brand')
        rad=request.POST.get('flexRadio')
        des=request.POST.get('desc')
        fil=request.POST.get('filef')
        us=request.session['cid']
        appoint=Appointment(device=dev,brand=brnd,option=rad,description=des,file=fil,uid=us)
        appoint.save()
        if appoint is not None:
            messages.add_message(request,messages.SUCCESS,'Appointment done sucessfully')
            return render(request,'aftersignin.html')
        else:
             data={'usr':appoint}
             return render(request,'login.html',{'data':data})
    else:
        return render(request,'appointment.html')    


def profile(request):
    id=request.session['cid']
    if id is not None:
        data =User.objects.filter(id=id) 
        return render(request,'profile.html', {'data': data})
    else:
        return HttpResponse('user id not found')
    

def add_staff(request):
    if request.method == 'POST':
        usrn= request.POST.get('usrname')
        eml = request.POST.get('emil')
        phn = request.POST.get('ph_no')
        usrtp=request.POST.get('usrtype')
        pss = request.POST.get('psword')
        User.objects.create_user(username=usrn,phone=phn,email= eml,password=pss,usertype=usrtp)
        usr=authenticate(request,username=usrn,password=pss)
        if usr is not None:
            messages.add_message(request,messages.SUCCESS,'Staff added sucessfully')
            return render(request,'admin.html')        
        else:
            return HttpResponse('Staff authentication failed')
    else:
        return render(request,'admin.html') 
    

def vwdetails(request):
    users=User.objects.filter(usertype=3).all()
    appoin=Appointment.objects.all()
    appoin_sorted = sorted(appoin, key=attrgetter('id'))
    return render(request,'detail.html',{'usr':users,'appo':appoin_sorted})


def logouts(request):
    logout(request)
    messages.add_message(request,messages.SUCCESS,'You are logged out from your profile,please login agian')
    return render(request,'user.html')

    
def editprofile(request):
    id=request.session['cid']
    if request.method =='POST':
        usrnm=request.POST['us']
        phno=request.POST['ph']
        eml=request.POST['em']
        User.objects.filter(id=id).update(username=usrnm,phone=phno,email=eml)
        data=User.objects.get(id=id)
        messages.add_message(request,messages.SUCCESS,'Profile edited SUCCESFULLY')
        return render(request,'editprofile.html',{'data':data})
    else:
        data=User.objects.filter(id=id).get()
        return render(request,'editprofile.html',{'data':data})
    

def userapointvw(request):
    id=request.session['cid']
    appo=Appointment.objects.filter(uid=id)
    if appo:
        return render(request,'userappointvw.html',{'app':appo})
    else:
        messages.add_message(request,messages.SUCCESS,'You have not made any appointment')
        return render(request,'userappointvw.html')


def delaccount(request):
    id=request.session['cid']
    user=User.objects.filter(id=id).get()
    Appointment.objects.filter(uid=id).delete()
    user.delete()
    messages.add_message(request, messages.SUCCESS,'Your account has deleted')
    return render(request,'user.html')


def home(request):
    return render(request,'aftersignin.html')


def back(request):
    return render(request,'profile.html')


def usrhm(request):
    return render(request,'user.html')


def sthm(request):
    return render(request,'staffview.html')


def adhm(request):
    return render(request,'adminview.html')


def vwstf(request):
        users=User.objects.filter(usertype=2).all()
        return render(request,'viewstaff.html',{'usr':users})


def accept(request, id):
    if id is not None:
        Appointment.objects.filter(id=id).update(appointment_progress=1)
        return redirect('/vwdet/')
    else:
        return HttpResponse('Appointment detailing failed')
    

def backappoint_view(request):
    return redirect('/appo/')
    

def estimation(request, id):
    if id is not None:
        Appointment.objects.filter(id=id).update(appointment_progress=2)
        return redirect('/vwdet/')
    else:
        return HttpResponse('Appointment detailing failed')
    

def waitforconfirm(request, id):
    if id is not None:
        Appointment.objects.filter(id=id).update(appointment_progress=3)
        return redirect('/appo/')
    else:
        return HttpResponse('Appointment detailing failed')

    

def onprogress(request, id):
    if id is not None:
        Appointment.objects.filter(id=id).update(appointment_progress=4)
        return redirect('/vwdet/')
    else:
        return HttpResponse('Appointment detailing failed')
    

def onprogress(request, id):
    if id is not None:
        Appointment.objects.filter(id=id).update(appointment_progress=5)
        return redirect('/vwdet/')
    else:
        return HttpResponse('Appointment detailing failed')
    


def reject(request, id):
    if id is not None:
        Appointment.objects.filter(id=id).update(appointment_progress=9)
        return redirect('/vwdet/')
    else:
        return HttpResponse('Appointment detailing failed') 


def rejection(request, id):
    if id is not None:
        Appointment.objects.filter(id=id).update(appointment_progress=10)
        return redirect('/appo/')
    else:
        return HttpResponse('Appointment detailing failed')


def delacount(request, id):
    user = User.objects.filter(id=id).get()
    user.delete()
    return redirect('/vst/')



def estimation_page(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    return render(request, 'estimationstaff.html',{'appoint': appointment})



def make_estimation(request, appointment_id):
    if request.method == 'POST':
        observation = request.POST.get('observ')
        remarks = request.POST.get('remark')
        delivery_date = request.POST.get('ddate')
        price = request.POST.get('eprice')
        appointment = Appointment.objects.get(id=appointment_id)
        estimation = Estimation.objects.create(observation=observation,remarks=remarks,deliverydate=delivery_date,price=price,eid=appointment.id)
        appointment.appointment_progress = 2
        appointment.save()      
        return redirect('/det/')      
    return render(request, 'estimationstaff.html')




def view_estimation(request, id):
    if id is not None: 
        estm =Estimation.objects.get(eid= id)
        return render(request,'estimationuser.html', {'data': estm})
    else:
        return HttpResponse('Appointment detailing failed')
 
