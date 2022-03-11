from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField('account.User', on_delete=models.PROTECT, related_name='owned_group', null=False)
    name = models.CharField(max_length=300, blank=False, null=False)
    description = models.TextField(null=False, blank=True)
    connected_to = models.ManyToManyField('account.Group', blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


# Create your models here.
class User(AbstractUser):
    """
    todo : use email as sign in key
    """
    email = models.EmailField(_('email address'), blank=False, null=False, unique=True)
    name = models.CharField(max_length=200, blank=False, null=False, unique=False)
    group = models.ForeignKey('account.Group', on_delete=models.PROTECT, related_name='members', null=True)
    joined_at = models.DateTimeField(null=True)  # joined to group

    # has_chat = models.ManyToManyField('account.User')

    def __str__(self):
        return self.email


class JoinRequest(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='join_requests')
    group = models.ForeignKey('account.Group', on_delete=models.CASCADE, related_name='join_requests')
    date = models.DateTimeField(auto_now_add=True)


class ConnectionRequest(models.Model):
    id = models.AutoField(primary_key=True)
    from_group = models.ForeignKey('account.Group', on_delete=models.CASCADE, related_name="sent_con_reqs")
    to_group = models.ForeignKey('account.Group', on_delete=models.CASCADE, related_name="rec_con_reqs")
    sent = models.DateTimeField(auto_now_add=True)
