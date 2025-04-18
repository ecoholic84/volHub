from django.shortcuts import render, redirect
from django.utils import timezone
from Guest.models import *
from User.models import *
from Admin.models import *
import json
from django.http import JsonResponse
from .models import tbl_skill, tbl_user, tbl_request, tbl_event
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseBadRequest


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
    

from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from User.models import tbl_user, tbl_country, tbl_state, tbl_city  # Adjust imports as needed

# Basic Profile Creation
def create_profile(request):
    country = tbl_country.objects.all()
    state = tbl_state.objects.all()
    thisUser = tbl_user.objects.get(id=request.session['u_id'])
    if request.method == "POST":
        print("POST data:", request.POST)  # Debug line
        print("FILES data:", request.FILES)  # Debug line for file uploads
        thisUser.user_name = request.POST.get('txt_name')
        thisUser.user_username = request.POST.get('txt_username')
        thisUser.user_email = request.POST.get('txt_email')
        thisUser.user_contact = request.POST.get('txt_contact')  # Add contact
        thisUser.user_gender = request.POST.get('txt_gender')
        city_id = request.POST.get('sel_city')
        try:
            thisUser.user_city = tbl_city.objects.get(id=city_id) if city_id else None
        except ObjectDoesNotExist:
            return render(request, 'User/create_profile.html', {
                'country': country,
                'state': state,
                'error': f"City with ID {city_id} does not exist."
            })
        if 'txt_photo' in request.FILES:  # Check if a file was uploaded
            thisUser.user_photo = request.FILES['txt_photo']  # Add profile photo
        thisUser.user_bio = request.POST.get('txt_bio')
        thisUser.save()
        if thisUser.user_type == 'volunteer':
            return redirect('User:volunteer_dashboard')
        elif thisUser.user_type == 'organizer':
            return redirect('User:organizer_dashboard')
        else:
            return redirect('User:user_who')
    else:
        return render(request, 'User/create_profile.html', {'country': country, 'state': state,'thisUser':thisUser})
    
def profile_country_ajax(request):
    state=tbl_state.objects.filter(country=request.GET.get("did"))
    return render(request,'User/profile_country_ajax.html', {"state":state})
    
def profile_state_ajax(request):
    city=tbl_city.objects.filter(state=request.GET.get("did"))
    return render(request,'User/profile_state_ajax.html', {"city":city})

def Event(request):
    country = tbl_country.objects.all()
    industry = tbl_industry.objects.all()
    skills = tbl_skill.objects.all()  # For multi-select of required skills
    user = tbl_user.objects.get(id=request.session['u_id'])

    if request.method == "POST":
        title = request.POST.get("txt_title")
        description = request.POST.get("txt_description")
        file = request.FILES.get("txt_file")
        selected_industry = tbl_industry.objects.get(id=request.POST.get('sel_industry'))
        venue = request.POST.get("txt_venue")
        date_time = request.POST.get("txt_datetime")
        country_obj = tbl_country.objects.get(id=request.POST.get('sel_country'))  # still used in template, so kept
        city = tbl_city.objects.get(id=request.POST.get('sel_city'))
        stipend = request.POST.get('txt_stipend')
        volunteer_slots = request.POST.get('txt_slots')
        application_deadline = request.POST.get('txt_deadline')
        selected_skills = request.POST.getlist('sel_skills')  # multi-select skill IDs

        # Create event instance
        event = tbl_event.objects.create(
            event_title=title,
            event_content=description,
            event_file=file,
            event_venue=venue,
            event_datetime=date_time,
            event_city=city,
            event_stipend=stipend,
            industry=selected_industry,
            user=user,
            volunteer_slots=volunteer_slots,
            application_deadline=application_deadline
        )

        # Assign ManyToMany skill relationships
        event.required_skills.set(selected_skills)

        return redirect("User:Event")

    else:
        return render(request, 'User/event.html', {
            'country': country,
            'industry': industry,
            'skills': skills
        })



#============ FROM HERE STARTS THE PAGES OF VOLUNTEER DASHBOARD ============

def volunteer_dashboard(request):
    user_id = request.session.get('u_id')
    if not user_id:
        return redirect('Guest:login')
    
    # Fetch user data
    user = tbl_user.objects.get(id=user_id)
    
    # Fetch upcoming events (excluding those the user has applied for with pending status)
    today = timezone.now().date()
    upcoming_events = tbl_event.objects.filter(
        event_datetime__gte=today,
        event_status=1,
        visibility=1
    ).exclude(
        id__in=tbl_request.objects.filter(
            user_id=user_id,
            request_status=0
        ).values('event_id')
    )
    
    # Fetch applied events for the logged-in user with request status
    applied_events = tbl_event.objects.filter(
        event_datetime__gte=today
    ).filter(
        id__in=tbl_request.objects.filter(
            user_id=user_id
        ).values('event_id')
    ).prefetch_related('requests')  # Changed to prefetch_related

    context = {
        'user': user,
        'upcoming_events': upcoming_events,
        'applied_events': applied_events,
        'username': request.session.get('username', 'User')
    }
    return render(request, 'User/volunteer_dashboard.html', context)



