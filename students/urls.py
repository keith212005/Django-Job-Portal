from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth.views import LogoutView
from students.views import showStudentProfile, updateProfile, addQualification, getAlleducationList, \
  showAllQualifications, editEducationdata, updateSingleQualification, getSingleQualification

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path('profile/', showStudentProfile, name='showStudentProfile'),
path('updateProfile/', updateProfile, name='updateProfile'),
path('getAlleducationList/', login_required(getAlleducationList.as_view()), name="getAlleducationList"),
#path('education/', showEducation, name='showEducation'),

path('showAllQualifications/', showAllQualifications, name='showAllQualifications'),

path('addQualification/', addQualification, name='addQualification'),


path('getSingleQualification/', getSingleQualification, name='getSingleQualification'),

path('editEducationdata/', editEducationdata, name="editEducationdata"),
path('updateSingleQualification/', updateSingleQualification, name="updateSingleQualification"),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
