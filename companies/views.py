from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_POST
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from authentication.models import CustomUser
from companies.models import CompanyInfo, JobPosting, AboutCompany
from django.core import serializers
from PIL import Image
import urllib.request
import json

# Create your views here.

@login_required(login_url="/login/")
def showAllJobListings(request):
  jobs = JobPosting.objects.all()
  json = serializers.serialize('json', jobs)
  print(json)
  context = {'jobs': jobs}
  return render(request, "companies/alljobslist.html", context)


# @login_required(login_url="/login/")
# def createNewJobForm(request):
#   return render(request, "companies/createnewjobposting.html")


def editCompanyProfile(request, **kwargs):
  company = CompanyInfo.objects.get(account_user_id=request.user.id)

  url_eng = "https://programming-quotes-api.herokuapp.com/quotes/random";
  # url_sr = "https://programming-quotes-api.herokuapp.com/quotes/random/lang/sr";
  openurlen = urllib.request.urlopen(url_eng);
  dataen = openurlen.read();
  jsonDataen = json.loads(dataen);
  print(jsonDataen);

  context = {'company': company, 'jsonData': jsonDataen}
  return render(request, "companies/editprofile.html", context)


@login_required(login_url="/login/")
def updateCompanyInfo(request):
  if request.method == 'POST':

    company = CompanyInfo.objects.get(account_user_id=request.user.id)
    company.name = request.POST.get('name')
    company.description = request.POST.get('description')
    company.websiteurl = request.POST.get('websiteurl')
    company.contactno1 = request.POST.get('contact1')
    company.contactno2 = request.POST.get('contact2')
    company.address1 = request.POST.get('address1')
    company.address2 = request.POST.get('address2')
    company.city = request.POST.get('city')
    company.state = request.POST.get('state')
    company.zipcode = request.POST.get('zipcode')
    company.country = request.POST.get('country')
    company.save();

    if (request.FILES.get('pic')):
      myfile = request.FILES['pic']
      fs = FileSystemStorage()
      filename = fs.save( str(request.user.id) +"_"+ myfile.name, myfile)
      # uploaded_file_url = fs.url(filename)
      obj = CustomUser.objects.get(pk=request.user.id)
      obj.pic = str(request.user.id) +"_"+ myfile.name
      obj.save()

    msg = 'Success'
    context = {'company': company, 'msg': msg}
    return render(request, 'companies/editprofile.html', context)


class getAllJobsList(BaseDatatableView):
  model = JobPosting

  # def render_column(self, row, column):
  #   # We want to render user as a custom column
  #   if column == 'user':
  #     # escape HTML for security reasons
  #     return escape('{0} {1}'.format(row.customer_firstname, row.customer_lastname))
  #   else:
  #     return super(getAllJobsList, self).render_column(row, column)

  def filter_queryset(self, qs):
    # use request parameters to filter queryset

    # simple example:
    search = self.request.GET.get('search[value]', None)
    if search:
      # qs = qs.filter(job_title__istartswith=search)
      qs = qs.filter(job_title__icontains=search)

    # more advanced example
    # filter_customer = self.request.GET.get('customer', None)
    #
    # if filter_customer:
    #   customer_parts = filter_customer.split(' ')
    #   qs_params = None
    #   for part in customer_parts:
    #     q = Q(customer_firstname__istartswith=part) | Q(customer_lastname__istartswith=part)
    #     qs_params = qs_params | q if qs_params else q
    #   qs = qs.filter(qs_params)
    return qs


@login_required(login_url="/login/")
def addJob(request):
  return render(request, "companies/registerjob.html")


@login_required(login_url="/login/")
def editJob(request, id):
  obj = JobPosting.objects.get(id=id)
  context = {'obj': obj}
  return render(request, "companies/registerjob.html", context)


@login_required(login_url="/login/")
def updateJob(request, id):
  print('updating...')
  obj = JobPosting.objects.get(id=id)
  obj.account_user_id = request.user.id
  obj.job_title = request.POST.get('job_title')
  obj.job_description = request.POST.get('job_description')
  obj.job_skills = request.POST.get('job_skills')
  obj.job_type = request.POST.get('job_type')
  obj.job_city = request.POST.get('job_city')
  obj.salary = request.POST.get('job_salary')
  obj.is_active = request.POST.get('is_active')
  if obj.is_active == 'on':
    obj.is_active = True
  else:
    obj.is_active = False

  obj.start_date = request.POST.get('start_date')
  obj.end_date = request.POST.get('end_date')
  obj.save()
  context = {'msg': 'Success'}
  return render(request, 'companies/alljobslist.html', context)


@login_required(login_url="/login/")
def saveJob(request):
  print('saveJob...')
  if request.method == 'POST':
    JobPosting.objects.updateJobList(request)
    obj = JobPosting()
    obj.account_user_id = request.user.id
    obj.job_title = request.POST.get('job_title')
    obj.job_description = request.POST.get('job_description')
    obj.job_skills = request.POST.get('job_skills')
    obj.job_type = request.POST.get('job_type')
    obj.job_city = request.POST.get('job_city')
    obj.salary = request.POST.get('salary')
    obj.is_active = request.POST.get('is_active')
    if obj.is_active == 'on':
      obj.is_active = True
    else:
      obj.is_active = False
    obj.save()
  context = {'msg': 'saved'}
  return render(request, 'companies/alljobslist.html', context)


@login_required(login_url="/login/")
def showAboutCompany(request):
  queryset = AboutCompany.objects.get(company__account_user_id=request.user.id)
  v1 = queryset.values()
  print(v1)
  context = {'obj': queryset}
  return render(request, "companies/aboutcompany.html", context)
