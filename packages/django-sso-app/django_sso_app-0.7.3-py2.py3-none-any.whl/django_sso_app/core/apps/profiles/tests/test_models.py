# profile filed update updates rev

from django.contrib.auth import get_user_model

from django_sso_app.backend.tests.factories import UserTestCase

User = get_user_model()


class ProfileTestCase(UserTestCase):

    def test_profile_field_update_updates_rev(self):
        """
        User update updates user revision
        """

        profile_rev = self.profile.sso_rev

        self.profile.country = 'IT'
        self.profile.save()

        self.profile.refresh_from_db()

        self.assertEqual(self.profile.sso_rev, profile_rev + 1)

    def test_django_user_email_update_updates_profile_django_user_email(self):
        profile_rev = self.profile.sso_rev

        self.assertEqual(self.user.email, self.profile.django_user_email)

        self.user.email = 'new_email@example.com'
        self.user.save()

        self.assertEqual(self.profile.django_user_email, 'new_email@example.com')

        self.assertEqual(self.profile.sso_rev, profile_rev + 1)

    def test_django_user_username_update_updates_profile_django_user_username(self):
        profile_rev = self.profile.sso_rev

        self.assertEqual(self.user.username, self.profile.django_user_username)

        self.user.username = 'new_username'
        self.user.save()

        self.assertEqual(self.profile.django_user_username, 'new_username')

        self.assertEqual(self.profile.sso_rev, profile_rev + 1)
