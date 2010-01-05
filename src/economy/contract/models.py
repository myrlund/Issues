# -*- coding: utf8 -*-

from django.db import models
from django.forms import ModelForm
from django.db.models import Q, Sum
from django.conf import settings

from economy.core.models import BaseModel

# from economy.project.models import Project
# from economy.invoices.models import Change, Invoice 

class Project(BaseModel):
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
    
    @models.permalink
    def get_absolute_url(self):
        return ('economy.contract.views.list_contracts', (self.id,))
    
    @models.permalink
    def new_contract_url(self):
        print "Min id:", self.id
        return ('economy.contract.views.new_contract', (), {'project_id': self.id})
    
    class Meta:
        ordering = ["title"]
        

class ContractCategory(BaseModel):
    title = models.CharField(max_length=50)
    weight = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ["weight"]

URL1 = '/static/info/bygningsdelstabell.html'
class Contract(BaseModel):
    project = models.ForeignKey(Project)
    category = models.ForeignKey(ContractCategory, blank=True, verbose_name='kategori', help_text='trengs ikke dersom Norsk Standard-rapportmal skal benyttes')
    code = models.CharField('kontraktskode', max_length=15, help_text='eget system eller <a href="'+URL1+'" target="_blank" onclick="popup(\''+URL1+'\');return false;"> tildeling for bygningsdelstabell')
    company = models.CharField('selskap', max_length=70, blank=True)
    budget = models.PositiveIntegerField('budsjett', default=0)
    amount = models.PositiveIntegerField('beløp', default=0)
    comment = models.TextField('kommentar', blank=True)
    
    def get_changes(self):
        return self.change_set.all()
    
    def get_invoices(self):
        return self.invoice_set.all()
    
    def total_accepted_changes(self):
        sum = self.change_set.filter(status__short=settings.ACCEPTED_SHORT).aggregate(amount=Sum("amount"), timediff=Sum("timediff"))
        return sum
    
    def total_pending_changes(self):
        sum = self.change_set.filter(~Q(status__short=settings.ACCEPTED_SHORT)).aggregate(amount=Sum("amount"), timediff=Sum("timediff"))
        return sum
    
    def total_invoices(self):
        sum = self.invoice_set.aggregate(amount=Sum("amount"))
        return sum["amount"]
    
    def total_changes(self):
        accepted = self.change_set.filter(status__short=settings.ACCEPTED_SHORT).aggregate(amount=Sum("amount"), timediff=Sum("timediff"))
        pending = self.change_set.filter(~Q(status__short=settings.ACCEPTED_SHORT)).aggregate(amount=Sum("amount"), timediff=Sum("timediff"))
        timediff = (accepted["timediff"] or 0) + (pending["timediff"] or 0)
        return {"accepted": accepted, "pending": pending, "timediff": timediff}
    
    def total_sum(self):
        changes = self.total_changes()["accepted"]["amount"] or 0
        invoices = self.total_invoices() or 0
        return invoices + changes
    
    def total_percent(self):
        total = (1.0 * self.total_invoices()) / self.total_sum()
        if total and total > 0:
            return total
        else:
            return 0
    
    def total_remaining(self):
        return self.amount - self.total_invoices()
    
    @models.permalink
    def get_url(self, action):
        return ('economy.contract.views.%s_contract' % action, (), {
            'project_id': self.project.id,
            'contract_code': self.code,
        })
    
    def get_absolute_url(self):
        return self.get_url("show")
    
    def get_edit_url(self):
        return self.get_url("edit")
    
    @models.permalink
    def new_subobject_url(self, type):
        return ('economy.invoices.views.new_%s' % type, (), {
            'project_id': self.project.id,
            'contract_code': self.code,
        })
    
    def new_change_url(self):
        try:
            print self.new_subobject_url("change")
        except Exception as inst:
            print inst
        return self.new_subobject_url("change")
    
    def new_invoice_url(self):
        return self.new_subobject_url("invoice")
    
    def __unicode__(self):
        return self.code
    
    class Meta:
        unique_together = ("project", "code")
        ordering = ["code"]

class ContractForm(ModelForm):
    class Meta:
        model = Contract
        exclude = ("project", "mod_date", "pub_date",)
