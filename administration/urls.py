from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import showAllCompanies, TestModelListJson, editCompany, activateOrDeactivate, getAllCompaniesData
from django.views.generic.base import View

urlpatterns = [

  path('showAllCompanies/', showAllCompanies, name="showAllCompanies"),
  path('getAllCompaniesData/', login_required(getAllCompaniesData.as_view()), name="getAllCompaniesData"),
  path('testmodel_list_json/', TestModelListJson, name="testmodel_list_json"),
  path('editCompany/<int:pk_id>/<int:acc_id>', editCompany, name="editCompany"),
  path('activateOrDeactivate/<int:id>', activateOrDeactivate, name="activateOrDeactivate"),


]
