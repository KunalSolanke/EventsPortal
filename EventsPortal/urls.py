from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path,include
from django.views.generic import RedirectView


urlpatterns = [
    path("",RedirectView.as_view(url="/accounts/profile"),name="profile_page"),
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('events/',include('events.urls')),
]
urlpatterns += static(settings.MEDIA_URL,
                     document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)

