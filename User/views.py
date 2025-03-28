from django.shortcuts import render, redirect
from Guest.models import *
from User.models import *
from Admin.models import *

# Create your views here.
def logout(request):
    del request.session["u_id"]
    return redirect("Guest:login")

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

def volunteer_dashboard(request):
    if 'u_id' not in request.session:
        return redirect('Guest:login')
    
    user = tbl_user.objects.get(id=request.session['u_id'])
    if user.user_type != "volunteer":
        return redirect('Guest:user_who')  # Consistent redirect
    
    # Fetch all requests made by this volunteer
    user_requests = tbl_request.objects.filter(user=user).select_related('event', 'event__industry', 'event__event_city')
    
    return render(request, 'User/volunteer-dashboard.html', {
        'requests': user_requests
    })

def request_to_volunteer(request, event_id):
    if 'u_id' not in request.session:
        return redirect('Guest:login')
    
    user = tbl_user.objects.get(id=request.session['u_id'])
    if user.user_type != "volunteer":
        return redirect('Guest:user_who')
    
    if request.method == "POST":
        event = tbl_event.objects.get(id=event_id)
        if not tbl_request.objects.filter(user=user, event=event).exists():
            tbl_request.objects.create(user=user, event=event, request_status=0)
            message = "Request submitted successfully!"
        else:
            message = "You have already requested this event."
        
        events = tbl_event.objects.filter(event_status=1).select_related('industry', 'event_city', 'user')
        user_requests = tbl_request.objects.filter(user=user).select_related('event')
        request_dict = {req.event.id: req.request_status for req in user_requests}
        
        return render(request, 'User/volunteer-dashboard.html', {
            'events': events,
            'user_requests': request_dict,
            'volunteer': user,
            'success': message
        })
    
    return redirect('User:volunteer_dashboard')


# Organizer dashboard and event detail page
def organizer_dashboard(request):
    if 'u_id' not in request.session:
        return redirect('Guest:login')
    
    user = tbl_user.objects.get(id=request.session['u_id'])
    if user.user_type != "organizer":
        return redirect('User:user_dashboard')  # Matches your initial redirect
    
    # Fetch events created by this organizer
    organizer_events = tbl_event.objects.filter(user=user).select_related('industry', 'event_city')
    
    return render(request, 'User/organizer-dashboard.html', {
        'events': organizer_events,
        'organizer': user
    })

# Ensure organizer event_detail view is correct for request updates
def event_detail(request, event_id):
    if 'u_id' not in request.session:
        return redirect('Guest:login')
    
    user = tbl_user.objects.get(id=request.session['u_id'])
    if user.user_type != "organizer":
        return redirect('Guest:user_who')
    
    try:
        event = tbl_event.objects.get(id=event_id, user=user)
    except tbl_event.DoesNotExist:
        return render(request, 'User/event_detail.html', {'error': "Event not found or you don’t have access."})
    
    requests = tbl_request.objects.filter(event=event).select_related('user')
    
    if request.method == "POST":
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        req = tbl_request.objects.get(id=request_id, event=event)
        
        if action == "accept":
            req.request_status = 1  # Accepted
            req.save()
            message = f"Request from {req.user.user_email} accepted successfully!"
        elif action == "reject":
            req.request_status = 2  # Rejected
            req.save()
            message = f"Request from {req.user.user_email} rejected successfully!"
            requests = tbl_request.objects.filter(event=event).select_related('user')
        return render(request, 'User/event_detail.html', {
            'event': event,
            'requests': requests,
            'success': message
        })
    
    return render(request, 'User/event_detail.html', {
        'event': event,
        'requests': requests
    })

def edit_profile(request, page=1):
    if 'u_id' not in request.session:
        return redirect('Guest:login')
    
    user = tbl_user.objects.get(id=request.session['u_id'])
    
    # Validate page number
    if page < 1 or page > 5:
        page = 1
    
    # Define months for the dropdown
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    # Define years for the dropdown
    years = [str(year) for year in range(2020, 2031)]
    
    if request.method == "POST":
        if 'autosave' in request.POST:
            # Handle auto-save via AJAX
            field = request.POST.get('field')
            value = request.POST.get('value')
            if field == 'user_name':
                user.user_name = value
            elif field == 'user_gender':
                user.user_gender = value
            elif field == 'user_bio':
                user.user_bio = value
            elif field == 'user_degree_type':
                user.user_degree_type = value
            elif field == 'user_institution':
                user.user_institution = value
            elif field == 'user_field_of_study':
                user.user_field_of_study = value
            elif field == 'user_graduation_month':
                user.user_graduation_month = int(value) if value else None
            elif field == 'user_graduation_year':
                user.user_graduation_year = int(value) if value else None
            elif field == 'user_organization_name':
                user.user_organization_name = value
            elif field == 'user_job_title':
                user.user_job_title = value
            elif field == 'user_industry':
                user.user_industry = value
            elif field == 'user_location':
                user.user_location = value
            elif field == 'user_links':
                user.user_links = value
            elif field == 'user_contact':
                user.user_contact = value
            elif field == 'user_emergency_name':
                user.user_emergency_name = value
            elif field == 'user_emergency_phone':
                user.user_emergency_phone = value
            user.save()
            return JsonResponse({'status': 'success'})
        else:
            # Handle form submission (Next/Previous)
            user.user_name = request.POST.get('user_name', user.user_name)
            user.user_gender = request.POST.get('user_gender', user.user_gender)
            user.user_bio = request.POST.get('user_bio', user.user_bio)
            user.user_degree_type = request.POST.get('user_degree_type', user.user_degree_type)
            user.user_institution = request.POST.get('user_institution', user.user_institution)
            user.user_field_of_study = request.POST.get('user_field_of_study', user.user_field_of_study)
            user.user_graduation_month = int(request.POST.get('user_graduation_month')) if request.POST.get('user_graduation_month') else user.user_graduation_month
            user.user_graduation_year = int(request.POST.get('user_graduation_year')) if request.POST.get('user_graduation_year') else user.user_graduation_year
            user.user_organization_name = request.POST.get('user_organization_name', user.user_organization_name)
            user.user_job_title = request.POST.get('user_job_title', user.user_job_title)
            user.user_industry = request.POST.get('user_industry', user.user_industry)
            user.user_location = request.POST.get('user_location', user.user_location)
            user.user_links = request.POST.get('user_links', user.user_links)
            user.user_contact = request.POST.get('user_contact', user.user_contact)
            user.user_emergency_name = request.POST.get('user_emergency_name', user.user_emergency_name)
            user.user_emergency_phone = request.POST.get('user_emergency_phone', user.user_emergency_phone)
            user.save()
            
            if 'next' in request.POST:
                page = int(page) + 1
            elif 'previous' in request.POST:
                page = int(page) - 1
            return redirect('User:edit_profile', page=page)
    
    return render(request, 'User/edit_profile.html', {  # Update template path to User/
        'user': user,
        'page': page,
        'user_type': user.user_type,
        'months': months,
        'years': years,
    })