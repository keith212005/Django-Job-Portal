from django.contrib.auth.decorators import login_required
from django.urls import path, include  # add this
from django.conf import settings
from django.conf.urls.static import static

from companies.views import showAllJobListings, editCompanyProfile, getAllJobsList, addJob, saveJob, editJob, updateJob, \
  updateCompanyInfo, showAboutCompany

urlpatterns = [
  path('showAllJobListings/', showAllJobListings, name="showAllJobListings"),
  path('getAllJobsList/', login_required(getAllJobsList.as_view()), name="getAllJobsList"),
  path('editCompanyProfile/', editCompanyProfile, name="editCompanyProfile"),
  path('updateCompanyInfo/', updateCompanyInfo, name="updateCompanyInfo"),
  path('addJob/', addJob, name="addJob"),
  path('saveJob/', saveJob, name="saveJob"),
  path('editJob/<int:id>', editJob, name="editJob"),
  path('updateJob/<int:id>', updateJob, name="updateJob"),
  path('showAboutCompany/', showAboutCompany, name="showAboutCompany"),
]



