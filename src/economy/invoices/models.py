# # -*- coding: utf8 -*-

from datetime import datetime, date
from django.db import models
from django.db.models import Q, F
from django.db.models.signals import pre_save, post_save 
from django.forms.models import ModelForm, ModelChoiceField
from django import forms
from django.conf import settings

#from economy.contract.models import Contract
from economy.core.models import BaseModel
from economy.contract.helpers import render_project_response

class Invoice(BaseModel):
    contract = models.ForeignKey("contract.Contract")
    number = models.PositiveIntegerField(u"fakturanummer")
    date = models.DateField(u"fakturadato")
    description = models.TextField(u"beskrivelse", blank=True)
    comment = models.TextField(u"kommentar", blank=True)
    amount = models.IntegerField(u"beløp", default=0)
    
    def __unicode__(self):
        return u"%s%d" % (self.contract.code, self.number)
    
    @staticmethod
    def sum(invoices):
        amount = 0
        for invoice in invoices:
            amount += invoice.amount
        return {"amount": amount}
    
    @staticmethod
    def get_search_fields():
        return ["number", "description", "comment"]
    
    def get_edit_url(self):
        return self.get_url("edit")
    
    def get_absolute_url(self):
        return self.get_url("show")
    
    @models.permalink
    def get_url(self, action):
        return ('economy.invoices.views.%s_invoice' % action, (), {
            'project_id': self.contract.project.number,
            'contract_code': self.contract.code,
            'number': self.number,
        })
    
    def project(self):
        return self.contract.project
    
    class Meta:
        ordering = ["-date", "contract", "-number"]
        unique_together = ("number", "contract",)
        
class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        exclude = ("contract","mod_date","pub_date",)
    # def save(self, status=0):
    #     return super(InvoiceForm, self).save()


class ChangeStatus(BaseModel):
    id = models.PositiveSmallIntegerField(primary_key=True)
    short = models.CharField(max_length=20)
    title = models.CharField(max_length=40, blank=True)
    
    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return self.short
    
    class Meta:
        get_latest_by = "changestatusdate"

class Change(BaseModel):
    contract = models.ForeignKey("contract.Contract", verbose_name="kontrakt")
    number = models.PositiveIntegerField('nummer')
    invoiced = models.BooleanField('fakturert?', default=False)
    description = models.TextField('beskrivelse', blank=True)
    comment = models.TextField('kommentar', blank=True)
    status = models.ForeignKey(ChangeStatus)
    # status = models.ManyToManyField(ChangeStatus, through="ChangeStatusDate")
    timediff = models.IntegerField('tidskrav', blank=True, default=0, help_text='dager') # Days
    amount = models.IntegerField('beløp')
    
    def status_date(self, status=None):
        if not status:
            try:
                status = self.status
            except ChangeStatus.DoesNotExist:
                return ChangeStatusDate(change=self, date=date.today())
        try:
            csd = self.changestatusdate_set.get(status=status)
        except ChangeStatusDate.DoesNotExist:
            csd = ChangeStatusDate(change=self, status=status, date=date.today())
            print "Lagde ny statusdato:", csd
        return csd
    
    def __unicode__(self):
        return u"EA%d" % self.number
    
    @staticmethod
    def sum(changes):
        amount = 0
        timediff = 0
        for change in changes:
            amount += change.amount
            timediff += change.timediff
        return {"amount": amount, "timediff": timediff}
    
    @staticmethod
    def get_search_fields():
        return ["number", "description", "comment", "status__title"]
    
    def get_statuses(self):
        return ChangeStatus.objects.all()
    
    def amount_accepted(self):
        if self.status.short == settings.ACCEPTED_SHORT:
            return self.amount
        else:
            return 0
    
    def amount_pending(self):
        if self.status.short != settings.ACCEPTED_SHORT:
            return self.amount
        else:
            return 0
    
    def get_edit_url(self):
        return self.get_url("edit")
    
    def get_absolute_url(self):
        return self.get_url("show")
    
    @models.permalink
    def get_url(self, action):
        return ('economy.invoices.views.%s_change' % action, (), {
            'project_id': self.contract.project.number,
            'contract_code': self.contract.code,
            'number': self.number,
        })
    
    class Meta:
        ordering = ["number"] # __date, "-status__status"

class ChangeForm(ModelForm):
    class Meta:
        model = Change
        exclude = ("contract","pub_date","mod_date",)

class ChangeStatusDate(BaseModel):
    status = models.ForeignKey(ChangeStatus)
    change = models.ForeignKey(Change)
    date = models.DateField()
    
    def save(self):
        # self.date = datetime.date.today()
        super(ChangeStatusDate, self).save()
    
    def __unicode__(self):
        return u"%s %s %s" % (self.status, self.change, self.date)
    
    class Meta:
        ordering = ("-date",)

class ChangeStatusDateForm(ModelForm):
    class Meta:
        model = ChangeStatusDate
        exclude = ("status", "change", "mod_date", "pub_date",)

def set_change_number(sender, instance, **kwargs):
    if not instance.number:
        instance.number = sender.objects.filter(contract=instance.contract).count()+1

def set_status_date(sender, instance, **kwargs):
    if instance.status:
        try:
            status_date = ChangeStatusDate.objects.get(status=instance.status, change=instance)
        except ChangeStatusDate.DoesNotExist:
            status_date = ChangeStatusDate(status=instance.status, change=instance)
        status_date.save()


#pre_save.connect(set_change_number, sender=Change)
#post_save.connect(set_status_date, sender=Change)
