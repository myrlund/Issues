# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

from fokus.issue.models import IssueStatus, IssueType

class Migration(DataMigration):

    def forwards(self, orm):
        IssueStatus.objects.create(name=u"new", title=u"Ny", weight=0, color="red")
        IssueStatus.objects.create(name=u"on_hold", title=u"På vent", weight=2, color="orange")
        IssueStatus.objects.create(name=u"wip", title=u"Under behandling", weight=4, color="yellow")
        IssueStatus.objects.create(name=u"closed", title=u"Lukket", weight=6, color="green", closed=True)
        
        IssueType.objects.create(name=u"reklamasjon", title=u"Reklamasjon", weight=0)
        IssueType.objects.create(name=u"befaringsliste", title=u"Befaringsliste", weight=5)


    def backwards(self, orm):
        IssueStatus.objects.all().delete()
        IssueType.objects.all().delete()

    models = {
        'issue.issuestatus': {
            'Meta': {'ordering': "('weight', 'pub_date')", 'object_name': 'IssueStatus'},
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'color': ('django.db.models.fields.CharField', [], {'default': "'yellow'", 'max_length': '40'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'issue.issuetype': {
            'Meta': {'ordering': "('weight', 'pub_date')", 'object_name': 'IssueType'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
    }

    complete_apps = ['issue']
