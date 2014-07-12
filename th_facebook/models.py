# -*- coding: utf-8 -*-

from django.db import models
from django_th.models.services import Services


class Facebook(Services):

    # put whatever you need  here 
    
    # but keep at least this one 
    trigger = models.ForeignKey('TriggerService')

    class Meta:
        app_label = 'django_th'
