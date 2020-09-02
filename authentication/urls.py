from django.urls import path
from .views import login_view, register_user, studentDashboard, companyDashboard, adminDashboard
from django.contrib.auth.views import LogoutView

urlpatterns = [

  path('login/', login_view, name="login"),
  path('register/', register_user, name="register"),
  path("logout/", LogoutView.as_view(), name="logout"),

  path('administration/dashboard/', adminDashboard, name='adminDashboard'),
  path('students/dashboard/', studentDashboard, name='studentDashboard'),
  path('company/dashboard/', companyDashboard, name='companyDashboard'),


]
