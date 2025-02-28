from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *
from User.models import *
# Create your views here.
def userRegistration(request):
    dis=tbl_district.objects.all()
    if request.method=="POST":
        tbl_user.objects.create(user_name=request.POST.get('txt_name'), user_email=request.POST.get('txt_email'),user_contact=request.POST.get('txt_contact'),user_address=request.POST.get('txt_address'),user_password=request.POST.get('txt_password'), place=tbl_place.objects.get(id=request.POST.get('sel_place')), user_photo=request.FILES.get('txt_photo'))
    return render(request,'Guest/userRegistration.html', {"district":dis})

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