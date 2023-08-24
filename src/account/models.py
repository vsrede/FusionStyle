from django.contrib.auth.base_user import AbstractBaseUser
# from main.managers import CustomerManager
# from main.utils.validators import first_name_validator
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from account.managers import CustomerManager


class Customer(AbstractBaseUser, PermissionsMixin):
    class CURRENCY_VALUES(models.IntegerChoices):
        UAH = 0, "UAH"
        USD = 1, "USD"
        EURO = 2, "EURO"

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(
        _("email address"), unique=True, error_messages={"unique": _("A user with that email already exists.")}
    )
    avatar = models.ImageField(upload_to="customer/avatar_customer/", null=True, blank=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    birth_date = models.DateField(_("birth_day"), blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True, help_text="+1234567890")
    address = models.CharField(max_length=50, blank=True, null=True, help_text="Maidan Nezalezhnosti 1")
    city = models.CharField(max_length=60, blank=True, null=True, help_text="	Kyiv")
    zipcode = models.CharField(max_length=5, blank=True, null=True, help_text="02000")
    country = CountryField(max_length=5, blank=True, null=True, help_text="").formfield()
    preferred_currency = models.PositiveSmallIntegerField(choices=CURRENCY_VALUES.choices, default=CURRENCY_VALUES.UAH)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )
    objects = CustomerManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
        abstract = False
        ordering = ("last_name",)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"

    # def clean(self):
    #     super().clean()
    #     self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def get_period_of_registration(self):
        return f"Time on site: {timezone.now() - self.date_joined}"
