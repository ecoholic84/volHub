from django.shortcuts import render, redirect
from django.utils import timezone
from Guest.models import *
from User.models import *
from Admin.models import *
import json
from django.http import JsonResponse
from .models import tbl_skill, tbl_user, tbl_request, tbl_event, tbl_country, tbl_state, tbl_user, tbl_city
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.core.mail import send_mail
from django.conf import settings
import magic
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Update profile photo via AJAX
@login_required
def update_profile_photo(request):
    if request.method == 'POST' and request.FILES.get('user_photo'):
        try:
            user = tbl_user.objects.get(id=request.session['u_id'])
            user.user_photo = request.FILES['user_photo']
            user.save()
            return JsonResponse({'status': 'success'})
        except Exception:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})

# Multi-step profile edit view with autosave
@login_required
def edit_profile(request, page=1):
    if 'u_id' not in request.session:
        return redirect('Guest:login')
    user = tbl_user.objects.get(id=request.session['u_id'])
    user_type = user.user_type
    user_city = tbl_city

    # Months and years for dropdowns
    months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    current_year = datetime.now().year
    years = list(range(current_year - 50, current_year + 10))

    # Handle autosave AJAX
    if request.method == 'POST' and request.POST.get('autosave') == 'true':
        field = request.POST.get('field')
        value = request.POST.get('value')
        if field and hasattr(user, field):
            if field == 'user_city':
                try:
                    city = tbl_city.objects.get(id=value)
                    setattr(user, field, city)
                except Exception:
                    pass
            else:
                setattr(user, field, value)
            user.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'})

    # Handle regular form submission (Next/Previous)
    if request.method == 'POST':
        if 'previous' in request.POST and page > 1:
            return redirect('User:edit_profile', page - 1)
        if 'next' in request.POST and page < 5:
            if page == 1:
                user.is_basic_profile_complete = True
            user.save()
            return redirect('User:edit_profile', page + 1)

    context = {
        'user': user,
        'user_type': user_type,
        'user_city': user_city,
        'page': page,
        'months': months,
        'years': years,
        'request': request, # Pass request to template for session access
    }
    return render(request, 'User/edit_profile.html', context)

# Create your views here.
def logout(request):
    request.session.flush()  # This deletes all session data for the user
    return redirect("Guest:index")

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

# Basic Profile Creation
def create_profile(request):
    country = tbl_country.objects.all()
    state = tbl_state.objects.all()
    thisUser = tbl_user.objects.get(id=request.session['u_id'])

    if request.method == "POST":
        data = request.POST
        files = request.FILES

        # Basic fields
        thisUser.user_name = data.get('txt_name')
        thisUser.user_username = data.get('txt_username')
        thisUser.user_email = data.get('txt_email')
        thisUser.user_contact = data.get('txt_contact')
        thisUser.user_gender = data.get('txt_gender')
        thisUser.user_bio = data.get('txt_bio')

        # City
        city_id = data.get('sel_city')
        if city_id:
            thisUser.user_city_id = city_id

        # Profile photo with validation
        file = files.get('txt_photo')
        if file:
            print(f"Received file: {file.name}, size: {file.size}")  # Debugging
            if file.size > 5 * 1024 * 1024:
                messages.error(request, 'Image too large (max 5MB).')
                return render(request, 'User/create_profile.html', {
                    'country': country, 'state': state, 'thisUser': thisUser
                })
            mime = magic.Magic(mime=True)
            if not mime.from_buffer(file.read(1024)).startswith('image/'):
                messages.error(request, 'Invalid image format.')
                return render(request, 'User/create_profile.html', {
                    'country': country, 'state': state, 'thisUser': thisUser
                })
            file.seek(0)  # Reset file pointer
            thisUser.user_photo = file

        # Check for basic profile completeness
        if (thisUser.user_name and thisUser.user_username and thisUser.user_email and thisUser.user_contact and
            thisUser.user_gender and thisUser.user_city_id and thisUser.user_bio):
            thisUser.is_basic_profile_complete = True
        else:
            thisUser.is_basic_profile_complete = False

        try:
            thisUser.save()
            request.session['gender'] = thisUser.user_gender
            request.session['profile_photo_url'] = thisUser.user_photo.url if thisUser.user_photo else ''
        except Exception as e:
            print(f"Error saving profile: {str(e)}")  # Debugging
            messages.error(request, f"Error saving profile: {str(e)}")
            return render(request, 'User/create_profile.html', {
                'country': country, 'state': state, 'thisUser': thisUser
            })

        return redirect({
            'volunteer': 'User:volunteer_dashboard',
            'organizer': 'User:organizer_dashboard',
            'both': 'User:volunteer_dashboard'
        }.get(thisUser.user_type, 'User:user_who'))

    return render(request, 'User/create_profile.html', {
        'country': country, 'state': state, 'thisUser': thisUser
    })

    
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

        from django.contrib import messages
        messages.success(request, 'Event created successfully!')
        return redirect("User:organizer_dashboard")

    else:
        return render(request, 'User/event.html', {
            'country': country,
            'industry': industry,
            'skills': skills
        })



