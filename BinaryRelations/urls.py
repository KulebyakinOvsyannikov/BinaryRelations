from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'BinaryRelations.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^student_site/', include('StudentSite.urls', namespace='student_site')),
    url(r'^admin/', include(admin.site.urls)),
]
