from django.db import models
from Admin.models import *

# Create your models here.

USER_TYPES = [
    ('volunteer', 'Volunteer'),
    ('organizer', 'Organizer'),
    ('both', 'Both'),
]

class tbl_user(models.Model):
    user_email = models.EmailField(max_length=50, unique=True)
    user_name = models.CharField(max_length=50, null=True, blank=True)
    user_username = models.CharField(max_length=50, null=True, blank=True)
    user_contact = models.CharField(max_length=10, null=True, blank=True)
    user_address = models.CharField(max_length=100, null=True, blank=True)
    user_password = models.CharField(max_length=128, null=True, blank=True)  # Store hashed password
    user_city = models.ForeignKey(tbl_city, on_delete=models.CASCADE, null=True)
    user_photo = models.FileField(upload_to="Assets/Files/User", null=True, blank=True)
    user_gender = models.CharField(max_length=100, null=True, blank=True)  
    user_bio = models.TextField(null=True, blank=True)
    user_links = models.TextField(null=True, blank=True)  # Store as JSON (GitHub, LinkedIn, etc.)

    # Educational Information
    user_degree_type = models.CharField(max_length=50, null=True, blank=True)  
    user_institution = models.CharField(max_length=100, null=True, blank=True)  
    user_field_of_study = models.CharField(max_length=100, null=True, blank=True)  
    user_graduation_month = models.IntegerField(null=True, blank=True)  # Store as month number (1-12)
    user_graduation_year = models.IntegerField(null=True, blank=True)  # Store as year (YYYY)
    
    # Emergency Contact
    user_emergency_name = models.CharField(max_length=100, null=True, blank=True)
    user_emergency_phone = models.CharField(max_length=15, null=True, blank=True)

    # Work Details
    user_organization_name = models.CharField(max_length=100, null=True, blank=True)
    user_job_title = models.CharField(max_length=100, null=True, blank=True)
    user_industry = models.CharField(max_length=100, null=True, blank=True)
    user_location = models.CharField(max_length=100, null=True, blank=True)
    user_official_address = models.CharField(max_length=200, null=True, blank=True)
    user_official_contact_number = models.CharField(max_length=15, null=True, blank=True)

    # Profile Completion Flags
    is_basic_profile_complete = models.BooleanField(default=False)  
    is_volunteer_profile_complete = models.BooleanField(default=False)
    is_organizer_profile_complete = models.BooleanField(default=False)

    # Past Volunteering Experience
    user_past_volunteering = models.TextField(null=True, blank=True) 

    # User Type & Roles and Visibility
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='volunteer')
    user_visibility = models.BooleanField(default=False)  # If true, profile is public and visible to anyone

    @property
    def is_public_organizer(self):
        return self.user_type == 'organizer' and self.user_visibility

    # PUBLIC FIELDS for Organizer Profile:
    # user_name, user_username, user_photo, user_degree_type, user_institution, user_field_of_study, user_graduation_month, user_graduation_year, user_email, user_contact, user_job_title, user_organization_name, user_location, user_bio, user_links