#============ FROM HERE STARTS THE PAGES OF VOLUNTEER DASHBOARD ============

def volunteer_dashboard(request):
    request.session['last_dashboard_url'] = request.path
    user_id = request.session.get('u_id')
    if not user_id:
        return redirect('Guest:login')
    
    # Fetch user data
    user = tbl_user.objects.get(id=user_id)
    
    # Fetch upcoming events (exclude ALL events the user has ever applied to, regardless of request status)
    # Only events with visibility=1 (public) are shown to volunteers. Private events (visibility=0) are hidden even if admin approved.
    today = timezone.now().date()
    applied_event_ids = tbl_request.objects.filter(user_id=user_id).values_list('event_id', flat=True)
    upcoming_events = tbl_event.objects.filter(
        event_datetime__gte=today,
        event_status=1,
        visibility=1
    ).exclude(id__in=applied_event_ids)

    # Fetch applied events for the logged-in user (all events the user has applied to)
    applied_events = tbl_event.objects.filter(
        event_datetime__gte=today
    ).filter(
        id__in=applied_event_ids
    ).prefetch_related('requests')

    context = {
        'user': user,
        'upcoming_events': upcoming_events,
        'applied_events': applied_events,
        'username': request.session.get('username', 'User'),
        'dashboard_type': 'volunteer',
        'is_basic_profile_complete': getattr(user, 'is_basic_profile_complete', False),
        'is_volunteer_profile_complete': getattr(user, 'is_volunteer_profile_complete', False)
    }
    return render(request, 'User/volunteer_dashboard.html', context)


