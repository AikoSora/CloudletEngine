import re
from django.db import models
from time import strftime, time, localtime

class Account(models.Model):

    class TempBot:
        bot = None

    class Dialog:
        START = 'start'
        DEFAULT = 'default'

    username = models.TextField(default=None, null=True, blank=True)
    nickname = models.TextField(default="нету")
    user_id = models.IntegerField(default=0)
    dialog = models.TextField(default=Dialog.START)
    balance = models.DecimalField(default=100, max_digits=32, decimal_places=0)
    temp = models.TextField(default='')
    reg_date = models.TextField(default=f'{strftime("%Y.%m.%d %H:%M", localtime(time() + 10800))}')
    hyperlink = models.BooleanField(default=True)
    farm = models.IntegerField(default=0)