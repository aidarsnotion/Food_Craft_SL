from django.conf.urls.static import static
from django.utils.translation import gettext_lazy as _
from django.conf.urls import handler400, handler403, handler404, handler500
from main import AdminViews
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.urls import path, include, re_path
from main.models import CustomUser

urlpatterns = i18n_patterns(
    path(_('admin/'), AdminViews.AdminMain.as_view()),
    path('rosetta/', include('rosetta.urls')),
    path("", include("main.urls")),
    path("mobile/", include("mobile.urls")),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler400 = 'main.views.error_400'
handler404 = 'main.views.error_404'
handler403 = 'main.views.error_403'
handler500 = 'main.views.error_500'
