from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from Admin.models import *
from User.models import *
from datetime import datetime
from django.urls import reverse
from django.db import IntegrityError

# Create your views here.

# Logout
def logout(request):
    del request.session["a_id"]
    return redirect("Guest:login")

# Admin Section
def adminRegistration(request):
    admin=tbl_admin.objects.all()
    if request.method=="POST":
        tbl_admin.objects.create(admin_name=request.POST.get('txt_name'),admin_email=request.POST.get('txt_email'),admin_password=request.POST.get('txt_password'))
        return redirect('Admin:adminRegistration')
    else:
        return render(request,'Admin/adminRegistration.html',{"admin":admin})

def deleteAdmin(request,did):
    tbl_admin.objects.get(id=did).delete()
    return redirect('Admin:adminRegistration')

def editAdmin(request,eid):
    adm=tbl_admin.objects.get(id=eid)
    if request.method=="POST":
        adm.admin_name=request.POST.get('txt_name')
        adm.admin_contact=request.POST.get('txt_contact')
        adm.admin_email=request.POST.get('txt_email')
        adm.admin_password=request.POST.get('txt_password')
        adm.save()
        return redirect('Admin:adminRegistration')
    else:
        return render(request,'Admin/adminRegistration.html',{"editadmin":editadmin})

# Category Section
def category(request):
    category=tbl_category.objects.all()
    if request.method=="POST":
        tbl_category.objects.create(category_name=request.POST.get('txt_category'))
        return redirect('Admin:category')
    else:
        return render(request,'Admin/Category.html',{"category":category})
def deleteCategory(request,did):
    tbl_category.objects.get(id=did).delete()
    return redirect('Admin:category')
def editCategory(request,eid):
    cat=tbl_category.objects.get(id=eid)
    if request.method=="POST":
        cat.category_name=request.POST.get('txt_category')
        cat.save()
        return redirect('Admin:category')
    else:
        return render(request,'Admin/Category.html',{"editcat":cat})

# Type
def types(request):
        typ=tbl_type.objects.all()
        if request.method=="POST":
            tbl_type.objects.create(type_name=request.POST.get('txt_type_name'))
            return redirect('Admin:type')
        else:    
            return render(request,'Admin/type.html',{"type":typ}) # here 'type' is a variable name and its assigned data is the variable 'typ'.

def deleteType(request,did):
    tbl_type.objects.get(id=did).delete()
    return redirect('Admin:type')

def editType(request,eid):
    thisType=tbl_type.objects.get(id=eid)
    if request.method=="POST":
        thisType.type_name=request.POST.get('txt_type_name')
        thisType.save()
        return redirect('Admin:type')
    else:
        return render(request,'Admin/type.html',{"editType":thisType})

# Compliant Inbox
def complaintInbox(request):
    complaints=tbl_complaint.objects.all()
    return render(request,'Admin/complaintInbox.html',{"complaintsInbox":complaints})

def replyCompliant(request,rid):
    thisCompliant=tbl_complaint.objects.get(id=rid)
    if request.method=="POST":
        thisCompliant.complaint_reply=request.POST.get("txt_compliant_content")
        thisCompliant.complaint_status=1
        thisCompliant.complaint_reply_date=datetime.now()
        thisCompliant.save()
        return redirect('Admin:complaintInbox')  
    else:
        return render(request,'Admin/replyCompliant.html')

# Industry and Skills Views
def industrySkills(request):
    if 'a_id' not in request.session:  # Assuming admin uses same session key
        return redirect('Guest:login')  # Adjust to your admin login URL if different
    industries = tbl_industry.objects.all().prefetch_related('skills')  # No user filter for admin
    return render(request, 'Admin/industry_skills.html', {'industries': industries})

def addIndustry(request):
    if 'a_id' not in request.session:
        return redirect('Guest:login')
    if request.method == "POST":
        industry_name = request.POST.get('txt_industry_name')
        admin_user = tbl_user.objects.get(id=request.session['a_id'])
        try:
            tbl_industry.objects.create(user_id=admin_user, industry_name=industry_name)
            return redirect('Admin:industrySkills')
        except IntegrityError:
            industries = tbl_industry.objects.all().prefetch_related('skills')
            return render(request, 'Admin/industry_skills.html', {
                'industries': industries,
                'error': 'Industry name must be unique'
            })
    return render(request, 'Admin/industry_skills.html')

def addSkill(request):
    if 'a_id' not in request.session:
        return redirect('Guest:login')
    industries = tbl_industry.objects.all().prefetch_related('skills')
    if request.method == "POST":
        industry_id = request.POST.get('industry_id')
        skill_name = request.POST.get('txt_skill_name')
        industry = tbl_industry.objects.get(id=industry_id)
        tbl_skill.objects.create(industry=industry, skill_name=skill_name)
        return redirect('Admin:industrySkills')
    return render(request, 'Admin/industry_skills.html', {'industries': industries})

def editSkill(request, sid):
    if 'a_id' not in request.session:
        return redirect('Guest:login')
    industries = tbl_industry.objects.all().prefetch_related('skills')
    thisSkill = tbl_skill.objects.get(id=sid)
    if request.method == "POST":
        thisSkill.skill_name = request.POST.get('txt_skill_name')
        thisSkill.save()
        return redirect('Admin:industrySkills')
    return render(request, 'Admin/industry_skills.html', {
        'industries': industries,
        'editSkill': thisSkill
    })

def deleteSkill(request, sid):
    if 'a_id' not in request.session:
        return redirect('Guest:login')
    tbl_skill.objects.get(id=sid).delete()
    return redirect('Admin:industrySkills')

def deleteIndustry(request, iid):
    if 'a_id' not in request.session:
        return redirect('Guest:login')
    tbl_industry.objects.get(id=iid).delete()
    return redirect('Admin:industrySkills')

# Admin/views.py
from django.shortcuts import render, redirect
from Admin.models import *
from Guest.models import *
from User.models import *

# Country, State, City Insertion Page
def country_state_city(request):
    if 'a_id' not in request.session:  # Matches your login view's session key
        return redirect('Admin:login')
    
    countries = tbl_country.objects.all()
    return render(request, 'Admin/country_state_city.html', {'countries': countries})

# Add Country
def add_country(request):
    if request.method == 'POST':
        country_code = request.POST.get('txt_country_code')
        country_name = request.POST.get('txt_country_name')
        phone_code = request.POST.get('txt_phone_code')
        if tbl_country.objects.filter(country_name=country_name).exists():
            message = "Country already exists!"
            return render(request, 'Admin/country_state_city.html', {
                'countries': tbl_country.objects.all(),
                'error': message
            })
        else:
            tbl_country.objects.create(
                country_code=country_code,
                country_name=country_name,
                country_phone_code=phone_code
            )
            message = "Country added successfully!"
            return render(request, 'Admin/country_state_city.html', {
                'countries': tbl_country.objects.all(),
                'success': message
            })
    return redirect('Admin:country_state_city')

# Add State
def add_state(request):
    if request.method == 'POST':
        country_id = request.POST.get('country_id')
        state_name = request.POST.get('txt_state_name')
        country = tbl_country.objects.get(id=country_id)
        if tbl_state.objects.filter(name=state_name, country=country).exists():
            message = "State already exists in this country!"
            return render(request, 'Admin/country_state_city.html', {
                'countries': tbl_country.objects.all(),
                'error': message
            })
        else:
            tbl_state.objects.create(name=state_name, country=country)
            message = "State added successfully!"
            return render(request, 'Admin/country_state_city.html', {
                'countries': tbl_country.objects.all(),
                'success': message
            })
    return redirect('Admin:country_state_city')

# Add City
def add_city(request):
    if request.method == 'POST':
        state_id = request.POST.get('state_id')
        city_name = request.POST.get('txt_city_name')
        state = tbl_state.objects.get(id=state_id)
        if tbl_city.objects.filter(name=city_name, state=state).exists():
            message = "City already exists in this state!"
            return render(request, 'Admin/country_state_city.html', {
                'countries': tbl_country.objects.all(),
                'error': message
            })
        else:
            tbl_city.objects.create(name=city_name, state=state)
            message = "City added successfully!"
            return render(request, 'Admin/country_state_city.html', {
                'countries': tbl_country.objects.all(),
                'success': message
            })
    return redirect('Admin:country_state_city')

def adminDashboard(request):
    if 'a_id' not in request.session:  # Matches your login view
        return redirect('Admin:login')
    
    # Fetch all events (no user_type filter)
    all_events = tbl_event.objects.all().select_related('user', 'industry', 'event_city')
    print(f"Number of events: {all_events.count()}")  # Debug line to verify count
    
    if request.method == "POST":
        event_id = request.POST.get('event_id')
        action = request.POST.get('action')
        event = tbl_event.objects.get(id=event_id)
        
        if action == "accept":
            event.event_status = 1  # Accepted
            event.save()
            message = f"Event '{event.event_title}' accepted successfully!"
            return render(request, 'Admin/adminDashboard.html', {
                'events': all_events,
                'success': message
            })
        elif action == "reject":
            event.event_status = 2  # Rejected
            event.save()
            message = f"Event '{event.event_title}' rejected successfully!"
            return render(request, 'Admin/adminDashboard.html', {
                'events': all_events,
                'success': message
            })
    
    return render(request, 'Admin/adminDashboard.html', {
        'events': all_events
    })