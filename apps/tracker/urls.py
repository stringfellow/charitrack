from django.conf.urls.defaults import *


urlpatterns = patterns("",

    url(r"^charities/$", 'tracker.views.charities', name="charities"),
    url(
        r"^charity/(?P<charity_name>[^/]+)/$",
        'tracker.views.charity',
        name="charity"
    ),
    url(
        r"^charity/(?P<charity_name>[^/]+)/donate/$",
        'tracker.views.charity_make_donation',
        name="charity_make_donation"
    ),
    url(
        r"^charity/(?P<charity_pk>[^/]+)/update_tags/$",
        'tracker.views.charity_update_tags',
        name="charity_update_tags"
    ),
    url(
        r"^charity/tag/(?P<tag_name>[^/]+)/user/(?P<user_name>[^/]+)/$",
        'tracker.views.charities_tag_user',
        name="charities_tag_user"
    ),
    url(r"^pledgers/$", 'tracker.views.pledgers', name="pledgers"),
    url(
        r"^pledger/(?P<pledger_name>[^/]+)/$",
        'tracker.views.pledger',
        name="pledger"
    ),
    url(
        r"^donation/(?P<donation_pk>[^/]+)/duplicate/$",
        'tracker.views.duplicate_donation',
        name="duplicate_donation"
    ),

)