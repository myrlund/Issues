# -*- coding: utf8 -*-

import re

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.forms.models import modelformset_factory
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template.defaultfilters import pluralize
from django.db.models import Q 

from fokus.issue.models import Project, IssueType, IssueStatus, Issue,\
    IssueSubscription
from fokus.issue.forms import IssueForm
from fokus.issue.helpers import get_project, get_contract, tab, render_issue_response, render_project_response,\
    render_contract_response

from fokus.attachment.models import ImageResource
from fokus.attachment.forms import ImageResourceForm

from fokus.core.models import User

def project_tabs(project):
    tabs = [
        tab('list issues', 'Saker', project.get_absolute_url()),
        tab('list contracts', 'Kontrakter', project.get_contracts_url()),
        tab('search', u'Søk', reverse('fokus.search.views.search', args=(project.number,))),
    ]
    return tabs

def project_tools(project):
    tools = [
        tab('edit project', 'Rediger prosjekt', project.get_edit_url()),
        tab('new issue', 'Ny sak', project.get_new_issue_url()),
    ]
    return tools

def project_overview(request):
    projects = Project.objects.all()
    pagetitle = "Alle prosjekter"
    return render_issue_response(request, 'project/list.html', locals())

def project_home(request, project_number):
    pagetitle = u"%s" % (get_project(project_number))
    
    categories = [
        {
            "title": u"Mine åpne saker",
            "issues": request.user.issue_set.filter(status__closed=False),
        }
    ]
    return issue_default_tables(request, project_number, categories=categories, active_tab=0, vars=locals())

def issue_default_tables(request, project_number, qs=None, categories=[], active_tab=None, vars={}):
    project = get_project(project_number)
    
    # Load and filter base queryset
    if not qs: qs = Issue.objects.all()
    qs = qs.filter(project=project)
    
    # Load categories from queryset
    categories.append({
        "title": u"Åpne saker",
        "issues": qs.filter(status__closed=False),
    })
    categories.append({
        "title": u"Alle saker",
        "issues": qs.all(),
    })
    
    return issue_tables(request, project_number, categories, active_tab, vars)

def issue_tables(request, project_number, categories=[], active_tab=None, vars={}):
    project = get_project(project_number)
    
    filters = {
        'code': 'contracts__code',
        'status': 'status__name',
        'user': 'subscribers__username',
    }
    for field, q_field in filters.iteritems():
        if request.GET.has_key(field):
            for category in categories:
                category['issues'] = category['issues'].filter(Q(**{q_field: request.GET[field]}))
    
    # Load tabs
    tools = project_tools(project)
    tabs = project_tabs(project)
    if active_tab: tabs[active_tab]["active"] = True
    
    # Load all IssueStatuses
    all_statuses = IssueStatus.objects.all()
    
    if vars.has_key("breadcrumb"):
        print "WTF!?!?!?"
    vars.update(locals())
    
    return render_project_response(request, 'project/issue_tables.html', project_number, vars)

def project_edit(request, project_number):
    pass

def contract_list(request, project_number):
    project = get_project(project_number)
    pagetitle = u"Kontrakter"
    
    contracts = project.contract_set.all()
    for contract in contracts:
        contract.my_issues = contract.get_all_issues(request.user)
        contract.my_issues_url = contract.get_my_issues_url(request.user)
    tools = project_tools(project)
    tabs = project_tabs(project)
    tabs[1]["active"] = True
    return render_project_response(request, 'contract/list.html', project_number, locals())

def contract_home(request, project_number, code):
    contract = get_contract(project_number, code)
    pagetitle = contract
    
    my_open_issues = contract.get_open_issues(request.user)
    my_issues = contract.get_all_issues(request.user)
    tools = [
        tab('edit contract', 'Rediger kontrakt', contract.get_edit_url()),
        tab('new issue', 'Ny sak', contract.get_new_issue_url()),
    ]
    return render_contract_response(request, 'contract/home.html', project_number, code, locals())

def contract_edit(request):
    pass

def contract_delete(request):
    pass

def contract_new(request):
    pass

def issue_subscribe(request, project_number, issue_id, user_id=None):
    if not user_id:
        user = request.user
    else:
        user = get_object_or_404(User, id=user_id)
    
    issue = get_object_or_404(Issue, id=issue_id)
    
    subscription, created = IssueSubscription.objects.get_or_create(issue=issue, user=user) #@UnusedVariable
    
    if created:
        messages.success(request, "Du abonnerer nå på denne saken.")
    else:
        messages.info(request, "Du abonnerer allerede på denne saken.")
    
    return HttpResponseRedirect(issue.get_absolute_url())

def issue_unsubscribe(request, project_number, issue_id, user_id=None):
    if not user_id:
        user = request.user
    else:
        user = get_object_or_404(User, id=user_id)
    
    issue = get_object_or_404(Issue, id=issue_id)
    
    subscription = get_object_or_404(IssueSubscription, issue=issue, user=user)
    subscription.delete()
    
    messages.success(request, "Du er ikke lenger ansvarlig for denne saken.")
    
    return HttpResponseRedirect(issue.get_absolute_url())

def issue_notify(request, project_number, issue_id, user_id=None):
    return issue_toggle_notify(request, project_number, issue_id, user_id, True)

