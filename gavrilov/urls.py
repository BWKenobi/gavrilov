from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.urls import include
from django.contrib.auth import views as auth_views

from .forms import CustomPasswordResetForm, CustomSetPasswordForm

from .views import home_view, policy_view, juri_view, get_contestant_zip_view, statistic_contestant_view, statistic_contestant_add_view, statistic_invoices_view, view_contestant, move_order_view
from .views import juri_set, juri_change, juri_new
from .views import login_view, logout_view, register_view, change_password, activate
from .views import delete_juri, ajax_activate



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name = 'home'),
    path('policy', policy_view, name = 'policy'),
    path('juri', juri_view, name = 'juri_view'),
    path('get_contestant_zip/<int:pk>/', get_contestant_zip_view, name = 'get_contestant_zip'),
    path('statistic_contestant', statistic_contestant_view, name = 'statistic_contestant'),
    path('statistic_contestant_add', statistic_contestant_add_view, name = 'statistic_contestant_add'),
    path('statistic_invoices', statistic_invoices_view, name = 'statistic_invoices'),
    path('view_contestant/<int:pk>/', view_contestant, name = 'view_contestant'),
    path('move_order', move_order_view, name = 'move_order'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


urlpatterns += [
	path('login/', login_view, name = 'login'),
    path('logout/', logout_view, name = 'logout'),
    path('register/', register_view, name = 'register'),
    path('passchange/', change_password, name = 'passchange'),
]


urlpatterns += [
    path('juri-set/', juri_set, name = 'juri_set'),
    path('juri-change/<int:pk>', juri_change, name = 'juri_change'),
    path('juri-new/', juri_new, name = 'juri_new'),
]


urlpatterns += [
    path('profile/', include(('profileuser.urls', 'profiles'))),
    path('pictures/', include(('pictures.urls', 'pictures'))),
    path('movies/', include(('movies.urls', 'movies'))),
    path('nominations/', include(('nominations.urls', 'nominations'))),
    path('mailing/', include(('mailing.urls', 'mailing'))),
    path('invoices/', include(('invoices.urls', 'invoices'))),
    path('protocols/', include(('protocols.urls', 'protocols'))),
    path('ratings/', include(('ratings.urls', 'ratings'))),
    path('statements/', include(('statements.urls', 'statements'))),
    path('personals/', include(('personals.urls', 'personals'))),
    path('marks/', include(('marks.urls', 'marks'))),
    #path('certificates/', include(('certificates.urls', 'certificates'))),
]

urlpatterns += [
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(form_class = CustomPasswordResetForm), name = 'password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name = 'password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(form_class=CustomSetPasswordForm), name = 'password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_comlete.html'), name = 'password_reset_complete'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name = 'activate'),
]


urlpatterns += [
    path('ajax/delete-juri/', delete_juri, name = 'ajax_delete_juri'),
    path('ajax/activate/', ajax_activate, name = 'ajax_activate'),
]
