from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField('account.User', on_delete=models.PROTECT, related_name='owned_group', null=False)
    name = models.CharField(max_length=300, blank=False, null=False)
    description = models.TextField(null=False, blank=True)
    connected_to = models.ManyToManyField('account.Group')


# Create your models here.
class User(AbstractUser):
    """
    todo : use email as sign in key
    """

    email = models.EmailField(_('email address'), blank=False, null=False, unique=True)
    name = models.CharField(max_length=200, blank=False, null=False, unique=False)
    group = models.ForeignKey('account.Group', on_delete=models.PROTECT, related_name='members', null=True)


class JoinRequest(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    group = models.ForeignKey('account.Group', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class ConnectionRequest(models.Model):
    id = models.AutoField(primary_key=True)
    from_group = models.ForeignKey('account.Group', on_delete=models.CASCADE)
    to_group = models.ForeignKey('account.Group', on_delete=models.CASCADE)
    sent = models.DateTimeField(auto_now_add=True)
