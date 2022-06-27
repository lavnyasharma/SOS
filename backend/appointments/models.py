from datetime import datetime
from enum import auto
from django.utils import timezone
from cv001.utils.uid import decode_id, encode_id
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Appointment(models.Model):
    """
    APOINID 
    UID 
    OFID 
    BATCH 
    actual_end_time
    date 
    PST 
    status 
    created_at
    updated_at

    """
    APOINID = models.CharField(
        _("Appointment ID"), max_length=150, primary_key=True)
    UID = models.CharField(_("User ID"), max_length=150)
    OFID = models.CharField(
        _("Office ID"), max_length=150, blank=True, null=True)
    BATCH = models.CharField(_("Batch"), max_length=150, null=True)
    actual_end_time = models.DateTimeField(
        _("Actual End Time"), blank=True, null=True)
    date = models.DateField()
    PST = models.TimeField(_('probable start time'))
    status = models.CharField(
        _("Status"), max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        phone = decode_id(self.UID)['p']
        apoind = encode_id(p=phone, t='appointment', ct=str(timezone.now()))
        self.APOINID = apoind
        super(Appointment, self).save(*args, **kwargs)


class batch(models.Model):
    BATCHID = models.CharField(_("Batch ID"), max_length=150, primary_key=True)
    OFID = models.CharField(_("Office ID"), max_length=150)
    date = models.DateField()
    name = models.CharField(_("Name"), max_length=10)
    start = models.TimeField(_('Start Time'), null=True)
    end = models.TimeField(_('End Time'), null=True)
    min = models.IntegerField(_('Minutes'), null=True)
    SLOTS = models.IntegerField(_('Slots per hour'), null=True)
    total_hours = models.IntegerField(_('Total Hours'), null=True)
    status = models.CharField(null=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        phone = decode_id(self.OFID)['p']
        batchid = str(self.date).split(
            '-')[0] + str(self.date).split('-')[1] + str(self.date).split('-')[2] + "_" + str(phone)
        self.BATCHID = batchid
        super(batch, self).save(*args, **kwargs)
