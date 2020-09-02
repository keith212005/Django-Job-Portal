from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, UserManager, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from companies.models import CompanyInfo
from students.models import StudentInfo


class CustomUserManager(BaseUserManager):
  """
  Custom user model manager where email is the unique identifiers
  for authentication instead of usernames.
  """

  def create_user(self, email, password, **extra_fields):
    """
    Create and save a User with the given email and password.
    """
    if not email:
      raise ValueError(_('The Email must be set'))
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save()
    return user

  def create_superuser(self, email, password, **extra_fields):
    """
    Create and save a SuperUser with the given email and password.
    """
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    extra_fields.setdefault('is_active', True)

    if extra_fields.get('is_staff') is not True:
      raise ValueError(_('Superuser must have is_staff=True.'))
    if extra_fields.get('is_superuser') is not True:
      raise ValueError(_('Superuser must have is_superuser=True.'))
    return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
  user_type_data = ((1, "Admin"), (2, "Student"), (3, "Company"))
  user_type = models.IntegerField(default=1)
  email = models.EmailField(unique=True)
  pic = models.ImageField(upload_to='images/', blank=True, null=True)
  objects = CustomUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['user_type', 'username']

  def __str__(self):
    return self.email

  def __int__(self):
    return self.id

  def getEmail(self):
    return self.email

  def getUsername(self):
    return self.username


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    if instance.user_type == 2:
      StudentInfo.objects.create(account_user_id=instance.id,)
      pass
    if instance.user_type == 3:
      CompanyInfo.objects.create(account_user_id=instance.id)
      pass


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
  if instance.user_type == 2:
    instance.studentinfo.save()
  if instance.user_type == 3:
    instance.companyinfo.save()
