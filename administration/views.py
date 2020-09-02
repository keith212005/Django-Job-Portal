from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django_datatables_view.base_datatable_view import BaseDatatableView

from companies.models import CompanyInfo
from django.core import serializers
from authentication.models import CustomUser
# from datatableview.views import DatatableView
from  administration import forms
from django.utils.html import escape
import datetime
import json as simplejson

# Create your views here.


@login_required(login_url="/login/")
def TestModelListJson(request):
  company_info = CompanyInfo.objects.select_related('account_user')
  json = serializers.serialize('json', company_info)
  for e in CompanyInfo.objects.select_related('account_user'):
    print(e.account_user)

  print(json)

  # return HttpResponse(json,content_type='application/json')
  return HttpResponse(json,   content_type='application/json')



# This method converts datetime field to json
def myconverter(o):
  if isinstance(o, datetime.datetime):
    return o.__str__()


@login_required(login_url="/login/")
def editCompany(request, pk_id, acc_id):
  # show company edit form
  companies = CompanyInfo.objects.select_related('account_user').filter(pk=pk_id)
  customuserObject = CustomUser.objects.get(id=acc_id)
  context = {'company_info': companies, 'customuser': customuserObject}
  return render(request, "administration/editcompany.html",context)

@login_required(login_url="/login/")
def activateOrDeactivate(request, id):
  # deactivate company profile
  customuserObject = CustomUser.objects.get(id=id)
  customuserObject.is_active = 1 if customuserObject.is_active == 0 else 0
  customuserObject.save()
  return redirect('showAllCompanies')



@login_required(login_url="/login/")
def showAllCompanies(request):
  return render(request,"administration/allcompanies.html")



class getAllCompaniesData(BaseDatatableView):
  model = CompanyInfo

  def get_initial_queryset(self):
    return CompanyInfo.objects.all()

  def render_column(self, row, column):
    # We want to render user as a custom column
    if column == 'user':
      # escape HTML for security reasons
      return escape('{0} {1}'.format(row.customer_firstname, row.customer_lastname))
    else:
      return super(getAllCompaniesData, self).render_column(row, column)


  def filter_queryset(self, qs):
    # use request parameters to filter queryset

    # simple example:
    search = self.request.GET.get('search[value]', None)
    if search:
      qs = qs.filter(name__istartswith=search)

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





