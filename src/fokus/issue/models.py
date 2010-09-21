# -*- coding: utf8 -*-

from datetime import datetime

from django.db import models
from django.conf import settings

from fokus.core.models import BaseModel, User
from fokus.core.models import AttachableModel
from django.template.context import Context
from django.template import loader
from django.core.mail import send_mass_mail
from fokus.search.models import Index

class Project(BaseModel):
    number = models.PositiveIntegerField('prosjektnummer', unique=True)
    title = models.CharField('tittel', max_length=70, default="Uten navn")
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ('number',)
        verbose_name = 'prosjekt'
        verbose_name_plural = 'prosjekter'
    
    @property
    def _index(self):
        return Index.objects.get_or_create(project=self)[0]
    
    @property
    def _project(self):
        return self
    
    @models.permalink
    def get_new_issue_url(self):
        return ('fokus.issue.views.issue.issue_new', (self.number,))
    
    @models.permalink
    def get_contracts_url(self):
        return ('fokus.issue.views.contract.contract_list', (self.number,))
    
    @models.permalink
    def get_user_url(self, user):
        return ('fokus.issue.views.list.list_by_user', (self.number, user.username))
    
    @models.permalink
    def get_url(self, action='view'):
        return ('fokus.issue.views.project.project_%s' % action, (self.number,))
    
    def get_absolute_url(self):
        return self.get_url("home")
    
    def get_by_type(self, type):
        return self.get_all_issues().filter(type=type)
    
    def get_by_status(self, status):
        return self.get_all_issues().filter(status=status)
    
    def get_all_issues(self, user=None):
        issues = Issue.objects.filter(contracts__project=self)
        
        if user:
            issues = issues.filter(subscribers=user)
        
        return issues.distinct()
    
    def get_open_issues(self, user=None):
        issues = self.get_all_issues(user)
        return issues.exclude(status__closed=True) 

class Contract(BaseModel):
    project = models.ForeignKey(Project, verbose_name='prosjekt')
    
    code = models.CharField('kode', max_length=20)
    company = models.CharField('selskap', max_length=70, blank=True)
    
    closed = models.BooleanField('lukket', default=False)
    
    class Meta:
        ordering = ('code',)
        verbose_name = 'kontrakt'
        verbose_name_plural = 'kontrakter'
        unique_together = ('project', 'code',)
    
    def __unicode__(self):
        s = self.code
        if self.company:
            s = u"%s: %s" % (s, self.company)
        return s
    
    @property
    def title(self):
        return self.__unicode__()
    
    def get_absolute_url(self):
        return self.get_url("home")
    
    @models.permalink
    def get_url(self, action=None):
        return ('fokus.issue.views.contract.contract_%s' % action, (self.project.number, self.code,))
    
    @models.permalink
    def get_new_issue_url(self):
        return ('fokus.issue.views.issue.issue_new', (self.project.number, self.code,))
    
    def get_my_issues_url(self, user):
        #TODO: Implementer
        pass
    
    def get_all_issues(self, user=None):
        issues = Issue.objects.filter(contracts=self)
        if user:
            issues = issues.filter(subscribers=user)
        return issues.distinct()

    def get_open_issues(self, user=None):
        return self.get_all_issues(user).exclude(status__closed=True)
    
    @staticmethod
    def link_list(contracts):
        list = []
        for contract in contracts:
            list.append(u"<a href=\"%s\">%s</a>" % (contract.get_absolute_url(), contract.code))
        return list

class IssueType(BaseModel):
    name = models.CharField('navn', max_length=20, unique=True)
    title = models.CharField('tittel', max_length=35)
    description = models.TextField('beskrivelse', blank=True)
    weight = models.IntegerField('vekt', default=0)

    class Meta:
        ordering = ('weight', 'pub_date',)
        verbose_name = 'sakstype'
        verbose_name_plural = 'sakstyper'

    def __unicode__(self):
        return self.title
    
    @property
    def key(self):
        return self.id
    
    @models.permalink
    def get_absolute_url(self):
        return ('fokus.issue.views.list.list_by_type', (self.project.number, self.key,))


