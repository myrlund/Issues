# -*- coding: utf8 -*-

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from fokus.core.models import BaseModel
from fokus.attachment.helpers import generate_filename
from fokus.nesh.thumbnail.templatetags.thumbnail import thumbnail
from django.conf import settings

class Resource(BaseModel):
    
    description = models.TextField('beskrivelse', blank=True)
    
    # Parent
    parent_ct = models.ForeignKey(ContentType, editable=False)
    parent_fk = models.PositiveIntegerField(editable=False)
    
    parent = generic.GenericForeignKey(ct_field="parent_ct",
                                       fk_field="parent_fk")
    
    def get_absolute_url(self):
        return self.parent.get_absolute_url()
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        raise NotImplementedError('Kiddo must implement __unicode__!')

class ImageResource(Resource):
    _search_fields = ('description',)
    
    value = models.ImageField('fil', upload_to=generate_filename)
    
    class Meta:
        verbose_name = "Bilderessurs"
    
    @property
    def _project(self):
        return self.parent._project
    
    def __unicode__(self):
        s = u'<img src="%s" alt="%%s" />' % thumbnail(self.value.url, r'width=%d,height=%d' % (settings.THUMB_SIZE_SMALL))
        s = s % self.description or ''
        return s

class URLResource(models.Model):
    name = models.CharField('navn', max_length=200)
    type = models.CharField('type', max_length=150)
    value = models.URLField('URL', max_length=120,
                          help_text=u'For å legge ved ressurser fra SuperOffice, ' +
                          u'høyreklikk på ressursen, velg \"Kopier snarvei\" og lim denne inn her.')
    
    class Meta:
        verbose_name = "URL-ressurs"
    
    def __unicode__(self):
        return self.value
