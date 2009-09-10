# # -*- coding: utf8 -*-

from django.db import models
from django.db.models import Q, F
from django.db.models.signals import pre_save, post_save 
from django.forms.models import ModelForm
from django import forms

#from economy.contract.models import Contract
from economy.contract.helpers import render_project_response

class Invoice(models.Model):
    contract = models.ForeignKey("contract.Contract")
    invoice_number = models.PositiveIntegerField()
    invoice_date = models.DateField()
    description = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    amount = models.IntegerField(default=0)
    
    def __unicode__(self):
        return u"%s%d" % (self.contract.code, self.invoice_number)
    
    @staticmethod
    def sum(invoices):
        amount = 0
        for invoice in invoices:
            amount += invoice.amount
        return {"amount": amount}
    
    def project(self):
        return self.contract.project
    
    class Meta:
        ordering = ["-invoice_date", "contract", "-invoice_number"]
        
class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        exclude = ("contract",)


class ChangeStatus(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    short = models.CharField(max_length=20)
    title = models.CharField(max_length=40, blank=True)
    
    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return self.short

class Change(models.Model):
    contract = models.ForeignKey("contract.Contract")
    number = models.PositiveIntegerField()
    invoiced = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    status = models.ManyToManyField(ChangeStatus, through="ChangeStatusDate")
    timediff = models.IntegerField(blank=True, default=0) # Days
    amount = models.IntegerField()
    
    def __unicode__(self):
        return u"%s%d" % (self.contract, self.change_number)
    
    @staticmethod
    def sum(changes):
        amount = 0
        timediff = 0
        for change in changes:
            amount += change.amount
            timediff += change.timediff
        return {"amount": amount, "timediff": timediff}
    
    class Meta:
        ordering = ["contract__code"] # __date, "-status__status"

class ChangeForm(ModelForm):
    class Meta:
        model = Change
        exclude = ("contract", "number",)

class ChangeStatusDate(models.Model):
    status = models.ForeignKey(ChangeStatus)
    change = models.ForeignKey(Change)
    date = models.DateField(blank=True)
    
    def save(self):
        if not self.date:
            self.date = datetime.date.today()
        super(ChangeStatusDate, self).save()


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


pre_save.connect(set_change_number, sender=Change)
post_save.connect(set_status_date, sender=Change)
