from django.shortcuts import render,redirect
from Admin.models import *
from User.models import *
from datetime import datetime

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
    
# Industry
def Industry(request):
    industry=tbl_industry.objects.all()
    if request.method=='POST':
        tbl_industry.objects.create(industry_name=request.POST.get('txt_industry_name'))
        return redirect('Admin:industries')
    else:
        return render(request, 'Admin/industry.html', {'industries':industry})

def editIndustry(request, eid):
    thisIndustry = tbl_industry.objects.get(id=eid)
    if request.method=='POST':
        thisIndustry.industry_name=request.POST.get('txt_industry_name')
        thisIndustry.save()
        return redirect('Admin:industries')
    else:
        return render(request, 'Admin/industry.html', {'editIndustry':thisIndustry})

def deleteIndustry(request, did):
    tbl_industry.objects.get(id=did).delete()
    return redirect('Admin:industries')