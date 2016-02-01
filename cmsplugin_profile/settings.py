from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

STATIC_URL = getattr(settings, 'STATIC_URL')
MAX_PROFILE_LINKS = getattr(settings, 'CMSPLUGIN_PROFILE_NR_LINKS', 4)
# The maximum number of profiles that should be initially displayed in a Profile Grid.
INITIAL_DISPLAYED_PROFILES = getattr(settings, 'CMSPLUGIN_PROFILE_INITIAL_DISPLAYED_PROFILES', 12)
# The maximum number of profiles that can be selected for Profile Grid Promo.
MAX_PROMO_PROFILES = getattr(settings, 'CMSPLUGIN_PROFILE_MAX_PROMO_PROFILES', 4)
# The minimum number of profiles that can be selected for Profile Grid Promo.
MIN_PROMO_PROFILES = getattr(settings, 'CMSPLUGIN_PROFILE_MIN_PROMO_PROFILES', 3)
# The minimum profiles that can remain in Profile Grid Promos after Profile Grid
# delete operations
HARD_MIN_PROMO_PROFILES = getattr(settings, 'CMSPLUGIN_PROFILE_HARD_MIN_PROMO_PROFILES', 3)

if MIN_PROMO_PROFILES > MAX_PROMO_PROFILES:
    raise ImproperlyConfigured("MIN_PROMO_PROFILES cannot be bigger than MAX_PROMO_PROFILES!")

if HARD_MIN_PROMO_PROFILES > MIN_PROMO_PROFILES:
    raise ImproperlyConfigured("HARD_MIN_PROMO_PROFILES cannot be bigger than MIN_PROMO_PROFILES!")
