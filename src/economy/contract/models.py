# -*- coding: utf8 -*-

from django.db import models
from django.forms import ModelForm
from django.db.models import Q, Sum
from django.conf import settings

from economy.core.models import BaseModel

from copy import copy
# from economy.project.models import Project
# from economy.invoices.models import Change, Invoice 

class Project(BaseModel):
    number = models.PositiveIntegerField("prosjektnummer", unique=True)
    title = models.CharField("tittel", max_length=70, blank=True, default="Uten navn")
    tax_rate = models.DecimalField(u"MVA-nivå", max_digits=4, blank=True, decimal_places=2, default="25.0", help_text="Oppgi i prosent") # 00.00-99.99 in percent
    budget = models.PositiveIntegerField(u"vedtatt budsjett", blank=True, default=0, help_text="Oppgi uten MVA")
    
    def contracts(self, category=None):
        if category:
            return self.contract_set.filter(category=category)
        else:
            return self.contract_set.all()
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('economy.contract.views.list_contracts', (self.number,))
    
    @models.permalink
    def get_edit_url(self):
        return ('economy.contract.views.edit_project', (self.number,))
    
    @models.permalink
    def new_contract_url(self):
        print "Min id:", self.id
        return ('economy.contract.views.new_contract', (), {'project_id': self.number})
    
    def calculate_budget_total(self):
        groups = self.calculate_ns_sums()["groups"]
        print groups
        return groups[-2]["sum"]["total"]
    
    def calculate_ns_sums(self, from_date=None, to_date=None):
        self.agg = {"amount": Sum("amount"), "budget": Sum("budget"), "invoices": Sum("invoice__amount"), "changes": Sum("change__amount")}
        self.q = self.contract_set.none()
        self.changes_a = self.empty_change_set()
        self.changes_p = self.empty_change_set()
        self.date_query = {}
        if from_date:
            self.date_query["%s__gt"] = from_date
        if to_date:
            self.date_query["%s__lt"] = to_date
        
        groups = []
        
        # Huskostnad
        ns = range(1,7)
        row = self.calculate_ns_row("Huskostnad", ns)
        groups.append(row)
        
        # Entreprisekostnader
        n = ns[-1] + 1
        row = self.calculate_ns_row("Entreprisekostnader", [n])
        groups.append(row)
        
        # Byggekostnader
        n += 1
        row = self.calculate_ns_row("Byggekostnader", [n])
        groups.append(row)
        
        # Byggekostnader
        n += 1
        row = self.calculate_ns_row("Prosjektkostnad", [n])
        groups.append(row)
        
        # RM
        budget_total = row["sum"]["total"]
        if self.budget:
            rm = self.budget - budget_total
            sum = copy(row["sum"])
            sum["total"] = self.budget
            groups.append({
                "title": "Totalsum eks. mva.",
                "posts": {"RM": {"total": rm, "title": "Reserver og marginer"}},
                "sum": sum,
            })
        
        #@todo: implement!
        if self.tax_rate > 0:
            for field, sum in row.iteritems():
                print field, "=", sum
        
        return {"groups": groups, "project": self}
    
    def calculate_change_sums(self, contracts):
        sums = {}
        ca = accepted_for_contracts(contracts)
        cp = pending_for_contracts(contracts)
        if ca:
            if self.date_query:
                pass #@todo: implement!
            sums.update(ca.aggregate(accepted=Sum("amount")))
            self.changes_a = self.changes_a | ca 
        if cp:
            if self.date_query:
                pass #@todo: implement!
            if self.date_query:
                cp.filter(self.date_query)
            sums.update(cp.aggregate(pending=Sum("amount")))
            self.changes_p = self.changes_p | cp
        # row_a = self.changes_a.aggregate(accepted=Sum("amount"))
        # row_p = self.changes_p.aggregate(pending=Sum("amount"))
        return sums
    
    def calculate_ns_row(self, title, ns):
        posts = {}
        for n in ns:
            posts_q = self.contract_set.filter(code__startswith=str(n))
            self.q = self.q | posts_q
            posts[n] = posts_q.aggregate()
            for name, sel in self.agg.iteritems():
                posts[n].update(posts_q.aggregate(**{name: sel}))
            posts[n]["total"] = (posts[n]["budget"] or 0) + (posts[n]["changes"] or 0)
            posts[n].update(self.calculate_change_sums(posts_q))
            if posts[n]["invoices"] and posts[n]["budget"]:
                posts[n]["percent"] = 100.0 * posts[n]["invoices"] / posts[n]["total"]
            else:
                posts[n]["percent"] = 0
            if POSTNAMES.has_key(n):
                posts[n]["title"] = POSTNAMES[n]
        sum = self.q.aggregate()
        for name, sel in self.agg.iteritems():
            sum.update(self.q.aggregate(**{name: sel}))
        sum["total"] = (sum["budget"] or 0) + (sum["changes"] or 0)
        if sum["invoices"] and sum["budget"]:
            sum["percent"] = 100.0 * sum["invoices"] / sum["total"]
        else:
            sum["percent"] = 0
        sum.update(self.calculate_change_sums(self.q))
        
        return {"title": title, "posts": posts, "sum": sum, "n": n}
    
    def calculate_category_sums(self, date_query=None):
        categories = []
        for category in ContractCategory.objects.all():
            contracts = self.contract_set.filter(category=category)
            if date_query:
                contracts = contracts.filter(date_query)
            sums = contracts.aggregate(changes=Sum("change__amount"), invoices=Sum("invoice__amount"), amount=Sum("amount"), budget=Sum("budget"))
            data = {"title": category.title, "contracts": contracts, "sums": sums}
            categories.append(data)
        total = self.contract_set.aggregate(changes=Sum("change__amount"), invoices=Sum("invoice__amount"), amount=Sum("amount"), budget=Sum("budget"))
        return {"categories": categories, "total": total}

    def empty_change_set(self):
        return self.contract_set.all()[0].change_set.none()

    class Meta:
        ordering = ["title"]

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ("pub_date", "mod_date",)

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
        return sum["amount"] or 0
    
    def total_changes(self):
        accepted = self.change_set.filter(status__short=settings.ACCEPTED_SHORT).aggregate(amount=Sum("amount"), timediff=Sum("timediff"))
        pending = self.change_set.filter(~Q(status__short=settings.ACCEPTED_SHORT)).aggregate(amount=Sum("amount"), timediff=Sum("timediff"))
        timediff = (accepted["timediff"] or 0) + (pending["timediff"] or 0)
        return {"accepted": accepted, "pending": pending, "timediff": timediff}
    
    def total_sum(self):
        changes = self.get_changes().aggregate(changes=Sum("amount"))["changes"] or 0
        return self.amount + changes
    
    def total_percent(self):
        if self.total_sum() != 0:
            total = (100.0 * self.total_invoices()) / self.total_sum()
        else:
            total = 0
        
        if total and total > 0:
            return total
        else:
            return 0
    
    def total_remaining(self):
        return self.total_sum() - self.total_invoices()
    
    @models.permalink
    def get_url(self, action):
        return ('economy.contract.views.%s_contract' % action, (), {
            'project_id': self.project.number,
            'contract_code': self.code,
        })
    
    def get_absolute_url(self):
        return self.get_url("show")
    
    def get_edit_url(self):
        return self.get_url("edit")
    
    @models.permalink
    def new_subobject_url(self, type):
        return ('economy.invoices.views.new_%s' % type, (), {
            'project_id': self.project.number,
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



#########################

def get_changes(contract_query):
    changes = [c.change_set.all() for c in contract_query.all()]
    if changes:
        cs = changes.pop(0)
        for c in changes:
            cs = cs | c
        return cs
    return changes

def accepted_for_contracts(contract_query):
    changes = get_changes(contract_query)
    if changes:
        return changes.filter(status__short=settings.ACCEPTED_SHORT)
def pending_for_contracts(contract_query):
    changes = get_changes(contract_query)
    if changes:
        return changes.exclude(status__short=settings.ACCEPTED_SHORT)

POSTNAMES = {
    0: "Diverse kostnader",
    1: "Felleskostnader",
    2: "Bygningsmessige arbeider",
    3: "VVS-installasjoner",
    4: "Elkraft",
    5: "Tele og automatisering",
    6: "Andre installasjoner",
    7: "Utvendige anlegg",
    8: "Generelle kostnader/Prosjektering",
    9: "Spesielle kostnader (MVA)",
}