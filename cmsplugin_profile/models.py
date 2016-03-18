from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from filer.fields.image import FilerImageField


LOAD_MORE_BUTTON = "load_mode_button"
LOAD_MORE_SCROLL = "load_mode_scroll"
GRID_LOADING_TYPE_CHOICES = (
    (LOAD_MORE_BUTTON, _("Load more button")),
    (LOAD_MORE_SCROLL, _("Lazy loading")),
)


class ProfileGrid(CMSPlugin):
    title = models.CharField(max_length=60)
    description = models.TextField(null=True, blank=True, max_length=400, default="")
    show_title_on_thumbnails = models.BooleanField(default=False)
    load_mode_type = models.CharField(
        _("Pagination type"), max_length=20,
        choices=GRID_LOADING_TYPE_CHOICES,
        help_text=_("There are two options for pagination type. "
                    "The <strong>Load More Button</strong> will enable loading of more "
                    "profiles entries when a user clicks on the Load More "
                    "button. Best for pages where there are multiple "
                    "components in the page content area. "
                    "<strong>Lazy Loading</strong> will enable the page to automatically "
                    "load more profiles as the user scrolls down the page. "
                    "Best for pages where this grid is the only component in "
                    "the page content area."),
        default=GRID_LOADING_TYPE_CHOICES[0])

    class Meta:
        db_table = 'cmsplugin_profilegrid'

    def __unicode__(self):
        return u'{}'.format(self.title)

    def post_copy(self, old_instance, new_old_ziplist):
        """
        Custom actions that must be performed for copied ProfileGrid plugins:
        - copy profiles
        """

        # old_instance.profilegrid will point to self
        old_profile_grid = ProfileGrid.objects.get(id=old_instance.id)

        for profile in old_profile_grid.profile_set.all():
            profile.id = None
            profile.profile_plugin = self
            profile.save()

    def get_warning_on_delete(self):
        promos = self.profilepromogrid_set.all()
        if not promos:
            return None
        return "Deleting this Profile Grid will also delete the Promo Grid(s): {}".format(
            ", ".join([promo.short_info for promo in promos])
        )


class Profile(models.Model):
    profile_plugin = models.ForeignKey(ProfileGrid, null=False, blank=False)
    title = models.CharField(null=True, blank=True, max_length=60)
    description = models.TextField(max_length=395)
    call_to_action_text = models.CharField(null=True, blank=True, max_length=30)
    call_to_action_url = models.CharField(null=True, blank=True, max_length=200)
    additional_links_label = models.CharField(null=True, blank=True, max_length=30, default="")
    thumbnail_image = FilerImageField(
        on_delete=models.PROTECT,
        default=None, help_text=_('Image must be 1:1 aspect ratio. We recommend 440px min size.'),
        verbose_name=_("Thumbnail Image"),
        related_name="profile_thumbnail"
    )
    detail_image = FilerImageField(
        on_delete=models.PROTECT,
        default=None, help_text=_('Image must be 1:1 aspect ratio. We recommend 600px min size.'),
        verbose_name=_("Detail Image"),
        related_name="profile_detail"
    )
    image_credit = models.CharField(null=True, blank=True, max_length=40)

    class Meta:
        order_with_respect_to = 'profile_plugin'

    def __unicode__(self):
        return u'{}'.format(self.title)

    @property
    def links(self):
        return self.profilelink_set.all()


class ProfileLink(models.Model):
    profile = models.ForeignKey(Profile, null=False, blank=False)
    text = models.CharField(null=True, blank=True, max_length=60)
    url = models.CharField(null=True, blank=True, max_length=200)
    target = models.CharField(null=True, blank=True, max_length=50)


class ProfilePromoGrid(CMSPlugin):
    profile_plugin = models.ForeignKey(ProfileGrid, null=False, blank=False)
    selected_profiles = models.ManyToManyField(
        Profile, through="SelectedProfile", through_fields=('promo_grid', 'profile')
    )
    title = models.CharField(null=True, blank=True, max_length=60)
    call_to_action_text = models.CharField(max_length=100)

    class Meta:
        db_table = 'cmsplugin_profilepromogrid'

    def __unicode__(self):
        return u'{}'.format(self.title)

    def save(self, *args, **kwargs):
        ret_value = super(ProfilePromoGrid, self).save(*args, **kwargs)
        self._save_selected_profiles()
        return ret_value

    def _save_selected_profiles(self):
        if not hasattr(self, 'unsaved_selected_profiles'):
            return
        self.selectedprofile_set.all().delete()
        for unsaved_selected_profile in self.unsaved_selected_profiles:
            unsaved_selected_profile.promo_grid = self
            unsaved_selected_profile.save()

    def post_copy(self, old_instance, new_old_ziplist):
        """
        Custom actions that must be performed for copied ProfilePromoGrid plugins:
        - copy profile selection
        """

        # old_instance.profilepromogrid will point to self
        old_profile_promo_grid = ProfilePromoGrid.objects.get(id=old_instance.id)

        for selected_profile in old_profile_promo_grid.selectedprofile_set.all():
            selected_profile.id = None
            selected_profile.promo_grid = self
            selected_profile.save()

    @property
    def short_info(self):
        if self.title:
            return self.title
        elif len(self.call_to_action_text) > 10:
            return u'Call to action:"{}.."'.format(self.call_to_action_text[:10])
        else:
            return self.call_to_action_text


class SelectedProfile(models.Model):
    profile = models.ForeignKey(Profile, null=False, blank=False)
    promo_grid = models.ForeignKey(ProfilePromoGrid, null=False, blank=False)
