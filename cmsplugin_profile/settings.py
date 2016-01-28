from django.conf import settings

STATIC_URL = getattr(settings, 'STATIC_URL')
MAX_PROFILE_LINKS = getattr(settings, 'CMSPLUGIN_PROFILE_NR_LINKS', 4)
# The maximum number of profiles that should be initially displayed in a Profile Grid.
INITIAL_DISPLAYED_PROFILES = getattr(settings, 'CMSPLUGIN_PROFILE_INITIAL_DISPLAYED_PROFILES', 12)
# The maximum number of profiles that can be selected for Profile Grid Promo.
MAX_PROMO_PROFILES = getattr(settings, 'CMSPLUGIN_PROFILE_MAX_PROMO_PROFILES', 4)
# The minimum number of profiles that can be selected for Profile Grid Promo.
MIN_PROMO_PROFILES = getattr(settings, 'CMSPLUGIN_PROFILE_MAX_PROMO_PROFILES', 3)
