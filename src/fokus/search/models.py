import re

from django.db import models
from django.db.models.loading import get_model
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from fokus.core.models import BaseModel

class Index(BaseModel):
    # Each project has its own isolated index
    project = models.OneToOneField('issue.Project', unique=True)
    
    @staticmethod
    def _index(obj):
        # Get or create index for current project
        index, c = Index.objects.get_or_create(project=obj._project) #@UnusedVariable
        return index.index(obj)
    
    @staticmethod
    def searchable_models():
        """ Settes opp i settings.INDEXABLE_MODELS. """
        m = [m.split(".", 1) for m in settings.INDEXABLE_MODELS]
        models = [get_model(t[0], t[1]) for t in m]
        return models
    
    def index(self, obj):
        # Create or get existing index entry
        ct = ContentType.objects.get_for_model(obj)
        index_entry, created = IndexEntry.objects.get_or_create(index=self, content_type=ct, object_id=obj.pk) #@UnusedVariable
        
        # Don't bother if not changed
        if not created and obj.mod_date <= index_entry.mod_date:
            return False
        
        # Update existing or create new field data
        for field_name in obj._search_fields:
            if obj.__class__.__name__ == "ImageResource":
                print "IR-field: %s" % field_name
            field, c = IndexEntryField.objects.get_or_create(index_entry=index_entry, #@UnusedVariable
                                                             field_name=field_name)
            field.value = obj.__getattribute__(field_name)
            field.save()
        
        return True
    
    def search(self, string, types):
        # Get all hits into a flat list
        flat_hits = self.indexentry_set.filter(indexentryfield__value__icontains=string).distinct()
        
        # Filter on content types
        if types:
            flat_hits = flat_hits.filter(content_type__id__in=[t.id for t in types])
        
        categories = {}
        for hit in flat_hits:
            # Create category
            if not categories.has_key(hit.content_type):
                categories[hit.content_type] = {}
                categories[hit.content_type]['hits'] = []
            
            # Load query string into fields, for formatting of output
            hit.fields = hit.indexentryfield_set.all()
            for f in hit.fields: f.q = string
            
            # Append hit to appropriate category
            categories[hit.content_type]['hits'].append(hit)
            categories[hit.content_type]['title'] = u"%s (%d treff)" % (
                hit.instance.modelname(True).title(),
                len(categories[hit.content_type]['hits']),
            )
        
        return categories

class IndexEntry(BaseModel):
    index = models.ForeignKey(Index)
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    
    instance = generic.GenericForeignKey()

class IndexEntryField(BaseModel):
    index_entry = models.ForeignKey(IndexEntry)
    field_name = models.CharField(max_length=150)
    value = models.TextField()
    
    q = None
    
    def __unicode__(self):
        if self.q:
            r = re.compile(r'(%s)' % self.q, re.I)
            return r.sub(r'<b>\1</b>', self.value)
        else:
            return self.value