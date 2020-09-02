from glob import escape
# import wikipedia
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.html import escape
from django_datatables_view.base_datatable_view import BaseDatatableView
import json as simplejson

from authentication.models import CustomUser
from students.models import StudentInfo, Qualifications
from django.forms.models import model_to_dict


# Create your views here.
@login_required(login_url="/login/")
def showStudentProfile(request):
  student_info = StudentInfo.objects.get(account_user=request.user.id)
  print(student_info)
  context = {'student_info': student_info}

  return render(request, 'students/page-user.html', context)


# ducation list

class getAlleducationList(BaseDatatableView):
  model = Qualifications

  def render_column(self, row, column):
    # We want to render user as a custom column
    if column == 'user':
      # escape HTML for security reasons
      return escape('{0} {1}'.format(row.customer_firstname, row.customer_lastname))
    else:
      return super(getAlleducationList, self).render_column(row, column)

  def filter_queryset(self, qs):
    # use request parameters to filter queryset

    # simple example:
    search = self.request.GET.get('search[value]', None)
    if search:
      qs = qs.filter(degree_name__istartswith=search)

    # more advanced example
    filter_customer = self.request.GET.get('customer', None)

    if filter_customer:
      customer_parts = filter_customer.split(' ')
      qs_params = None
      for part in customer_parts:
        q = Q(customer_firstname__istartswith=part) | Q(customer_lastname__istartswith=part)
        qs_params = qs_params | q if qs_params else q
      qs = qs.filter(qs_params)
    return qs


def showAllQualifications(request):
  qualifications_list = Qualifications.objects.filter(account_user_id=request.user.id)
  context = {'qualification_list': qualifications_list}
  return render(request, "students/educationlist.html", context)


# Student Profile Data Update
@login_required(login_url="/login/")
def updateProfile(request):
  if request.method == 'POST':
    studentObject = StudentInfo.objects.get(account_user_id=request.user.id)
    studentObject.fname = request.POST.get('fname')
    studentObject.lname = request.POST.get('lname')
    studentObject.contact = request.POST.get('contact')
    studentObject.address1 = request.POST.get('address1')
    studentObject.address2 = request.POST.get('address2')
    studentObject.city = request.POST.get('city')
    studentObject.state = request.POST.get('state')
    studentObject.country = request.POST.get('country')
    # studentObject.cus = myfile.name
    studentObject.dob = request.POST.get('dob')
    studentObject.skills = request.POST.get('skills')
    studentObject.description = request.POST.get('description')
    studentObject.zipcode = request.POST.get('zipcode')
    studentObject.upload_cv = request.POST.get('upload_cv')
    studentObject.save()

    if(request.FILES.get('file_pic')):
      myfile = request.FILES['file_pic']
      fs = FileSystemStorage()
      filename = fs.save(myfile.name, myfile)
      uploaded_file_url = fs.url(filename)
      obj = CustomUser.objects.get(pk=request.user.id)
      obj.pic = myfile.name
      obj.save()

    msg = 'Your Data Updated Successfully'
    context = {'msg': msg, 'student_info': studentObject }
    return render(request, 'students/page-user.html', context)


# Education Data Add
def addQualification(request):
  print('savedetails')
  if request.method == 'POST':
    studentEduObject = Qualifications()
    studentEduObject.account_user_id = request.user.id
    studentEduObject.degree_name = request.POST.get('degree_name')
    studentEduObject.description = request.POST.get('description')
    studentEduObject.institute_name = request.POST.get('institute_name')
    studentEduObject.start_year = request.POST.get('start_year ')
    studentEduObject.end_year = request.POST.get('end_year')
    studentEduObject.percentage = request.POST.get('percentage')
    studentEduObject.save()
    msg = 'Your Education Data Saveed Successfully'
    context = {'msg': msg, 'studenteducationdata': studentEduObject}
    return redirect('showAllQualifications')


# Education Data Edit
def editEducationdata(request, **kwargs):
  editeducationdata = Qualifications.objects.filter(account_user_id=request.user.id)
  context = {'editeducationdata': editeducationdata}
  return render(request, "students/educationlist.html", context)


# Update Education Data
@login_required(login_url="/login/")
def updateSingleQualification(request):
  editeducationdata = Qualifications.objects.get(id__exact=request.POST.get('edit_modal_id'))
  editeducationdata.degree_name = request.POST.get('edit_modal_degree_name')
  editeducationdata.institute_name = request.POST.get('edit_modal_institute_name')
  editeducationdata.start_year = request.POST.get('edit_modal_start_year')
  editeducationdata.end_year = request.POST.get('edit_modal_end_year')
  editeducationdata.percentage = request.POST.get('edit_modal_percentage')
  editeducationdata.description = request.POST.get('edit_modal_description')
  editeducationdata.save()
  # msg = 'Successfully Edited '
  # context = {'editeducationdata': editeducationdata, 'msg': msg}
  # return render(request, 'students/educationlist.html', context)
  return redirect('showAllQualifications')


def getSingleQualification(request):
  print('ketan')
  print(request.GET.get('ids'))

  queryset = Qualifications.objects.filter(id=request.GET.get('ids'))
  # alert_list = alert.objects.all()

  tmpJson = serializers.serialize("json", queryset)
  tmpObj = simplejson.loads(tmpJson)
  x = simplejson.dumps(tmpObj)
  print(x)

  return HttpResponse(x)
  # return JsonResponse(model_to_dict(queryset))