# def event_detail(request, event_id):
#     # Check if user is logged in and is a volunteer
#     if 'u_id' not in request.session or not tbl_user.objects.filter(
#         id=request.session['u_id'], user_type='volunteer'
#     ).exists():
#         return redirect('Guest:login')

#     # Fetch event with visibility and status checks
#     event = tbl_event.objects.filter(id=event_id, visibility=1, event_status=1).first()
#     if not event:
#         messages.error(request, "Event not found or not available.")
#         return redirect('User:volunteer_dashboard')

#     # Check if user has already requested this event
#     has_requested = tbl_request.objects.filter(
#         user_id=request.session['u_id'], event_id=event_id
#     ).exists()

#     # Handle form submission (request or undo)
#     if request.method == 'POST':
#         user = tbl_user.objects.get(id=request.session['u_id'])
#         if 'undo' in request.POST and has_requested:
#             tbl_request.objects.filter(user=user, event=event).delete()
#             messages.success(request, "Request undone successfully.")
#         elif 'request' in request.POST and not has_requested:
#             tbl_request.objects.create(user=user, event=event, request_status=0)
#             messages.success(request, "Request submitted successfully.")
#         else:
#             messages.warning(request, 
#                 "You have already requested this event." if has_requested 
#                 else "Nothing to undo.")
#         return redirect('User:event_detail', event_id=event_id)

#     return render(request, 'User/event_detail.html', {
#         'event': event,
#         'has_requested': has_requested
#     })


def event_detail(request, event_id):
    if 'u_id' not in request.session or not tbl_user.objects.filter(
        id=request.session['u_id'], user_type='volunteer'
    ).exists():
        return redirect('Guest:login')

    event = tbl_event.objects.filter(id=event_id, visibility=1, event_status=1).first()
    if not event:
        messages.error(request, "Event not found or not available.")
        return redirect('User:volunteer_dashboard')

    user = tbl_user.objects.get(id=request.session['u_id'])
    has_requested = tbl_request.objects.filter(user=user, event=event).exists()
    request_status = (tbl_request.objects.filter(user=user, event=event)
                     .values_list('request_status', flat=True).first() or 0)

    if request.method == 'POST':
        if 'undo' in request.POST and has_requested:
            tbl_request.objects.filter(user=user, event=event).delete()
            messages.success(request, "Request undone successfully.")
            has_requested = False
            request_status = 0
        elif 'request' in request.POST and not has_requested:
            tbl_request.objects.create(user=user, event=event, request_status=0)
            messages.success(request, "Request submitted to organizer successfully.")
            has_requested = True
            request_status = 0
        else:
            messages.warning(request, 
                "Your request is already being processed." if has_requested 
                else "Nothing to undo.")
        return redirect('User:event_detail', event_id=event_id)  # Refresh to get updated status

    return render(request, 'User/event_detail.html', {
        'event': event,
        'has_requested': has_requested,
        'request_status': request_status
    })

#============ FROM HERE STARTS THE PAGES OF ORGANIZER DASHBOARD ============

# Organizer dashboard
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

