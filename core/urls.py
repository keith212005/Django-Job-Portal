from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include  # add this

urlpatterns = [
  path("", include("authentication.urls")),  # Auth routes - login / register
  path("", include("app.urls")),  # UI Kits Html files
  path("student/", include("students.urls")),
  path("company/", include("companies.urls")),
  path("administration/", include("administration.urls")),
  # path("administration/", include("django.contrib.auth.urls")),
  # path('administration/', administration.site.urls),  # Django administration route
  path('administration', admin.site.urls),  # Django administration route
  path('imagefit/', include('imagefit.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#         urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
  import debug_toolbar
  urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns


