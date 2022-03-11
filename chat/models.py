from django.db import models


# Create your models here.

class Message:
    message = models.CharField(500, blank=False, null=False)
    sent_by = models.ForeignKey('account.User', on_delete=models.DO_NOTHING, null=False)
    sent_to = models.ForeignKey('account.User', on_delete=models.DO_NOTHING, null=False)
    date = models.DateTimeField(auto_now_add=True)
