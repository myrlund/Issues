from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from fokus.issue.models import Project
from django.conf import settings
from django.db.models.loading import get_model, get_models
from fokus.search.models import Index

class Command(BaseCommand):
    args = '<project_id project_id ...>'
    help = 'Indexes specified projects, or all of them, if none supplied.'
    
    def handle(self, *args, **options):
        # Get projects
        if args:
            projects = [Project.objects.get(number=n) for n in args]
        else:
            projects = Project.objects.all()
        
        models = Index.searchable_models()
        
        n = 0
        for model in models:
            instances = model.objects.all()
            for instance in instances:
                if instance._project in projects:
                    new = Index._index(instance)
                    if new:
                        n += 1
        
        print "Indexed %d objects." % n