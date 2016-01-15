from django.contrib.auth.models import Group, Permission
from django.core.urlresolvers import reverse

from filer.models import Image
from cms.test_utils.testcases import CMSTestCase
from cms.models import Placeholder
from cms.api import create_page

from cmsplugin_profile.models import (
    ProfileGrid, Profile, ProfilePromoGrid, SelectedProfile
)


class ProfileGridTest(CMSTestCase):

    def _create_image(self, title="test_image"):
        return Image.objects.create(title=title)

    def _create_placeholder_with_page(self):
        page = create_page("copy destination page", "cms/dummy.html",
                           "en", published=True, in_navigation=False)
        placeholder = Placeholder.objects.create()
        page.placeholders.add(placeholder)
        page.save()
        return placeholder

    def _create_profilegrid(self, placeholder, profile_nr=1):
        grid = ProfileGrid.objects.create(description="grid", plugin_type="ProfileGridPlugin",
                                          language='en', placeholder=placeholder)
        img = self._create_image()
        for _ in range(profile_nr):
            Profile.objects.create(
                thumbnail_image=img, detail_image=img, profile_plugin=grid
            )
        return grid

    def test_get_new_profile(self):
        admin = self.get_superuser()
        profile_index = 11
        grid_id = 0
        with self.login_user_context(admin):
            response = self.client.get(
                reverse('new_profile', args=[profile_index]),
                {'profilegrid_id': grid_id}
            )
        assert response.status_code == 200
        assert 'id="profile_set-{}"'.format(profile_index) in response.content

    def test_get_new_profile_admin_no_rights(self):
        admin_no_rights = self.get_staff_user_with_no_permissions()
        profile_index = 11
        grid_id = 0
        with self.login_user_context(admin_no_rights):
            response = self.client.get(
                reverse('new_profile', args=[profile_index]),
                {'profilegrid_id': grid_id}
            )
        assert response.status_code == 403

    def test_get_new_profile_admin_rights(self):
        admin = self.get_staff_user_with_no_permissions()
        profile_index = 11
        grid_id = 0
        group = Group.objects.create(name="editor")
        group.user_set.add(admin)
        group.permissions.add(Permission.objects.get(name="Can change profile grid"))
        group.save()
        with self.login_user_context(admin):
            response = self.client.get(
                reverse('new_profile', args=[profile_index]),
                {'profilegrid_id': grid_id}
            )
        assert response.status_code == 200
        assert 'id="profile_set-{}"'.format(profile_index) in response.content

    def test_copy_grid(self):
        admin = self.get_superuser()
        placeholder = self._create_placeholder_with_page()
        self._create_profilegrid(placeholder, profile_nr=1)

        self.assertEqual(ProfileGrid.objects.all().count(), 1)
        self.assertEqual(Profile.objects.all().count(), 1)

        with self.login_user_context(admin):
            url = reverse('admin:cms_page_copy_plugins')
            data = dict(placeholder=placeholder.pk,
                        language='fr',
                        copy_from='en')
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 200)

        self.assertEqual(ProfileGrid.objects.all().count(), 2)
        self.assertEqual(Profile.objects.all().count(), 2)

        old_profile, new_profile = Profile.objects.all()
        self.assertEqual(old_profile.detail_image, new_profile.detail_image)
        self.assertEqual(old_profile.thumbnail_image.image, new_profile.thumbnail_image)

    def test_copy_grid_promo(self):
        admin = self.get_superuser()
        placeholder = self._create_placeholder_with_page()
        grid = self._create_profilegrid(placeholder, profile_nr=2)
        grid_promo = ProfilePromoGrid.objects.create(
            profile_plugin=grid, placeholder=placeholder, language='en',
            plugin_type="ProfileGridPromoPlugin"
        )

        SelectedProfile.objects.create(
            profile=Profile.objects.all()[0],
            promo_grid=grid_promo
        )

        self.assertEqual(ProfileGrid.objects.all().count(), 1)
        self.assertEqual(Profile.objects.all().count(), 2)
        self.assertEqual(ProfilePromoGrid.objects.all().count(), 1)
        self.assertEqual(SelectedProfile.objects.all().count(), 1)

        with self.login_user_context(admin):
            url = reverse('admin:cms_page_copy_plugins')
            data = dict(placeholder=placeholder.pk,
                        language='fr',
                        copy_from='en')
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 200)

        self.assertEqual(ProfileGrid.objects.all().count(), 2)
        self.assertEqual(Profile.objects.all().count(), 4)
        self.assertEqual(ProfilePromoGrid.objects.all().count(), 2)
        self.assertEqual(SelectedProfile.objects.all().count(), 2)

        old_promo_grid, new_promo_grid = ProfilePromoGrid.objects.all()
        old_sel_profile, new_sel_profile = SelectedProfile.objects.all()
        self.assertEqual(old_sel_profile.profile, new_sel_profile.profile)
        self.assertEqual(old_sel_profile.promo_grid, old_promo_grid)
        self.assertEqual(new_sel_profile.promo_grid, new_promo_grid)
