from django.shortcuts import render, redirect
from Guest.models import *
from User.models import *

# Create your views here.
def userDashboard(request):
    return render(request,'User/userDashboard.html')

def myProfile(request):
    thisProfile=tbl_user.objects.get(id=request.session['u_id'])
    return render(request,'User/myProfile.html', {'thisProfile':thisProfile})

def editProfile(request):
    editProfile=tbl_user.objects.get(id=request.session['u_id'])
    if request.method=="POST":
        editProfile.user_name=request.POST.get('txt_name')
        editProfile.user_email=request.POST.get('txt_email')
        editProfile.user_contact=request.POST.get('txt_contact')
        editProfile.user_address=request.POST.get('txt_address')
        editProfile.save()
        return redirect('User:myProfile')
    else:
        return render(request, 'User/editProfile.html', {'editProfile':editProfile})

def changePassword(request):
    loggedUser=tbl_user.objects.get(id=request.session['u_id'])
    if request.method=="POST":
        oldPassword=request.POST.get('txt_old_password')
        newPassword=request.POST.get('txt_new_password')
        confirmPassword=request.POST.get('txt_confirm_password')
        if loggedUser.user_password==oldPassword:
            if newPassword==confirmPassword:
                loggedUser.user_password=newPassword
                loggedUser.save()
            else:
                return redirect('User:myProfile')
        else:
            return redirect('User:myProfile')
    return render(request, 'User/changePassword.html')

# Feedback
def Feedback(request):
    fb=tbl_feedback.objects.all()
    if request.method=="POST":
        content=request.POST.get("txt_feedback")
        tbl_feedback.objects.create(feedback_content=content,user_id=tbl_user.objects.get(id=request.session['u_id']))
        return redirect('User:feedback')
    else:
        return render(request,'User/feedback.html',{'feed':fb})
        
def deleteFeedback(request,did):
    tbl_feedback.objects.get(id=did).delete()
    return redirect('User:feedback')

# Complaint
def Complaint(request):
    cp=tbl_complaint.objects.all()
    if request.method=="POST":
        complaintTitle=request.POST.get("txt_complaint_title")
        complaintContent=request.POST.get("txt_complaint_content")
        tbl_complaint.objects.create(complaint_title=complaintTitle,complaint_content=complaintContent,user_id=tbl_user.objects.get(id=request.session['u_id']))
        return redirect('User:complaint')
    else:
        return render(request,'User/complaint.html', {'comp':cp})
    
def deleteComplaint(request,did):
    tbl_complaint.objects.get(id=did).delete()
    return redirect('User:complaint')

def editComplaint(request,eid):
    thisComplaint=tbl_complaint.objects.get(id=eid)
    if request.method=="POST":
        thisComplaint.complaint_title=request.POST.get('txt_complaint_title')
        thisComplaint.complaint_content=request.POST.get('txt_complaint_content')
        thisComplaint.save()
        return redirect('User:complaint') #complaint here is the url which we have defined in urls.py, Django looks for a URL pattern name that matches 'User/complaint' in your urls.py file.
    else:
        return render(request,'User/complaint.html', {"editComplaint":thisComplaint})
    

# Profile Creation
def create_profile(request):
    country = tbl_country.objects.all()
    state = tbl_state.objects.all()
    thisUser = tbl_user.objects.get(id=request.session['u_id'])
    if request.method=="POST":
        print("POST data:", request.POST)  # Debug line
        thisUser.user_name=request.POST.get('txt_name')
        thisUser.user_username=request.POST.get('txt_username')
        thisUser.user_email=request.POST.get('txt_email')
        thisUser.user_gender=request.POST.get('txt_gender')
        thisUser.user_city=tbl_city.objects.get(id=request.POST.get('sel_city'))
        thisUser.user_bio=request.POST.get('txt_bio')
        thisUser.save()
        return redirect('User:create_profile')
    else:
        return render(request, 'User/create_profile.html', {'country':country, 'state':state})
    
def profile_country_ajax(request):
    state=tbl_state.objects.filter(country=request.GET.get("did"))
    return render(request,'User/profile_country_ajax.html', {"state":state})
    
def profile_state_ajax(request):
    city=tbl_city.objects.filter(state=request.GET.get("did"))
    return render(request,'User/profile_state_ajax.html', {"city":city})