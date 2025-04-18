from django.shortcuts import render, redirect
from Admin.models import *
from Guest.models import *
from User.models import *

def index(request):
    return render(request, 'Guest/index.html')

def get_email(request):
    if request.method == 'POST':
        email = request.POST.get('txt_email')
        if not email:
            return render(request, 'Guest/sign_up.html', {'failed': 'Email is required!'})
        if tbl_user.objects.filter(user_email=email).exists():
            return render(request, 'Guest/sign_up.html', {'failed': 'Email already exists!'})
        request.session['temp_email'] = email
        return redirect('Guest:user_registration')
    return render(request, 'Guest/sign_up.html')

def user_registration(request):
    if request.method == "POST":
        email = request.session.get('temp_email')
        if not email:
            return redirect('Guest:sign_up')
        if tbl_user.objects.filter(user_email=email).exists():
            return render(request, 'Guest/sign_up.html', {'failed': 'Email already registered!'})
        user = tbl_user.objects.create(
            user_email=email,
            user_name=request.POST.get('txt_name'),
            user_username=request.POST.get('txt_username'),
            user_password=request.POST.get('txt_password')
        )
        request.session['u_id'] = user.id
        del request.session['temp_email']
        return redirect('Guest:user_who')
    return render(request, 'Guest/user_registration.html')

def user_who(request):
    if request.method == "POST":
        user_id = request.session.get('u_id')
        if not user_id:
            return redirect('Guest:sign_up')
        user = tbl_user.objects.get(id=user_id)
        selectedType = request.POST.get('user_type')
        user.user_type = selectedType
        user.save()
        if selectedType == "volunteer":
            return redirect('User:volunteer_dashboard')
        elif selectedType == "organizer":
            return redirect('User:organizer_dashboard')
        return render(request, 'Guest/user_type.html', {"message": "Invalid user type selected. Please try again."})
    return render(request, 'Guest/user_type.html', {"message": "Please select a type"})

def ajax_place(request):
    place = tbl_place.objects.filter(district=request.GET.get("did"))
    return render(request, 'Guest/ajax_place.html', {"place": place})

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        admin_count = tbl_admin.objects.filter(admin_email=email, admin_password=password).count()
        user_count = tbl_user.objects.filter(user_email=email, user_password=password).count()
        if user_count > 0:
            user = tbl_user.objects.get(user_email=email, user_password=password)
            request.session['u_id'] = user.id
            request.session["username"] = user.user_username
            redirect_url = (
                'User:volunteer_dashboard' if user.user_type == "volunteer"
                else 'User:organizer_dashboard' if user.user_type == "organizer"
                else 'Guest:user_who'
            )
            return redirect(redirect_url)
        elif admin_count > 0:
            admin = tbl_admin.objects.get(admin_email=email, admin_password=password)
            request.session['a_id'] = admin.id
            request.session["username"] = admin.admin_name
            return redirect('Admin:adminDashboard')
        return render(request, 'Guest/login.html', {'msg': "Invalid login"})
    return render(request, 'Guest/login.html')

def profile(request, name):
    user_count = tbl_user.objects.filter(user_username=name,user_visibility=1).count()
    if user_count > 0:
        user = tbl_user.objects.get(user_username=name)
        return render(request,"Guest/Profile.html",{"user":user})
    else:
        return render(request,"Guest/Profile.html",{"user":''})