def issue_denotify(request, project_number, issue_id, user_id=None):
    return issue_toggle_notify(request, project_number, issue_id, user_id, False)

def issue_toggle_notify(request, project_number, issue_id, user_id=None, notify=None):
    if not user_id:
        user = request.user
    else:
        user = get_object_or_404(User, id=user_id)
    
    issue = get_object_or_404(Issue, id=issue_id)
    
    subscription = get_object_or_404(IssueSubscription, issue=issue, user=user)
    
    # Toggle if notify not set
    print "Notify is: %s" % notify
    if notify is None:
        notify = not subscription.notify
        print "Nofify is now: %s" % notify
    subscription.notify = notify
    
    subscription.save()
    
    if notify:
        messages.success(request, "Du vil nå motta varsler for denne saken.")
    else:
        messages.success(request, "Du vil ikke lenger motta varsler for denne saken.")
    
    return HttpResponseRedirect(issue.get_absolute_url())
    

def issue_view(request, project_number, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    tools = [
        tab('edit issue', 'Rediger sak', issue.get_edit_url()),
    ]
    
    subscription = False
    if request.user in issue.subscribers.all():
        tools.append(tab('unsubscribe issue', 'Avslutt abonnement', reverse(issue_unsubscribe, args=(project_number, issue_id,))))
        subscription = IssueSubscription.objects.get(issue=issue, user=request.user)
        if subscription.notify:
            tools.append(tab('unnotify', 'Slå av varsling', reverse(issue_denotify, args=(project_number, issue_id,))))
        else:
            tools.append(tab('notify', 'Slå på varsling', reverse(issue_notify, args=(project_number, issue_id,))))
    else:
        tools.append(tab('subscribe issue', 'Abonnér på sak', reverse(issue_subscribe, args=(project_number, issue_id,))))
    
    if subscription:
        issue.subscription = subscription
    
    # Load issue notificants cache excluding current user
    issue.notificants(exclude_user=request.user)
    
    breadcrumb = issue
    return render_project_response(request, 'issue/view.html', project_number, locals())

def issue_new(request, project_number, code=None):
    issue = Issue()
    # if code: issue.contracts.add(get_contract(project_number, code))
    issue.no_link = True
    return issue_form(request, project_number, issue, "oppretter", "opprett")

def issue_edit(request, project_number, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    return issue_form(request, project_number, issue, "redigerer", "lagre")

def issue_form(request, project_number, issue, action, postaction):
    ImageFormset = modelformset_factory(ImageResource, form=ImageResourceForm, extra=1, can_delete=True)
    image_qs = ImageResource.objects.none()
    if issue.pk:
        image_qs = issue.all_images()
    else:
        issue.project = get_project(project_number)
    
    if request.POST:
        form = IssueForm(request.POST, instance=issue)
        formset = ImageFormset(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            issue = form.save()
            
            images = formset.save(commit=False)
            for image in images:
                image.parent = issue
                image.save()
            
            return HttpResponseRedirect(issue.get_absolute_url())
    else:
        form = IssueForm(instance=issue)
        formset = ImageFormset(queryset=image_qs)
    
    breadcrumb = issue
    return render_project_response(request, 'issue/form.html', project_number, locals())

def issue_delete(request, project_number):
    if request.POST.has_key("issue_id"):
        issue = get_object_or_404(Issue, id=request.POST["issue_id"])
        issue.delete()
        
        #TODO: Load flash error message
        
        return HttpResponseRedirect(issue.project.get_absolute_url())
    else:
        raise Http404()

def get_close_formset():
    pass

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
        
    return HttpResponseRedirect(project.get_absolute_url())

def list(request, project_number, key, list_by, issues):
    breadcrumb = key
    key.project = get_project(project_number)
    return render_project_response(request, 'project/list_by.html', project_number, locals())

def list_by_type(request, project_number, type_id):
    list_by = "type"
    project = get_project(project_number)
    key = get_object_or_404(IssueType, id=type_id)
    issues = project.get_by_type(key)
    return list(request, project_number, key, list_by, issues)

def list_by_status(request, project_number, status_name):
    project = get_project(project_number)
    if status_name == "open":
        status = get_object_or_404(IssueStatus, closed=True)
        issues = project.issue_set.exclude(status=status)
        status = u"Åpen"
    else:
        status = get_object_or_404(IssueStatus, name=status_name)
        issues = project.issue_set.filter(status=status)
    
    category = {
        'title': u'Saker med status: %s' % status,
        'issues': issues,
    }
    
    return issue_tables(request, project_number, categories=[category], vars=locals())

def list_by_user(request, project_number, username=None):
    project = get_project(project_number)
    if not username:
        return HttpResponseRedirect(project.get_user_url(request.user))
    user = get_object_or_404(User, username=username)
    
    qs = Issue.objects.filter(subscribers=user)
    
    if user == request.user:
        user = u"meg"
    title = u"Saker tilordnet %s" % user
    
    vars = {
        "breadcrumb": {
            "title": title,
            "no_link": True,
        },
        "pagetitle": title,
    }
    
    return issue_default_tables(request, project_number, qs, vars=vars)
