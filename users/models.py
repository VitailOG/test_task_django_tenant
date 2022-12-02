from django.utils.timezone import now
from tenant_users.tenants.models import DeleteError, UserProfileManager, SchemaError, ExistsError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.db import connection, models
from django.utils.translation import gettext_lazy as _
from django_tenants.utils import get_public_schema_name

from tenant_users.permissions.models import PermissionsMixinFacade


class CustomUserProfileManager(UserProfileManager):
    def _create_user(
        self,
        email,
        password,
        is_staff,
        is_superuser,
        is_verified,
        **extra_fields,
    ):
        # Do some schema validation to protect against calling create user from
        # inside a tenant. Must create public tenant permissions during user
        # creation. This happens during assign role. This function cannot be
        # used until a public schema already exists
        UserModel = get_user_model()

        if connection.schema_name != get_public_schema_name():
            raise SchemaError(
                'Schema must be public for UserProfileManager user creation',
            )

        if not email:
            raise ValueError('Users must have an email address.')

        email = self.normalize_email(email)

        profile = UserModel.objects.filter(email=email).first()
        if profile and profile.is_active:
            raise ExistsError('User already exists!')

        # Profile might exist but not be active. If a profile does exist
        # all previous history logs will still be associated with the user,
        # but will not be accessible because the user won't be linked to
        # any tenants from the user's previous membership. There are two
        # exceptions to this. 1) The user gets re-invited to a tenant it
        # previously had access to (this is good thing IMO). 2) The public
        # schema if they had previous activity associated would be available
        if not profile:
            profile = UserModel()

        profile.email = email
        profile.is_active = True
        profile.is_staff = is_staff
        profile.is_verified = is_verified
        profile.set_password(password)
        for attr, value in extra_fields.items():
            setattr(profile, attr, value)
        profile.save()

        return profile


class CustomUserProfile(AbstractBaseUser, PermissionsMixinFacade):
    USERNAME_FIELD = 'email'
    objects = CustomUserProfileManager()

    email = models.EmailField(
        _('Email Address'),
        unique=True,
        db_index=True,
    )

    is_active = models.BooleanField(_('active'), default=True)

    is_staff = models.BooleanField(_('staff'), default=False)

    # Tracks whether the user's email has been verified
    is_verified = models.BooleanField(_('verified'), default=False)

    date_joined = models.DateTimeField(default=now)

    def has_verified_email(self):
        return self.is_verified

    def delete(self, force_drop=False, *args, **kwargs):
        if force_drop:
            super().delete(*args, **kwargs)
        else:
            raise DeleteError(
                'UserProfile.objects.delete_user() should be used.',
            )

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        """Return string representation."""
        return str(self)
