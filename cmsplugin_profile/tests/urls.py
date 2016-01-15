from django.conf.urls import patterns, url, include
from django.contrib import admin


urlpatterns = patterns(
    'cmsplugin_profile.views',
    url(r'^cmsplugin_profile/(?P<profilegrid_id>\d+)/view_profiles/$',
        'view_profiles', name='view_profiles'),
    # We cannot register this admin url the normal way because plugin models do not have
    # registered model admins.
    url(r'^admin/cmsplugin_profile/new_profile/(?P<profile_nr>\d+)/$',
        'new_profile', name='new_profile'),
    url(r'^admin/', include(admin.site.urls)),
)
