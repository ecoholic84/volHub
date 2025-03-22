from django.shortcuts import render, redirect
from Guest.models import *
from User.models import *

# Create your views here.
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

def Event(request):
    country=tbl_country.objects.all()
    industry=tbl_industry.objects.all()
    user=tbl_user.objects.get(id=request.session['u_id'])
    if request.method=="POST":
        title=request.POST.get("txt_title")
        description=request.POST.get("txt_description")
        file=request.FILES.get("txt_file")
        industry=tbl_industry.objects.get(id=request.POST.get('sel_industry'))
        venue=request.POST.get("txt_venue")
        date_time=request.POST.get('txt_datetime')
        country=tbl_country.objects.get(id=request.POST.get('sel_country'))
        city=tbl_city.objects.get(id=request.POST.get('sel_city'))
        stipend=request.POST.get('txt_stipend')
        tbl_event.objects.create(event_title=title,event_content=description,event_file=file,industry=industry,event_venue=venue,event_datetime=date_time,event_city=city,event_stipend=stipend,user=user)
        return redirect("User:Event")
    else:
        return render(request,'User/event.html',{'country':country,'industry':industry})

# Volunteer dashboard redirection and listing
def volunteer_dashboard(request):
    if 'u_id' not in request.session:
        return redirect('Guest:login')
    user = tbl_user.objects.get(id=request.session['u_id'])
    if user.user_type != "volunteer":
        return redirect('User:user_dashboard')
    
    events = tbl_event.objects.all().select_related('industry', 'event_city', 'user')
    user_requests = tbl_request.objects.filter(user=user).values_list('event_id', flat=True)  # Now just 'event_id'
    return render(request, 'User/volunteer-dashboard.html', {
        'events': events,
        'user_requests': user_requests
    })

# Volunteer request
def request_to_volunteer(request, event_id):
    if 'u_id' not in request.session:
        return redirect('Guest:login')
    user = tbl_user.objects.get(id=request.session['u_id'])
    if user.user_type != "volunteer":
        return redirect('User:user_dashboard')
    
    if request.method == "POST":
        event = tbl_event.objects.get(id=event_id)
        if not tbl_request.objects.filter(user=user, event=event).exists():
            tbl_request.objects.create(
                user=user,
                event=event
                # request_datetime is auto-set
            )
        return redirect('User:volunteer_dashboard')
    return redirect('User:volunteer_dashboard')

# Organizer dashboard
def organizer_dashboard(request):
    if 'u_id' not in request.session:
        return redirect('Guest:login')
    user = tbl_user.objects.get(id=request.session['u_id'])
    if user.user_type != "organizer":
        return redirect('User:user_dashboard')
    return render(request, 'User/organizer-dashboard.html')

def user_dashboard(request):
    return render(request, 'User/userDashboard.html')