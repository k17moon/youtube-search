from django.db import models
from django.utils import timezone

import requests
import re


# Create your models here.


class TubesearchModel(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(null=True, blank=True)

    # url情報
    keyword = models.CharField(max_length=50)

    # video情報
    # videos = models.JSONField(null=True, blank=True)

    #日付 デフォルトで今日の日付
    register_date = models.DateField(null=True, blank=True, default=timezone.now)
    last_date = models.DateField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.title


