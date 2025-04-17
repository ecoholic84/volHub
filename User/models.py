from django.db import models
from Guest.models import *

# Create your models here.

class tbl_feedback(models.Model):
    feedback_content=models.CharField(max_length=1000)
    feedback_date=models.DateField(auto_now_add=True)
    user_id=models.ForeignKey(tbl_user, on_delete=models.CASCADE)

class tbl_complaint(models.Model):
    complaint_title=models.CharField(max_length=30)
    complaint_content=models.CharField(max_length=1000)
    complaint_date=models.DateField(auto_now_add=True)
    complaint_reply=models.CharField(max_length=1000)
    complaint_reply_date=models.DateField(null=True)
    complaint_status=models.IntegerField(default=0)
    user_id=models.ForeignKey(tbl_user, on_delete=models.CASCADE)

class tbl_industry(models.Model):
    industry_name = models.CharField(max_length=100, unique=True)

class tbl_skill(models.Model):
    industry = models.ForeignKey(tbl_industry, on_delete=models.CASCADE, related_name="skills")
    skill_name = models.CharField(max_length=100)

class tbl_event(models.Model):
    event_title=models.CharField(max_length=30)
    event_content=models.CharField(max_length=30)
    event_datetime=models.DateTimeField()
    event_file=models.FileField(upload_to="Assets/Files/User")
    event_created_at = models.DateTimeField(auto_now_add=True)
    event_venue=models.CharField(max_length=30)
    event_city=models.ForeignKey(tbl_city,on_delete=models.CASCADE)
    event_stipend=models.CharField(max_length=30)
    event_status=models.IntegerField(default=0)
    industry=models.ForeignKey(tbl_industry,on_delete=models.CASCADE)
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
    volunteer_slots=models.PositiveIntegerField(default=1)
    required_skills=models.ManyToManyField(tbl_skill)
    application_deadline=models.DateTimeField()
    visibility=models.IntegerField(default=1)

class tbl_request(models.Model):
    request_datetime = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(tbl_event, on_delete=models.CASCADE, related_name='requests')
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE, related_name='volunteer_requests')
    request_status = models.IntegerField(default=0)