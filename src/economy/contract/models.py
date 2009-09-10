# -*- coding: utf8 -*-

from django.db import models
from django.forms import ModelForm
from django.db.models import Q, F, Sum

# from economy.project.models import Project
# from economy.invoices.models import Change, Invoice 

ACCEPTED_SHORT = "godkjent"

class Project(models.Model):
    id = models.PositiveIntegerField("prosjektnummer", primary_key=True)
    title = models.CharField("tittel", max_length=70, blank=True, default="Uten navn")
    tax_rate = models.DecimalField(u"MVA-nivå", max_digits=4, blank=True, decimal_places=2, default="25.0", help_text="Oppgi i prosent") # 00.00-99.99 in percent
    
    def contracts(self, category=None):
        if category:
            return self.contract_set.filter(category=category)
        else:
            return self.contract_set.all()
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return "/%s/" % (self.id)
    
    class Meta:
        ordering = ["title"]
        

class ContractCategory(models.Model):
    title = models.CharField(max_length=50)
    weight = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ["weight"]


class Contract(models.Model):
    project = models.ForeignKey(Project)
    category = models.ForeignKey(ContractCategory)
    code = models.CharField(max_length=15)
    company = models.CharField(max_length=70, blank=True)
    budget = models.PositiveIntegerField(default=0)
    amount = models.PositiveIntegerField(default=0)
    comment = models.TextField(blank=True)
    
    def total_accepted_changes(self):
        changes = self.change_set.filter(status__short=ACCEPTED_SHORT).aggregate(amount=Sum("amount"), timediff=Sum("timediff"))
        return sum
    
    def total_pending_changes(self):
        sum = self.change_set.filter(~Q(status__short=ACCEPTED_SHORT)).aggregate(amount=Sum("amount"), timediff=Sum("timediff"))
        return sum
    
    def calculate_total(self):
        pass
    
    def get_absolute_url(self):
        return "%scontract/%s/" % (self.project.get_absolute_url(), self.code)
    
    def get_edit_url(self):
        return "%scontract/edit/%s/" % (self.project.get_absolute_url(), self.code)
    
    def __unicode__(self):
        return self.code
    
    class Meta:
        unique_together = ("project", "code")
        ordering = ["code"]

class ContractForm(ModelForm):
    class Meta:
        model = Contract
        exclude = ("project",)
