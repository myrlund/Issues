from datetime import datetime

from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from fokus.core.models import AttachableModel, User
from django.conf import settings
from fokus.core.templatetags.tools import smart_trim
    
class Update(AttachableModel):
    _search_fields = ('text',)
    
    # Local text field
    text = models.TextField('tekst')
    
    # Generic fields
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    
    # Generic parent access
    parent = generic.GenericForeignKey()
    
    # User
    posted_by = models.ForeignKey(User, editable=False)
    
    class Meta:
        verbose_name = "oppdatering"
        verbose_name_plural = "oppdateringer"
    
    def __unicode__(self):
        return u"%s" % smart_trim(self.text)
    
    @property
    def _project(self):
        return self.issue._project
    
    @property
    def _index(self):
        return self.issue._index
    
    @property
    def issue(self):
        if isinstance(self.parent, Update):
            return self.parent.issue
        else:
            return self.parent
    
    def reply_url(self):
        return self.issue.reply_url()
    
    @models.permalink
    def get_url(self, action):
        return ('fokus.update.views.update_%s' % action, (self.issue.project.number, self.issue.id))
    
    def get_delete_url(self):
        return r"%s?update_id=%d" % (self.get_url('delete'), self.id)
    
    def get_absolute_url(self):
        return u"%s#update-%d" % (self.issue.get_absolute_url(), self.id)
    
    def thumb_size(self):
        return u"width=%d,height=%d" % settings.THUMB_SIZE_UPDATE
    
    def notify_subscribers(self):
        self.issue.notify_subscribers('update', self)
