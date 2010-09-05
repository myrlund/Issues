from django.contrib import admin
from fokus.issue.models import Issue, IssueStatus, IssueType, Project, Contract

admin.site.register(Issue)
admin.site.register(IssueStatus)
admin.site.register(IssueType)
admin.site.register(Project)
admin.site.register(Contract)
