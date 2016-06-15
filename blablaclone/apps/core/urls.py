from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from core.views import *

from core.api import router

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls, namespace='api')),
    url("^login/$", login, name="login"),
    url("^register/$", register, name="register"),
    url(
        r'^ride/(?P<slug>[a-zA-Z-_0-9]+)/$',
        RideDetailView.as_view(),
        name="ride-detail"
    ),
    url(
        r'^ride/(?P<slug>.*)/update/$',
        RideUpdateView.as_view(),
        name="ride-update"
    ),

    url(
        r'^ride-create/$',
        RideCreateView.as_view(),
        name="ride-create"
    ),
    url(
        r'^ride/(?P<slug>[a-zA-Z-_0-9]+)/delete/$',
        RideDeleteView.as_view(),
        name="ride-delete"
    ),

    url(
        r'^ride-list/$',
        RideListView.as_view(),
        name="ride-list"
    ),
    url(
        r'^user/me/update/$',
        UserUpdateView.as_view(),
        name="user-update"
    ),

    url(
        r'^user/(?P<slug>[a-zA-Z-_0-9]+)/$',
        UserDetailView.as_view(),
        name="user-detail"
    ),
    url(
        r'^riderequest-create/(?P<ride>.*)/$',
        RideRequestCreateView.as_view(),
        name="riderequest-create"
    ),
)
