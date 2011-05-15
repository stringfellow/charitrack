from django.conf.urls.defaults import *

from idios.urls import urlpatterns

from profiles import views

urlpatterns += patterns("",

    url(r"me/", views.profile_home, name="profile_home"),

)

