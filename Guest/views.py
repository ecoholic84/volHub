from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *
from User.models import *
# Create your views here.

def Index(request):
    return render(request, 'Guest/index2.html')

def userEmail(request):
    if request.method=='POST':
        email=request.POST.get('txt_email')
        if tbl_user.objects.filter(user_email=email).exists():
            message = "Email already exists!"
            return render(request, 'Guest/signUp.html',{'failed': message})
        else:
            user = tbl_user.objects.create(user_email=email)
            request.session['regId']=user.id
            message = "Email created successfully!"
            return render(request, 'Guest/signUp.html',{'success': message})
    else:
        return render(request, 'Guest/signUp.html',)

        

def userRegistration(request):
    city=tbl_city.objects.all()
    if request.method=="POST":
        user = tbl_user.objects.get(id=request.session.get('regId'))
        user.user_name=request.POST.get('txt_name')
        user.user_username=request.POST.get('txt_username')
        user.user_password=request.POST.get('txt_password')
        request.session['u_id']=user.id
        user.save()
        return redirect('Guest:userWho')
    else:
        return render(request,'Guest/userRegistration.html')
    

def userWho(request):
    if request.method=="POST":
        user = tbl_user.objects.get(id=request.session.get('regId'))
        selectedType = request.POST.get('user_type')
        user.user_type = selectedType
        request.session['u_id']=user.id
        user.save()
        return redirect('User:userDashboard')
    else: 
        return render(request, 'Guest/userType.html', {"message": "Please select a type"})


    



def ajaxPlace(request):
    place=tbl_place.objects.filter(district=request.GET.get("did"))
    return render(request,'Guest/ajaxPlace.html', {"place":place})

def login(request):
    if request.method=="POST":
        email=request.POST.get('txt_email')
        password=request.POST.get('txt_password')
        adminCount=tbl_admin.objects.filter(admin_email=email,admin_password=password).count()
        userCount=tbl_user.objects.filter(user_email=email,user_password=password).count()
        if userCount > 0:
            user=tbl_user.objects.get(user_email=email,user_password=password)
            request.session['u_id']=user.id
            return redirect('User:userDashboard')
        elif adminCount > 0:
            admin=tbl_admin.objects.get(admin_email=email,admin_password=password)
            request.session['a_id']=admin.id
            return redirect('Admin:adminDashboard')
        else:
            return render(request,'Guest/login.html',{'msg':"invalid login"})
    else:
        return render(request,'Guest/login.html')
    