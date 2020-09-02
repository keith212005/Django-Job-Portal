from django.db import models
from django.conf import settings


class Qualifications(models.Model):
  id = models.AutoField(primary_key=True)
  account_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  degree_name = models.CharField(max_length=100,  blank=True, null=True)
  description = models.TextField(blank=True, null=True)
  institute_name = models.CharField(max_length=100)
  start_year = models.DateField(verbose_name='start date', auto_now_add=True)
  end_year = models.DateField(verbose_name='end date', auto_now_add=True)
  percentage = models.FloatField()
  objects = models.Manager()

  class Meta:
    db_table = "qualifications"


class StudentInfo(models.Model):
  id = models.AutoField(primary_key=True)
  account_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  fname = models.CharField(max_length=200, blank=True, null=True)
  lname = models.CharField(max_length=200, blank=True, null=True)
  # pic = models.ImageField(upload_to='images/', blank=True, null=True)
  upload_cv = models.FileField(upload_to='uploads/files/', blank=True, null=True)
  description = models.TextField(blank=True, null=True)
  skills = models.TextField(blank=True, null=True)
  contact = models.CharField(max_length=20, blank=True, null=True)
  gender = models.NullBooleanField(blank=True, null=True)
  dob = models.DateField(blank=True, null=True)
  address1 = models.TextField(blank=True, null=True)
  address2 = models.TextField(blank=True, null=True)
  city = models.CharField(max_length=50, blank=True, null=True)
  state = models.CharField(max_length=50, blank=True, null=True)
  zipcode = models.IntegerField(blank=True, null=True)
  country = models.CharField(max_length=100, blank=True, null=True)
  date_updated = models.DateTimeField(auto_now_add=True)
  date_deleted = models.DateTimeField(blank=True, null=True)
  objects = models.Manager()

  class Meta:
    db_table = "student_info"
