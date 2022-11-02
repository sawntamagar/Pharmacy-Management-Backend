from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import (
   AbstractUser
)

from itsdangerous import TimedSerializer as Serializer
SECRET_KEY="asdfhaoefahsdfasfieufdjsalsdjfkj12341!@#@###@!&hjshkjdhHHSFHASDFHSDHFHDFDHhdjfh"

class PmsUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # def set_password(self, user, password):
    #     return user.set_password(password)
    
    def create_superuser(self, email,password,  **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("superuser must have is_staff=True.")
        if extra_fields.get("is_superuser")is not True:
            raise ValueError("superuser must have is_superuser=True")
        
        return self.create_user(email, password, **extra_fields)
        

    def create_super_admin(self, email, password, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_super_admin", True)
        extra_fields.setdefault("is_pms_root", False)
        
        if extra_fields.get("is_admin") is not True:
            raise ValueError("superadmin must have is_admin=True")
        if extra_fields.get("is_super_admin") is not True:
            raise ValueError("superadmin must have is_super_admin=True")
        
        return self.create_user(email, password, **extra_fields)
    
    def get_token(self, email, expires_sec=900):
        s = Serializer(SECRET_KEY, "expires_sec")
        return s.dumps({"email":email})
    
    def verify_token(self, token):
        s=Serializer(SECRET_KEY, "expires_sec")
        try:
            email = s.loads(token)["email"]
        except Exception:
            return None
        user = PmsUser.objects.get(email=email)
        return user.email    
        

class PmsUser(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = None
    is_super_admin = models.BooleanField(
        _("admin status"),
        default=False,
        help_text=_("Designates whether the user is owner/creator of organization"))

    is_admin = models.BooleanField(
        _("admin status"),
        default=False,
    help_text=_("designates whether the user can log into admin site of the organization"))
    is_employee =models.BooleanField(_("employee status"), default=False, null =True)
    is_pms_root = models.BooleanField(_("pms_root status"), default=False,help_text=_("designates whether the pms user is super user") )
    is_active = models.BooleanField(default=True)
    email_confirmed = models.BooleanField(_("Invitation and email confirmation status"), default=False)
    email_confirmed_on = models.DateTimeField(null=True)
 
    updated_on = models.DateTimeField(_("info updated"), null=True)

   

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name"]
    
    objects = PmsUserManager()

    def update(self, update_dict=None, **kwargs):
        if not update_dict:
            update_dict = kwargs
        update_fields = {"updated_on"}
        for k, v in update_dict.items():
            setattr(self, k, v)
            update_fields.add(k)
        self.save(update_fields=update_fields)

    @property
    def is_user_handler(self):
        return self.is_hcm_root or self.is_super_admin or self.is_admin


class PmsUserDetails(models.Model):
    REQUIRED_FIELDS = ["first_name", "last_name", "user"]
    user =models.OneToOneField(PmsUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone_number =  models.CharField(max_length=15, blank=True)
    address =  models.CharField(max_length=50, blank=True)
    city =  models.CharField(max_length=50, blank=True)
    state =  models.CharField(max_length=50, blank=True)
    country =  models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    # wallet_address =  models.CharField(ma_length=100, blank=True)
    
#TODO staff detail and Admin invitation admin and admin inviting staff    
#staff detail which will be one to one relation with PMsUser and
# can only be filled up only after staff invitaion link sent by admin
    