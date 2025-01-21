import datetime
from django.db import models
from .choices import *
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.



class AccountManager(BaseUserManager):
    """
    Custom manager for handling user creation and management.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with the given email and password.

        :param email: The email address of the user.
        :param password: The password for the user. Defaults to None.
        :param extra_fields: Additional fields for the user model.
        :raises ValueError: If the email is not provided.
        :return: The created user instance.
        """
        if not email:
            raise ValueError("Email must be provided")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with the given email and password.

        :param email: The email address of the superuser.
        :param password: The password for the superuser. Defaults to None.
        :param extra_fields: Additional fields for the superuser model.
        :return: The created superuser instance.
        """
        user = self.create_user(email, password, **extra_fields)
        user.is_admin_user = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractUser):
    profile_picture = models.ImageField(
        upload_to="profile_images/", default="profile_images/default-profile-image.png", blank=True, null=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, blank=True, null=True, choices=Gender.choices)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True, default=0)
    otp = models.IntegerField(null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    password = models.CharField(max_length=20, blank=True, null=True)

    is_admin_user = models.BooleanField(default=False)
    is_seller_user = models.BooleanField(default=False)
    is_buyer_user = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)


    objects = AccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def calculate_age(self):
        """
        Calculates the age of the user based on their date of birth.

        Parameters:
        self (Account): The instance of the Account model.

        Returns:
        int or None: The age of the user if their date of birth is provided, otherwise returns None.
        """
        if not self.date_of_birth:
            return None
        today = datetime.date.today()
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month or (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
            age -= 1
        return age
        
    
    def save(self, *args, **kwargs):
        """
        Override the save method to automatically calculate and set the age before saving.

        This method checks if a date of birth is provided, calculates the age using
        the calculate_age method, and sets the age field before saving the instance.

        Parameters:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

        Returns:
        None. The method doesn't return anything explicitly, but saves the instance
        to the database with the updated age (if applicable).
        """
        if self.date_of_birth:
            self.age = self.calculate_age()
        super().save(*args, **kwargs)

    def clear_otp(self):
        """
        Clears the OTP (One-Time Password) and its creation timestamp if the email is verified.

        This method sets the `otp` and `otp_created_at` attributes to None and saves the changes
        to the database if the `is_email_verified` attribute is True.

        Returns:
            None
        """
        if self.is_email_verified:
            self.otp = None
            self.otp_created_at = None
            self.save()
        
    
    
    def __str__(self):
        """
        Returns a string representation of the Account instance.

        This method generates a formatted string containing the user's first name,
        last name, and their role(s) in the system. The roles are determined based
        on the boolean flags is_buyer_user, is_admin_user, and is_seller_user.

        Parameters:
        self (Account): The instance of the Account model.

        Returns:
        str: A formatted string containing the user's name and role(s).
             Format: "<first_name> <last_name> | (<role1><role2><role3>)"
             Where roles can be "Customer", "Admin", and/or "Vendor".
        """
        role = []
        if self.is_buyer_user:
            role.append("Customer")
        if self.is_admin_user:
            role.append("Admin")
        if self.is_seller_user:
            role.append("Vendor")
        return f"{self.first_name} {self.last_name} ({', '.join(role)})"


