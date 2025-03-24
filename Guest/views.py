from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *
from User.models import *
# Create your views here.

def index(request):
    return render(request, 'Guest/index.html')

def get_email(request):
    if request.method=='POST':
        email=request.POST.get('txt_email')
        if tbl_user.objects.filter(user_email=email).exists():
            message = "Email already exists!"
            return render(request, 'Guest/sign_up.html',{'failed': message})
        else:
            user = tbl_user.objects.create(user_email=email)
            request.session['regId']=user.id
            message = "Email created successfully!"
            return render(request, 'Guest/sign_up.html',{'success': message})
    else:
        return render(request, 'Guest/sign_up.html',)

        

def user_registration(request):
    city=tbl_city.objects.all()
    if request.method=="POST":
        user = tbl_user.objects.get(id=request.session.get('regId'))
        user.user_name=request.POST.get('txt_name')
        user.user_username=request.POST.get('txt_username')
        user.user_password=request.POST.get('txt_password')
        request.session['u_id']=user.id
        user.save()
        return redirect('Guest:user_who')
    else:
        return render(request,'Guest/user_registration.html')
    

# User Type Selection
def user_who(request):
    if request.method == "POST":
        user = tbl_user.objects.get(id=request.session.get('regId'))
        selectedType = request.POST.get('user_type')
        user.user_type = selectedType
        request.session['u_id'] = user.id
        user.save()
        if selectedType == "volunteer":
            return redirect('User:volunteer_dashboard')
        elif selectedType == "organizer":
            return redirect('User:organizer_dashboard')
        else:
            return redirect('User:user_dashboard')  # Fallback to generic dashboard
    else:
        return render(request, 'Guest/user_type.html', {"message": "Please select a type"})


def ajax_place(request):
    place=tbl_place.objects.filter(district=request.GET.get("did"))
    return render(request,'Guest/ajax_place.html', {"place":place})

# Guest/views.py (assuming this is where login resides)
from django.shortcuts import render, redirect
from Admin.models import tbl_admin
from Guest.models import tbl_user

def login(request):
    if request.method == "POST":
        email = request.POST.get('txt_email')
        password = request.POST.get('txt_password')
        adminCount = tbl_admin.objects.filter(admin_email=email, admin_password=password).count()
        userCount = tbl_user.objects.filter(user_email=email, user_password=password).count()
        
        if userCount > 0:
            user = tbl_user.objects.get(user_email=email, user_password=password)
            request.session['u_id'] = user.id
            if user.user_type == "volunteer":
                return redirect('User:volunteer_dashboard')
            elif user.user_type == "organizer":
                return redirect('User:organizer_dashboard')
            else:
                return redirect('Guest:user_who')  # Redirect to user-type selection if no valid user_type
        elif adminCount > 0:
            admin = tbl_admin.objects.get(admin_email=email, admin_password=password)
            request.session['a_id'] = admin.id
            return redirect('Admin:adminDashboard')
        else:
            return render(request, 'Guest/login.html', {'msg': "Invalid login"})
    else:
        return render(request, 'Guest/login.html')