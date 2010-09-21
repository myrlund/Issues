# -*- coding: utf8 -*-

import re

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.template.defaultfilters import pluralize

from fokus.issue.helpers import get_project, redirect
from fokus.issue.models import IssueStatus, Issue

def issues_set_status(request, project_number):
    project = get_project(project_number)
    r = re.compile(r'issue-(\d+)')
    
    if not request.POST.has_key("status_id"):
        messages.error(request, "Det skjedde en feil under statusoppdateringen.")
    else:
        status_id = request.POST["status_id"]
        status = IssueStatus.objects.get(id=status_id)
        
        altered = []
        for field, value in request.POST.iteritems():
            m = r.match(field)
            if value == "on" and m:
                issue_id = m.groups()[0]
                issue = get_object_or_404(Issue, id=issue_id)
                issue.status = status
                issue.save()
                
                altered.append(issue)
        
        if status.closed: verb = u"lukket"
        elif status.name == "on_hold": verb = u"satt på vent"
        elif status.name == "wip": verb = u"endret til 'under behandling'"
        else: verb = u"åpnet"
        
        messages.success(request, "%d sak%s ble %s." % (len(altered), pluralize(altered, "er"), verb))
        
    return redirect(request, project.get_absolute_url())