# View for the page which the organizer approves and rejects volunteers
def event_action(request, event_id):
    if 'u_id' not in request.session:
        return redirect('Guest:login')

    user = tbl_user.objects.get(id=request.session['u_id'])
    event = tbl_event.objects.filter(id=event_id).first()
    if not event:
        messages.error(request, "Event not found or you don't have access.")
        return redirect('User:organizer_dashboard')

    requests = tbl_request.objects.filter(event=event).select_related('user')

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        req = tbl_request.objects.filter(id=request_id, event=event).first()
        if req:
            if action == 'accept':
                req.request_status = 1
                message = f"Request from {req.user.user_email} accepted successfully!"
            elif action == 'reject':
                req.request_status = 2
                message = f"Request from {req.user.user_email} rejected successfully!"
            req.save()
            messages.success(request, message)
        return redirect('User:event_action', event_id=event_id)

    return render(request, 'User/org_event_detail.html', {
        'event': event,
        'requests': requests,
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

def create_vol_profile(request):
    thisUser = tbl_user.objects.get(id=request.session['u_id'])
    industries = tbl_industry.objects.all()  # Get all industries
    
    if request.method == "POST":
        # Update user fields from form data
        thisUser.user_address = request.POST.get('user_address')
        
        # Handle JSON links
        links = request.POST.get('user_links')
        if links:  # Only save if not empty
            try:
                json.loads(links)  # Validate JSON format
                thisUser.user_links = links
            except json.JSONDecodeError:
                return render(request, 'User/create_vol_profile.html', {
                    'thisUser': thisUser,
                    'industries': industries,  # Pass industries to template
                    'error': 'Invalid JSON format for professional links'
                })
        
        # Educational Information
        thisUser.user_degree_type = request.POST.get('user_degree_type')
        thisUser.user_institution = request.POST.get('user_institution')
        thisUser.user_field_of_study = request.POST.get('user_field_of_study')
        thisUser.user_graduation_month = request.POST.get('user_graduation_month')
        thisUser.user_graduation_year = request.POST.get('user_graduation_year')
        
        # Work Details
        thisUser.user_organization_name = request.POST.get('user_organization_name')
        thisUser.user_job_title = request.POST.get('user_job_title')
        
        # Get industry from tbl_industry
        industry_id = request.POST.get('user_industry')
        if industry_id:
            try:
                thisUser.user_industry = tbl_industry.objects.get(id=industry_id)
            except tbl_industry.DoesNotExist:
                return render(request, 'User/create_vol_profile.html', {
                    'thisUser': thisUser,
                    'industries': industries,  # Pass industries to template
                    'error': 'Selected industry does not exist.'
                })
        
        thisUser.user_location = request.POST.get('user_location')
        thisUser.user_official_address = request.POST.get('user_official_address')
        thisUser.user_official_contact_number = request.POST.get('user_official_contact_number')
        
        thisUser.save()
        return redirect('User:organizer_dashboard')
    else:
        return render(request, 'User/create_vol_profile.html', {
            'thisUser': thisUser,
            'industries': industries  # Pass industries to template
        })

def create_organizer_profile(request):
    thisUser = tbl_user.objects.get(id=request.session['u_id'])
    industries = tbl_industry.objects.all()  # Get all industries
    
    if request.method == "POST":
        # Update user fields from form data
        thisUser.user_address = request.POST.get('user_address')
        
        # Educational Information
        thisUser.user_degree_type = request.POST.get('user_degree_type')
        thisUser.user_institution = request.POST.get('user_institution')
        thisUser.user_field_of_study = request.POST.get('user_field_of_study')
        thisUser.user_graduation_month = request.POST.get('user_graduation_month')
        thisUser.user_graduation_year = request.POST.get('user_graduation_year')
        
        # Emergency Contact
        thisUser.user_emergency_name = request.POST.get('user_emergency_name')
        thisUser.user_emergency_phone = request.POST.get('user_emergency_phone')
        
        # Work Details
        thisUser.user_organization_name = request.POST.get('user_organization_name')
        thisUser.user_job_title = request.POST.get('user_job_title')
        
        # Get industry from tbl_industry
        industry_id = request.POST.get('user_industry')
        if industry_id:
            try:
                thisUser.user_industry = tbl_industry.objects.get(id=industry_id)
            except tbl_industry.DoesNotExist:
                return render(request, 'User/create_organizer_profile.html', {
                    'thisUser': thisUser,
                    'industries': industries,
                    'error': 'Selected industry does not exist.'
                })
        
        thisUser.user_location = request.POST.get('user_location')
        thisUser.user_official_address = request.POST.get('user_official_address')
        thisUser.user_official_contact_number = request.POST.get('user_official_contact_number')
        
        # Past Volunteering Experience
        has_volunteering = request.POST.get('has_volunteering') == 'yes'
        if has_volunteering:
            thisUser.user_past_volunteering = request.POST.get('user_past_volunteering')
        else:
            thisUser.user_past_volunteering = None
        
        thisUser.save()
        return redirect('User:organizer_dashboard')
    else:
        return render(request, 'User/create_organizer_profile.html', {
            'thisUser': thisUser,
            'industries': industries
        })
    
def skill_search_ajax(request):
    term = request.GET.get('term', '')
    skills = tbl_skill.objects.filter(skill_name__icontains=term).values('id', 'skill_name')[:10]
    return JsonResponse(list(skills), safe=False)

# Public Profile View
def profile(request):
    if 'u_id' not in request.session:
        return redirect('Guest:login')
    user = tbl_user.objects.get(id=request.session['u_id'])
    is_volunteer = 'volunteer' in user.user_type.lower() or 'both' in user.user_type.lower()
    is_organizer = 'organizer' in user.user_type.lower() or 'both' in user.user_type.lower()
    return render(request, 'User/profile.html', {
        'user': user,
        'is_volunteer': is_volunteer,
        'is_organizer': is_organizer
    })