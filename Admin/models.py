from django.db import models

# Create your models here.
class tbl_district(models.Model):
    district_name = models.CharField(max_length = 30)

class tbl_place(models.Model):
    place_name=models.CharField(max_length=30)
    district=models.ForeignKey(tbl_district,on_delete=models.CASCADE)

class tbl_category(models.Model):
    category_name=models.CharField(max_length=30) 

class tbl_subcategory(models.Model):
    subcategory_name=models.CharField(max_length=30)
    category=models.ForeignKey(tbl_category,on_delete=models.CASCADE)

class tbl_admin(models.Model):
    admin_name=models.CharField(max_length=30)
    admin_email=models.CharField(max_length=50)
    admin_password=models.CharField(max_length=30)

class tbl_type(models.Model):
    type_name=models.CharField(max_length=30)
    
class tbl_country(models.Model):
    country_code=models.CharField(max_length=10)
    country_name=models.CharField(max_length=50)
    country_phone_code=models.IntegerField()

class tbl_state(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(tbl_country, on_delete=models.CASCADE)

class tbl_city(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(tbl_state, on_delete=models.CASCADE)


