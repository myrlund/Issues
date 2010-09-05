# -*- coding: utf8 -*-

from datetime import datetime

from django.core.management.base import BaseCommand
from django.core.mail import send_mass_mail

from fokus.issue.models import Issue

class Command(BaseCommand):
    args = '<project project ...>'
    help = 'Checks for expired issues and notifies the responsible.'
    
    def handle(self, *args, **options):
        now = datetime.now()
        issues = Issue.objects.filter(deadline__lt=now)
        
        emails = []
        
        print "Found %d expired issues." % len(issues)
        for issue in issues:
            emails += issue.notify_subscribers('deadline', send=False)
        
        if emails:
            send_mass_mail(emails)
