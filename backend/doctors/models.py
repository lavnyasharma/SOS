from django.db.models.fields import BooleanField
from django.utils import timezone
from cv001.utils.uid import decode_id, encode_id
from django.db import models
from django.utils.translation import gettext_lazy as _


class doctor(models.Model):
    DOCID = models.CharField(_("DOCID"), primary_key=True, max_length=150)
    UID = models.CharField(
        _('UID'),
        max_length=150,
        help_text=('User id'),
        unique=True
    )
    registration_number = models.CharField(
        max_length=150, blank=True, null=True)
    professional_statement = models.TextField(
        _('professional_statement'), null=True)  # detailed overview of the doctor’s qualifications
    # url for acessing this model
    slug = models.CharField(_("slug"), max_length=100, unique=True)
    # date from which the doctor is working in profession
    practicing_from = models.DateField(_('practicing from'), null=True)
    joined_at = models.DateTimeField(
        _("joined at"), auto_now=True)  # joining date

    def save(self, *args, **kwargs):
        phone = decode_id(self.UID)['p']
        docid = encode_id(p=phone, t='doc', ct=str(timezone.now()))
        self.DOCID = docid
        super(doctor, self).save(*args, **kwargs)


class specialization(models.Model):
    SPEID = models.CharField(_("specialization id"),
                             primary_key=True, max_length=150)
    name = models.CharField(
        _("specialization name"), null=False, max_length=150)

    def save(self, *args, **kwargs):
        id = encode_id(t='spec', ct=str(timezone.now()))
        self.SPEID = id
        super(specialization, self).save(*args, **kwargs)


class doc_specialization(models.Model):
    DOCID = models.CharField(_("doctor id"), null=False, max_length=150)
    SPEID = models.CharField(_("specialization id"),
                             null=False, max_length=150)


class qualification(models.Model):
    QID = models.CharField(_("Qualification id"),
                           primary_key=True, max_length=150)
    DOCID = models.CharField(_("doctor id"), null=False, max_length=150,unique=True)
    name = models.CharField(_("Qualification name"),
                            null=False, max_length=150)
    institute = models.CharField(
        _("institute name"), null=False, max_length=150)
    year = models.DateField(_("procurement year"), null=False)
    city = models.CharField(_("city"), max_length=150)

    def save(self, *args, **kwargs):
        phone = decode_id(self.DOCID)['p']
        qid = encode_id(p=phone, t='qual', ct=str(timezone.now()))
        self.QID = qid
        super(qualification, self).save(*args, **kwargs)


class hospital(models.Model):
    """
    HOID 
    DOCID 
    name 
    city 
    start 
    end 
    """
    HOID = models.CharField(_("hospital id"), primary_key=True, max_length=150)
    DOCID = models.CharField(_("doctor id"), null=False, max_length=150,unique=True)
    name = models.CharField(_("hospital name"), null=False, max_length=150)
    city = models.CharField(_("city"), max_length=150)
    start = models.DateField(_("start date"))
    currently_working = models.BooleanField(default=False)
    end = models.DateField(_("end date"), null=True)

    def save(self, *args, **kwargs):
        phone = decode_id(self.DOCID)['p']
        print('test')
        hoid = encode_id(p=phone, t='hosp', ct=str(timezone.now()))
        self.HOID = hoid
        super(hospital, self).save(*args, **kwargs)


class office(models.Model):
    OFID = models.CharField(_("hospital id"), primary_key=True, max_length=150)
    DOCID = models.CharField(_("doctor id"), null=False, max_length=150,unique=True)
    name = models.CharField(_("office name"), null=True, max_length=150)
    min_time_slot = models.IntegerField(_("min slot time"))
    first_consultation_fee = models.IntegerField(_("first consultation fee"))
    follow_up_fee = models.IntegerField(_("follow up fee"), null=True)
    start = models.TimeField(_("start time"), auto_now=True)
    end = models.TimeField(_("end time"), auto_now=True)
    AID = models.CharField(_("AID"), max_length=150, null=True)

    # days
    monday = models.BooleanField(_("monday"), default=True)
    tuesday = models.BooleanField(_("tuesday"), default=True, null=True)
    wednesday = models.BooleanField(_("wednesday"), default=True, null=True)
    thursday = models.BooleanField(_("thrusday"), default=True, null=True)
    friday = models.BooleanField(_("friday"), default=True, null=True)
    saturday = models.BooleanField(_("saturday"), default=True, null=True)
    sunday = models.BooleanField(_("sunday"), default=True, null=True)

    def save(self, *args, **kwargs):
        phone = decode_id(self.DOCID)['p']
        ofid = encode_id(p=phone, t='office', ct=str(timezone.now()))
        self.OFID = ofid
        super(office, self).save(*args, **kwargs)
