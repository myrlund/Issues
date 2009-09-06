# -*- coding: utf8 -*-

from django.db import models

class Project(models.Model):
    id = models.PositiveIntegerField("prosjektnummer", primary_key=True)
    title = models.CharField("tittel", max_length=70, blank=True, default="Uten navn")
    tax_rate = models.DecimalField(u"MVA-nivå", max_digits=4, blank=True, decimal_places=2, default="25.0", help_text="Oppgi i prosent") # 00.00-99.99 in percent
    
    def contracts(self, category=None):
        if category:
            return self.contract_set.filter(category=category)
        else:
            return self.contract_set.all()
    
    def contract_categories(self):
        return ContractCategory.objects.all()
    
    def __unicode__(self):
        return self.title
    
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
    
    def __unicode__(self):
        return self.code
    
    class Meta:
        unique_together = ("project", "code")
        ordering = ["code"]

class Invoice(models.Model):
    contract = models.ForeignKey(Contract)
    invoice_number = models.PositiveIntegerField()
    invoice_date = models.DateField()
    description = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    amount = models.IntegerField(default=0)
    
    def __unicode__(self):
        return u"%s%d" % (self.contract.code, self.invoice_number)
    
    def project(self):
        return self.contract.project
    
    class Meta:
        ordering = ["-invoice_date", "contract", "-invoice_number"]

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
    contract = models.ForeignKey(Contract)
    change_number = models.PositiveIntegerField()
    invoiced = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    status = models.ManyToManyField(ChangeStatus, through="ChangeStatusDate")
    timediff = models.IntegerField(blank=True, default=0) # Days
    amount = models.IntegerField()
    
    def __unicode__(self):
        return u"%s%d" % (self.contract, self.change_number)
    
    class Meta:
        ordering = ["-status__date", "contract"]

class ChangeStatusDate(models.Model):
    status = models.ForeignKey(ChangeStatus)
    change = models.ForeignKey(Change)
    date = models.DateField(blank=True)
    
    def save(self):
        if not self.date:
            self.date = datetime.date.today()
        super(ChangeStatusDate, self).save()