def event_detail(request, event_id):
    if 'u_id' not in request.session or not tbl_user.objects.filter(
        Q(id=request.session['u_id']) & Q(user_type__in=['volunteer', 'both'])
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

def delete_event(request, event_id):
    if 'u_id' not in request.session:
        return redirect('Guest:login')
    try:
        event = tbl_event.objects.get(id=event_id)
    except tbl_event.DoesNotExist:
        messages.error(request, 'Event not found.')
        return redirect('User:organizer_dashboard')
    # Only allow the creator to delete
    if event.user.id != request.session.get('u_id'):
        messages.error(request, 'You are not authorized to delete this event.')
        return redirect('User:organizer_dashboard')
    event.delete()
    messages.success(request, 'Event deleted successfully!')
    return redirect('User:organizer_dashboard')

def applied_volunteer_profile(request, req_id):
    # Only allow access if user is logged in
    if 'u_id' not in request.session:
        return redirect('Guest:login')
    try:
        user_request = tbl_request.objects.get(id=req_id)
    except tbl_request.DoesNotExist:
        from django.contrib import messages
        messages.error(request, 'Volunteer request not found.')
        return redirect('User:organizer_dashboard')
    volunteer = user_request.user
    return render(request, 'User/applied_volunteer_profile.html', {
        'volunteer': volunteer,
        'user_request': user_request
    })


def edit_event(request, event_id):
    from django.contrib import messages
    try:
        event = tbl_event.objects.get(id=event_id)
    except tbl_event.DoesNotExist:
        messages.error(request, 'Event not found.')
        return redirect('User:organizer_dashboard')

    # Only allow the creator to edit
    if event.user.id != request.session.get('u_id'):
        messages.error(request, 'You are not authorized to edit this event.')
        return redirect('User:organizer_dashboard')

    country = tbl_country.objects.all()
    industry = tbl_industry.objects.all()
    skills = tbl_skill.objects.all()
    states = tbl_state.objects.filter(country=event.event_city.state.country) if event.event_city else tbl_state.objects.none()
    cities = tbl_city.objects.filter(state=event.event_city.state) if event.event_city else tbl_city.objects.none()

    if request.method == "POST":
        event.event_title = request.POST.get('txt_title')
        event.event_content = request.POST.get('txt_description')
        event.event_venue = request.POST.get('txt_venue')
        event.event_stipend = request.POST.get('txt_stipend')
        event.event_slots = request.POST.get('txt_slots')
        event.event_deadline = request.POST.get('txt_deadline')
        event.event_datetime = request.POST.get('txt_datetime')

        # Foreign keys
        industry_id = request.POST.get('sel_industry')
        city_id = request.POST.get('sel_city')
        if industry_id:
            event.industry = tbl_industry.objects.get(id=industry_id)
        if city_id:
            event.event_city = tbl_city.objects.get(id=city_id)

        # File upload
        if request.FILES.get('txt_file'):
            event.event_file = request.FILES['txt_file']

        event.save()

        # Skills (ManyToMany)
        selected_skills = request.POST.getlist('sel_skills')
        event.required_skills.set(selected_skills)

        messages.success(request, 'Event updated successfully!')
        return redirect('User:event_action', event_id=event.id)

    return render(request, 'User/edit_event.html', {
        'event': event,
        'country': country,
        'industry': industry,
        'skills': skills,
        'states': states,
        'cities': cities
    })

def switch_dashboard(request):
    if 'u_id' not in request.session:
        return redirect('Guest:login')
    user = tbl_user.objects.get(id=request.session['u_id'])
    # Always set user_type to 'both' if not already
    if user.user_type != 'both':
        user.user_type = 'both'
        user.save()

    from_dashboard = request.GET.get('from')
    # Determine which profiles are required for switching
    # If switching from volunteer, require basic + organizer
    # If switching from organizer, require basic + volunteer
    is_basic_complete = getattr(user, 'is_basic_profile_complete', False)
    is_org_complete = getattr(user, 'is_organizer_profile_complete', False)
    is_vol_complete = getattr(user, 'is_volunteer_profile_complete', False)
    from django.contrib import messages
    if from_dashboard == 'volunteer':
        if not (is_basic_complete and is_org_complete):
            if not is_basic_complete:
                messages.error(request, 'You must complete your basic profile before switching to the organizer dashboard.')
                return redirect('User:edit_profile')
            if not is_org_complete:
                messages.error(request, 'You must complete your organizer profile before switching to the organizer dashboard.')
                return redirect('User:create_organizer_profile')
        return redirect('User:organizer_dashboard')
    elif from_dashboard == 'organizer':
        if not (is_basic_complete and is_vol_complete):
            if not is_basic_complete:
                messages.error(request, 'You must complete your basic profile before switching to the volunteer dashboard.')
                return redirect('User:edit_profile')
            if not is_vol_complete:
                messages.error(request, 'You must complete your volunteer profile before switching to the volunteer dashboard.')
                return redirect('User:create_vol_profile')
        return redirect('User:volunteer_dashboard')
    # fallback to user_type logic
    if user.user_type in ["organizer", "both"]:
        return redirect('User:organizer_dashboard')
    else:
        return redirect('User:volunteer_dashboard')

def organizer_dashboard(request):
    request.session['last_dashboard_url'] = request.path
    if 'u_id' not in request.session:
        return redirect('Guest:login')
    
    user = tbl_user.objects.get(id=request.session['u_id'])
    if user.user_type not in ["organizer", "both"]:
        return redirect('User:volunteer_dashboard')
    
    # Fetch events created by this organizer
    organizer_events = tbl_event.objects.filter(user=user).select_related('industry', 'event_city')
    active_events = organizer_events.filter(event_status=1)

    # Unique volunteers across all events
    from django.db.models import Q
    volunteer_ids = set()
    for event in organizer_events:
        volunteer_ids.update(event.requests.values_list('user_id', flat=True))
    total_volunteers = tbl_user.objects.filter(id__in=volunteer_ids)

    return render(request, 'User/organizer-dashboard.html', {
        'events': organizer_events,
        'active_events': active_events,
        'total_volunteers': total_volunteers,
        'organizer': user,
        'dashboard_type': 'organizer',
        'is_basic_profile_complete': getattr(user, 'is_basic_profile_complete', False),
        'is_organizer_profile_complete': getattr(user, 'is_organizer_profile_complete', False)
    })

# Organizer Profile View

def organizer_profile(request, event_id):
    if 'u_id' not in request.session:
        return redirect('Guest:login')
    try:
        event = tbl_event.objects.get(id=event_id)
        organizer = event.user
    except tbl_event.DoesNotExist:
        from django.contrib import messages
        messages.error(request, 'Event not found.')
        return redirect('User:volunteer_dashboard')
    # Add extra context from profile view
    is_volunteer = 'volunteer' in organizer.user_type.lower() or 'both' in organizer.user_type.lower()
    is_organizer = 'organizer' in organizer.user_type.lower() or 'both' in organizer.user_type.lower()
    return render(request, 'User/organizer_profile.html', {
        'organizer': organizer,
        'is_volunteer': is_volunteer,
        'is_organizer': is_organizer
    })

# Organizer Analytics View

def organizer_analytics(request):
    if 'u_id' not in request.session:
        return redirect('Guest:login')
    user = tbl_user.objects.get(id=request.session['u_id'])
    if user.user_type not in ["organizer", "both"]:
        return redirect('User:volunteer_dashboard')

    events = tbl_event.objects.filter(user=user).prefetch_related('required_skills', 'requests')

    # Status breakdown
    status_map = {0: 'Pending', 1: 'Approved', 2: 'Rejected'}
    status_counts = {'Approved': 0, 'Pending': 0, 'Rejected': 0}
    for event in events:
        status_label = status_map.get(event.event_status, 'Pending')
        status_counts[status_label] = status_counts.get(status_label, 0) + 1

    # Volunteer signups per event
    volunteer_counts = {}
    total_volunteers = 0
    for event in events:
        count = event.requests.count()
        volunteer_counts[event.id] = count
        total_volunteers += count

    engagement_rate = 0
    if events.count() > 0:
        engagement_rate = int((total_volunteers / events.count()) * 100) if total_volunteers > 0 else 0

    context = {
        'organizer': user,
        'events': events,
        'status_counts': status_counts,
        'total_volunteers': total_volunteers,
        'engagement_rate': engagement_rate,
    }
    return render(request, 'User/organizer_analytics.html', context)

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

    # Add counts for template
    pending_count = requests.filter(request_status=0).count()
    approved_count = requests.filter(request_status=1).count()
    rejected_count = requests.filter(request_status=2).count()

    if request.method == 'POST':
        # Handle visibility toggle
        if 'toggle_visibility' in request.POST:
            event.visibility = 0 if event.visibility else 1
            event.save()
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        req = tbl_request.objects.filter(id=request_id, event=event).first()
        if req:
            if action == 'accept':
                req.request_status = 1
                # email=req.user.user_email

                user_name = req.user.user_name
                event = req.event  # Or use req.event if you're directly accessing the event via the request

                event_date = event.event_datetime.strftime('%d-%m-%Y')
                event_time = event.event_datetime.strftime('%I:%M %p')
                event_details = (
                    f"Event     : {event.event_title}\n"
                    f"Date      : {event_date}\n"
                    f"Time      : {event_time}\n"
                    f"Venue     : {event.event_venue}, {event.event_city.name}\n"
                )

                message_body = (
                    f"Hello {user_name},\n\n"
                    "Congratulations! We're excited to inform you that your application to join us as a volunteer has been accepted.\n\n"
                    "Here are the details of the event you've been selected for:\n\n"
                    f"{event_details}\n"
                    "Thank you for your willingness to contribute and make a difference. We'll be reaching out soon with more details about your role and next steps.\n\n"
                    "Best regards,\n"
                    "The Team"
                )

                send_mail(
                    subject='Volunteer Application Accepted',
                    message=message_body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[req.user.user_email],
                )

                message = f"Request from {req.user.user_email} accepted successfully!"

            elif action == 'reject':
                req.request_status = 2
                email=req.user.user_email
                send_mail(
            subject='Regarding Your Volunteering Application',
            message=(
                f"Dear {req.user.user_name},\n\n"
                f"Thank you so much for your interest in volunteering with us for {event.event_title}. "
                "We truly appreciate the time and effort you took to apply.\n\n"
                "After careful consideration, we regret to inform you that we are unable to include you "
                "in this event’s volunteer team.\n\n"
                "We hope you’ll stay connected with us and consider applying for future opportunities.\n\n"
                "Warm regards,\n"
                "The Team"
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

            message = f"Request from {req.user.user_email} rejected successfully!"
            req.save()
            messages.success(request, message)
            return redirect('User:event_action', event_id=event_id)

    # Resolve city, state, and country for the event location
    event_city = event.event_city if event and event.event_city_id else None
    event_state = event_city.state if event_city and event_city.state_id else None
    event_country = event_state.country if event_state and event_state.country_id else None

    return render(request, 'User/org_event_detail.html', {
        'event': event,
        'requests': requests,
        'event_city': event_city,
        'event_state': event_state,
        'event_country': event_country,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
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
    industries = tbl_industry.objects.all()  # Get all industries for the dropdown
    
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
        
        # Get industry name from dropdown
        thisUser.user_industry = request.POST.get('user_industry')  # Store as string
        
        thisUser.user_location = request.POST.get('user_location')
        thisUser.user_official_address = request.POST.get('user_official_address')
        thisUser.user_official_contact_number = request.POST.get('user_official_contact_number')

        # Emergency details
        thisUser.user_emergency_name = request.POST.get('user_emergency_name')
        thisUser.user_emergency_phone = request.POST.get('user_emergency_phone')

        # Past volunteer experience
        thisUser.user_past_volunteering = request.POST.get('user_past_volunteering')
        
        # Check for volunteer profile completeness
        if (
            thisUser.user_address and
            thisUser.user_degree_type and
            thisUser.user_institution and
            thisUser.user_field_of_study and
            thisUser.user_emergency_name and
            thisUser.user_emergency_phone and
            thisUser.user_organization_name and
            thisUser.user_job_title and
            thisUser.user_industry and
            thisUser.user_location and
            thisUser.user_official_contact_number and
            thisUser.user_official_address
        ):
            thisUser.is_volunteer_profile_complete = True
        else:
            thisUser.is_volunteer_profile_complete = False

        thisUser.save()
        messages.success(request, 'Volunteer profile updated successfully!')
        return redirect('User:volunteer_dashboard')
    else:
        import datetime
        current_year = datetime.datetime.now().year
        year_range = list(range(current_year, 1949, -1))
        return render(request, 'User/create_vol_profile.html', {
            'thisUser': thisUser,
            'industries': industries,  # Pass industries to template
            'year_range': year_range
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
        
        # Work Details
        thisUser.user_organization_name = request.POST.get('user_organization_name')
        thisUser.user_job_title = request.POST.get('user_job_title')
        
        # Get industry
        thisUser.user_industry = request.POST.get('user_industry')
        
        thisUser.user_location = request.POST.get('user_location')
        thisUser.user_official_address = request.POST.get('user_official_address')
        thisUser.user_official_contact_number = request.POST.get('user_official_contact_number')

        # Check for organizer profile completeness
        if (
            thisUser.user_address and
            thisUser.user_degree_type and
            thisUser.user_institution and
            thisUser.user_field_of_study and
            thisUser.user_organization_name and
            thisUser.user_job_title and
            thisUser.user_industry and
            thisUser.user_location and
            thisUser.user_official_contact_number and
            thisUser.user_official_address
        ):
            thisUser.is_organizer_profile_complete = True
        else:
            thisUser.is_organizer_profile_complete = False
        
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

# Settings View
def delete_account(request, user):
    user.delete()
    request.session.flush()
    messages.success(request, 'Your account has been deleted.')
    return redirect('Guest:login')

def settings_page(request):
    if 'u_id' not in request.session:
        return redirect('Guest:login')
    user = tbl_user.objects.get(id=request.session['u_id'])
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'change_password':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if user.user_password != old_password:
                messages.error(request, 'Current password is incorrect.')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
            elif not new_password:
                messages.error(request, 'New password cannot be empty.')
            elif len(new_password) < 6:
                messages.error(request, 'Password must be at least 6 characters long.')
            else:
                user.user_password = new_password
                user.save()
                messages.success(request, 'Password changed successfully!')
        elif action == 'delete_account':
            return delete_account(request, user)
    return render(request, 'User/settings.html')

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

def converse(request, event_id):
    # Only allow logged-in users
    if 'u_id' not in request.session:
        return redirect('Guest:login')
    event = tbl_event.objects.get(id=event_id)
    # Get all requests for this event
    requests = tbl_request.objects.filter(event=event).select_related('user')
    accepted_users = [req.user for req in requests if req.request_status == 1]
    rejected_users = [req.user for req in requests if req.request_status == 2]

    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('body')
        recipient_group = request.POST.get('recipient_group', 'accepted')
        if recipient_group == 'rejected':
            recipients = [user.user_email for user in rejected_users]
        else:
            recipients = [user.user_email for user in accepted_users]
        if not subject or not message or not recipients:
            messages.error(request, 'All fields are required and at least one recipient must be present.')
            return render(request, 'User/converse.html', {
                'event': event,
                'subject': subject,
                'body': message,
                'recipient_group': recipient_group,
                'accepted_users': accepted_users,
                'rejected_users': rejected_users,
            })
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipients,
                fail_silently=False,
            )
            messages.success(request, f'Email sent to {len(recipients)} user(s) successfully!')
            from django.urls import reverse
            from django.http import HttpResponseRedirect
            return HttpResponseRedirect(reverse('User:converse', args=[event.id]) + '?success=1')
        except Exception as e:
            messages.error(request, f'Error sending email: {str(e)}')
            return render(request, 'User/converse.html', {
                'event': event,
                'subject': subject,
                'body': message,
                'recipient_group': recipient_group,
                'accepted_users': accepted_users,
                'rejected_users': rejected_users,
            })
    else:
        if request.GET.get('success'):
            messages.success(request, 'Email sent successfully!')
        return render(request, 'User/converse.html', {
            'event': event,
            'accepted_users': accepted_users,
            'rejected_users': rejected_users,
            'recipient_group': 'accepted',
        })