class IssueStatus(BaseModel):
    name = models.CharField('navn', max_length=20, unique=True)
    title = models.CharField('tittel', max_length=35)
    description = models.TextField('beskrivelse', blank=True)
    weight = models.IntegerField('vekt', default=0)
    
    closed = models.BooleanField('indikerer lukket?', default=False)
    color = models.CharField('farge', default='yellow', 
                             choices=[(c,c.title()) for c in settings.BULLET_COLORS],
                             max_length=40)
    
    class Meta:
        ordering = ('weight', 'pub_date',)
        verbose_name = 'saksstatus'
        verbose_name_plural = 'saksstatuser'
        
    def __unicode__(self):
        return self.title
    
    @property
    def key(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('fokus.issue.views.list.list_by_status', (self.project.number, self.key,))

PRIORITIES = (
    (1, "Lav"),
    (2, "Normal"),
    (3, "Høy"),
)

class IssueSubscriptionNotification(BaseModel):
    subscription = models.ForeignKey('IssueSubscription')
    
    class Meta:
        get_latest_by = "pub_date"

class IssueSubscription(BaseModel):
    issue = models.ForeignKey('Issue')
    user = models.ForeignKey(User)
    
    # Whether the subscription should be notified
    notify = models.BooleanField(default=True)

class Issue(AttachableModel):
    _search_fields = ('subject', 'description',)
    
    # Project
    project = models.ForeignKey(Project, verbose_name='prosjekt', editable=False)
    
    # Make one required in form
    contracts = models.ManyToManyField(Contract, verbose_name='kontrakter', blank=True)

    # Regular local fields
    subject = models.CharField('emne', max_length=80)
    priority = models.IntegerField('prioritet', choices=PRIORITIES, default=2)
    deadline = models.DateField('frist', blank=True)
    description = models.TextField('beskrivelse', blank=True)
    
    # Simple foreign fields to avoid data duplication (must be maintainable)
    status = models.ForeignKey(IssueStatus, default=1, verbose_name='status')
    type = models.ForeignKey(IssueType, verbose_name='type')
    
    # Related issues
    related = models.ManyToManyField('self', verbose_name='relaterte saker', blank=True)
    
    # Subscribers
    subscribers = models.ManyToManyField(User, verbose_name='ansvarlige', blank=True, through=IssueSubscription)
    
    # Simple cache variable
    _notificants = None
    
    @property
    def _project(self):
        return self.project
    
    @property
    def _index(self):
        return self._project._index
    
    def close(self):
        self.status = IssueStatus.objects.get(closed=True)
        self.save()
    
    def done(self):
        return self.status.closed
    
    @property
    def title(self):
        if self.pk:
            return u"<strong>#%d</strong> - %s" % (self.id, self.subject,)
        else:
            return u"Ny sak"
    
    def notificants(self, exclude_user=None):
        if self._notificants is None:
            subscriptions = IssueSubscription.objects.filter(issue=self, notify=True)
            if exclude_user:
                subscriptions = subscriptions.exclude(user=exclude_user)
            self._notificants = [s.user for s in subscriptions]
        return self._notificants
    
    def f_deadline(self):
        return datetime.strptime(str(self.deadline), "%Y-%m-%d")
    
    class Meta:
        ordering = ('-pub_date', '-priority',)
        verbose_name = 'sak'
        verbose_name_plural = 'saker' 

    def __unicode__(self):
        if self.pk:
            return u"#%d - %s" % (self.id, self.subject,)
        else:
            return u"Ny sak"
    
    @models.permalink
    def get_url(self, action="show"):
        return ('fokus.issue.views.issue.issue_%s' % action, (self.project.number, self.id,))
        
    @models.permalink
    def reply_url(self):
        return ('fokus.update.views.update_save', (self.project.number, self.id,))
    
    @models.permalink
    def close_multiple_url(self):
        return ('fokus.issue.views.issue.issues_close', (self.project.number,))
    
    @models.permalink
    def get_list(self, by):
        return ('fokus.issue.views.list.list_by_%s' % by, (self.project.number, self.__getattribute__(by).key))
    
    def toggle_notify_url(self):
        return self.get_url("toggle_notify")
    
    def notify_subscribers(self, type, object=None, send=True):
        emails = []
        for subscriber in self.subscribers.all():
            # If subscriber posted an update, don't inform
            try:
                if object.posted_by == subscriber:
                    continue
            except:
                pass
            
            # Elsewise, check subscription
            subscription = IssueSubscription.objects.get(user=subscriber, issue=self)
            
            # If notify turned off for subscription, don't inform
            if subscription.notify:
                
                # In case of deadline notification, check for latest notification
                if type == 'deadline':
                    try:
                        # Get time since last notification
                        latest_notification = subscription.issuesubscriptionnotification_set.latest()
                        now = datetime.now()
                        timediff = now - latest_notification.pub_date
                        
                        # User setting for notification interval
                        req = subscriber.notification_interval
                        
                        # If time since last notification is less than required, don't inform
                        if timediff < req:
                            print "Found active notification. Time until expiry: %s" % abs(timediff - req)
                            continue
                        
                        print "No active notifications. Last notification expired by: %s" % abs(timediff - req)
                    except IssueSubscriptionNotification.DoesNotExist: #@UndefinedVariable
                        pass
                
                # Render template for email
                context = Context({
                    'issue': self,
                    'user': subscriber,
                    'host': settings.HOST,
                    'object': object,
                })
                template = loader.get_template('issues/issue/notification/%s.txt' % type)
                raw_msg = template.render(context)
                
                # Quick'n'dirty way of separating subject and message
                # If parent template extended, it shouldn't cause any problems
                subject, msg = raw_msg.split("####", 1)
                subject, msg = subject.strip(), msg.strip()
                
                # Append data tuple to email array for mass sending
                emails.append((subject, msg, settings.EMAIL_FROM, (subscriber.email,),))
                
                # If deadline notification, update latest notification
                if type == 'deadline':
                    IssueSubscriptionNotification.objects.create(subscription=subscription)
                
                print "[SUCCESS] Informed %s of issue #%d's %s." % (subscriber, self.id, type)
        
        # If method is to send emails itself, send them, elsewise, they need to be handled by caller
        if send:
            send_mass_mail(emails)
        
        return emails
    
    def contracts_list(self):
        return Contract.link_list(self.contracts.all())
    
    def subscriber_list(self):
        list = []
        for user in self.subscribers.all():
            list.append(u"<a href=\"%s\">%s</a>" % (self.project.get_user_url(user), user.first_name,))
        return list
    
    def get_type_url(self):
        return self.get_list("type")
    def get_status_url(self):
        return self.get_list("status")
    
    def get_upload_path(self, filename):
        now = datetime.now()
        return "%d/0/%s-%s" % (self.id, now.strftime("%Y-%m-%d-%H%M"), filename)
    
    def aall_images(self):
        images = self.images()
        for update in self.updates.all():
            images |= update.images()
        return images
    
    def thumb_size(self):
        return u"width=%d,height=%d" % settings.THUMB_SIZE_ISSUE
