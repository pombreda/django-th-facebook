# -*- coding: utf-8 -*-

from django.db import models
from django_th.models.services import Services


class Facebook(Services):

    status = models.CharField(max_length=80)
    url = models.URLField(max_length=255)
    message = models.CharField(max_length=80)

    tag = models.CharField(max_length=80, blank=True)
    trigger = models.ForeignKey('TriggerService')

    class Meta:
        app_label = 'django_th'
