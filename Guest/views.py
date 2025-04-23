from django.shortcuts import render, redirect
from Admin.models import *
from Guest.models import *
from User.models import *
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


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
        request.session['name'] = user.user_name or ''
        request.session['username'] = user.user_username or ''
        # Set gender and profile photo URL in session if available
        request.session['gender'] = getattr(user, 'user_gender', '')
        if getattr(user, 'user_photo', None):
            request.session['profile_photo_url'] = user.user_photo.url if user.user_photo else ''
        else:
            request.session['profile_photo_url'] = ''
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
        if not user.is_basic_profile_complete:
            return redirect('User:create_profile')
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
            # Set gender and profile photo URL in session if available
            request.session['gender'] = getattr(user, 'user_gender', '')
            if getattr(user, 'user_photo', None):
                request.session['profile_photo_url'] = user.user_photo.url if user.user_photo else ''
            else:
                request.session['profile_photo_url'] = ''
            redirect_url = (
                'User:volunteer_dashboard' if user.user_type == "volunteer"
                else 'User:organizer_dashboard' if user.user_type == "organizer"
                else 'User:volunteer_dashboard' if user.user_type == "both"
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

def public_profile(request, name):
    # Show public profile for organizer or volunteer
    try:
        user = tbl_user.objects.get(user_username=name)
        # Volunteer Journey: events where user volunteered (accepted requests)
        volunteer_events = tbl_event.objects.filter(requests__user=user, requests__request_status=1).distinct()
        # Organizer Journey: events organized by this user
        organized_events = tbl_event.objects.filter(user=user)
        if (user.user_type == 'organizer' or user.user_type == 'volunteer') and user.user_visibility:
            return render(request, "Guest/public_profile.html", {
                "user": user,
                "volunteer_events": volunteer_events,
                "organized_events": organized_events
            })
        elif user.user_type != 'organizer':
            return render(request, "Guest/public_profile.html", {"user": user})
        else:
            return render(request, "Guest/public_profile.html", {"user": ''})
    except tbl_user.DoesNotExist:
        return render(request, "Guest/public_profile.html", {"user": ''})
    
def forgotpassword(request):
    if request.method == "POST":
        email = request.POST.get("txt_email")
        user = tbl_user.objects.get(user_email=email)
        otp = random.randint(111111,999999)
        request.session["otp"] = otp
        request.session["fid"] = user.id
        send_mail(
            'Forgot password OTP', #subject
            "\rHello \r" + str(otp) +"\n This is the OTP to reset ur password.\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n ",#body
            settings.EMAIL_HOST_USER,
            [email],
        )
        return render(request,"Guest/ForgotPassword.html",{"msg":email})
    else:
        return render(request,"Guest/ForgotPassword.html")

def otp(request):
    if request.method == "POST":
        inp_otp = int(request.POST.get("txt_otp"))
        if inp_otp == request.session["otp"]:
            return redirect("Guest:newpass")
        else:
            return render(request,"Guest/OTP.html",{"msg":"OTP Does not Matches..!!"})
    else:
        return render(request,"Guest/OTP.html")

def newpass(request):
    if request.method == "POST":
        user = tbl_user.objects.get(id=request.session["fid"])
        if request.POST.get("txt_new_pass") == request.POST.get("txt_con_pass"):
            user.user_password = request.POST.get("txt_con_pass")
            user.save()
            return render(request,"Guest/NewPassword.html",{"msg1":"Password Updated Sucessfully...."})
        else:
            return render(request,"Guest/NewPassword.html",{"msg":"Error in confirm password..!!!"})
    else:
        return render(request,"Guest/NewPassword.html")

def public_event_detail(request, event_id):
    try:
        event = tbl_event.objects.get(id=event_id, visibility=1, event_status=1)
        return render(request, 'Guest/public_event_detail.html', {'event': event})
    except tbl_event.DoesNotExist:
        return render(request, 'Guest/public_event_detail.html', {'event': None})
