from django.db import models
from django.conf import settings
from django.utils import timezone
from students.models import StudentInfo


class CompanyInfo(models.Model):
  id = models.AutoField(primary_key=True)
  account_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  name = models.CharField(max_length=200, blank=True, null=True)
  description = models.TextField(blank=True, null=True)
  contactno1 = models.CharField(max_length=20, blank=True, null=True)
  contactno2 = models.CharField(max_length=20, blank=True, null=True)
  websiteurl = models.URLField(max_length=200, blank=True, null=True)
  address1 = models.TextField(blank=True, null=True)
  address2 = models.TextField(blank=True, null=True)
  city = models.CharField(max_length=100, blank=True, null=True)
  state = models.CharField(max_length=100, blank=True, null=True)
  zipcode = models.IntegerField(blank=True, null=True)
  country = models.CharField(max_length=100, blank=True, null=True)
  date_updated = models.DateTimeField(auto_now=True, blank=True, null=True)
  date_deleted = models.DateTimeField(blank=True, null=True)
  objects = models.Manager()

  class Meta:
    db_table = "company_info"


class JobPosting(models.Model):
  id = models.AutoField(primary_key=True)
  account_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  job_title = models.CharField(max_length=100, blank=True, null=True)
  job_description = models.TextField(blank=True, null=True)
  job_skills = models.TextField(blank=True, null=True)
  job_type = models.CharField(max_length=100, blank=True, null=True)
  job_city = models.CharField(max_length=100, blank=True, null=True)
  salary = models.FloatField(default=0.00, blank=True, null=True)
  is_active = models.BooleanField(default=True, blank=True, null=True)
  start_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
  end_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
  date_updated = models.DateTimeField(auto_now=True)
  date_deleted = models.DateTimeField(blank=True, null=True)
  objects = models.Manager()

  class Meta:
    db_table = "jobs"


class JobPostActivity(models.Model):
  id = models.AutoField(primary_key=True)
  job_id = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
  student_id = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
  apply_date = models.DateTimeField(default=timezone.now)
  objects = models.Manager()

  class Meta:
    db_table = "jobs_activity"


class AboutCompany(models.Model):
  id = models.AutoField(primary_key=True)
  company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, related_name='about_company')
  estd_date = models.DateTimeField(blank=True, null=True)
  total_emps = models.IntegerField(blank=True, null=True)
  about_work = models.CharField(max_length=500, blank=True, null=True)
  vision = models.CharField(max_length=500, blank=True, null=True)
  services_offered = models.CharField(max_length=500, blank=True, null=True)
  objects = models.Manager()

  class Meta:
    db_table = "about_company"
