"""
URL configuration for school project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.users.urls")),
    path("students/", include("apps.students.urls")),
    path("teachers/", include("apps.teachers.urls")),
    path("academics/", include("apps.academics.urls")),
    path("finance/", include("apps.finance.urls")),
    path("communication/", include("apps.communication.urls")),
    path("settings/", include("apps.settings.urls")),
    path("library/", include("apps.library.urls")),
    path("transport/", include("apps.transport.urls")),
    path("dormitory/", include("apps.dormitory.urls")),
    path("homework/", include("apps.homework.urls")),
    path("leaves/", include("apps.leaves.urls")),
    path("frontdesk/", include("apps.frontdesk.urls")),
    path("api/", include("apps.users.api_urls")),
    path("api/students/", include("apps.students.api_urls")),
    path("api/teachers/", include("apps.teachers.api_urls")),
    path("api/academics/", include("apps.academics.api_urls")),
    path("api/finance/", include("apps.finance.api_urls")),
    path("api/communication/", include("apps.communication.api_urls")),
    path("api/settings/", include("apps.settings.api_urls")),
    path("api/library/", include("apps.library.api_urls")),
    path("api/transport/", include("apps.transport.api_urls")),
    path("api/dormitory/", include("apps.dormitory.api_urls")),
    path("api/homework/", include("apps.homework.api_urls")),
    path("api/leaves/", include("apps.leaves.api_urls")),
    path("api/frontdesk/", include("apps.frontdesk.api_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
