from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from Admin.models import *
from User.models import *
from datetime import datetime
from django.urls import reverse

# Create your views here.

# District Section
def district(request):    
    district=tbl_district.objects.all()
    if request.method=="POST":
        tbl_district.objects.create(district_name=request.POST.get('txt_district'))
        return redirect('Admin:district')
    else:    
        return render(request,'Admin/District.html',{"district":district})
    
def deletedistrict(request,did):
    tbl_district.objects.get(id=did).delete()
    return redirect('Admin:district')

def editdistrict(request,eid):
    dist=tbl_district.objects.get(id=eid)
    if request.method=="POST":
        dist.district_name=request.POST.get('txt_district')
        dist.save()
        return redirect('Admin:district')
    else:    
        return render(request,'Admin/District.html',{"editdist":dist})

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

#Place Section
def Place(request):
    district=tbl_district.objects.all()
    Place=tbl_place.objects.all()
    if request.method=="POST":
        dist=tbl_district.objects.get(id=request.POST.get("sel_district"))
        place_name=request.POST.get("txt_place")
        tbl_place.objects.create(district=dist,place_name=place_name)
        return redirect('Admin:Place')
    else:
        return render(request,'Admin/Place.html',{"district":district,"place":Place})
    
def editPlace(request, eid):
    plac=tbl_place.objects.get(id=eid)
    district=tbl_district.objects.all()
    if request.method=="POST":
        plac.district=tbl_district.objects.get(id=request.POST.get("sel_district"))
        plac.place_name=request.POST.get('txt_place')
        plac.save()
        return redirect('Admin:Place')
    else:
        return render(request,'Admin/Place.html',{"editPlace":plac, "district":district})
    
def deletePlace(request,did):
    tbl_place.objects.get(id=did).delete()
    return redirect('Admin:Place')

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

#Subcategory
def Subcategory(request):
    category=tbl_category.objects.all()
    subcategory=tbl_subcategory.objects.all()
    if request.method=="POST":
        cat=tbl_category.objects.get(id=request.POST.get("sel_category"))
        sub=request.POST.get("txt_subcategory")
        tbl_subcategory.objects.create(category=cat,subcategory_name=sub)
        return render(request,'Admin/Subcategory.html',{"category":category,"subcategory":subcategory})
    else:
        return render(request,'Admin/Subcategory.html',{"category":category,"subcategory":subcategory})
    
def deleteSubcategory(request,did):
    tbl_subcategory.objects.get(id=did).delete()
    return redirect('Admin:subcategory')

def editSubcategory(request,eid):
    sub=tbl_subcategory.objects.get(id=eid)
    category=tbl_category.objects.all()
    if request.method=="POST":
        sub.category=tbl_category.objects.get(id=request.POST.get("sel_category"))
        sub.subcategory_name=request.POST.get('txt_subcategory')
        sub.save()
        return redirect('Admin:subcategory')
    else:
        return render(request,'Admin/Subcategory.html',{"editsub":sub, "category":category})

# Dashboard
def adminDashboard(request):
    return render(request,'Admin/adminDashboard.html')

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
    if 'u_id' not in request.session:  # Assuming admin uses same session key
        return redirect('Guest:login')  # Adjust to your admin login URL if different
    industries = tbl_industry.objects.all().prefetch_related('skills')  # No user filter for admin
    return render(request, 'Admin/industry_skills.html', {'industries': industries})

def addIndustry(request):
    if 'u_id' not in request.session:
        return redirect('Guest:login')
    if request.method == "POST":
        industry_name = request.POST.get('txt_industry_name')
        admin_user = tbl_user.objects.get(id=request.session['u_id'])  # Assuming admin is a user
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
    if 'u_id' not in request.session:
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
    if 'u_id' not in request.session:
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
    if 'u_id' not in request.session:
        return redirect('Guest:login')
    tbl_skill.objects.get(id=sid).delete()
    return redirect('Admin:industrySkills')

def deleteIndustry(request, iid):
    if 'u_id' not in request.session:
        return redirect('Guest:login')
    tbl_industry.objects.get(id=iid).delete()
    return redirect('Admin:industrySkills')