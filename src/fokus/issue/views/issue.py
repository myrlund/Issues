# -*- coding: utf8 -*-

from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.forms.models import modelformset_factory
from django.core.urlresolvers import reverse

from fokus.core.models import User
from fokus.issue.models import Issue, IssueSubscription
from fokus.issue.forms import IssueForm
from fokus.issue.helpers import tab, render_project_response, get_project,\
    redirect
from fokus.attachment.models import ImageResource
from fokus.attachment.forms import ImageResourceForm

def issue_subscribe(request, project_number, issue_id, user_id=None, project_slug=None):
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

def issue_unsubscribe(request, project_number, issue_id, user_id=None, project_slug=None):
    if not user_id:
        user = request.user
    else:
        user = get_object_or_404(User, id=user_id)
    
    issue = get_object_or_404(Issue, id=issue_id)
    
    subscription = get_object_or_404(IssueSubscription, issue=issue, user=user)
    subscription.delete()
    
    messages.success(request, "Du er ikke lenger ansvarlig for denne saken.")
    
    return redirect(request, issue.get_absolute_url())

def issue_notify(request, project_number, issue_id, user_id=None, project_slug=None):
    return issue_toggle_notify(request, project_number, issue_id, user_id, True)

def issue_denotify(request, project_number, issue_id, user_id=None, project_slug=None):
    return issue_toggle_notify(request, project_number, issue_id, user_id, False)

def issue_toggle_notify(request, project_number, issue_id, user_id=None, notify=None, project_slug=None):
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
    
    return redirect(request, issue.get_absolute_url())
    

def issue_view(request, project_number, issue_id, project_slug=None):
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

def issue_new(request, project_number, code=None, project_slug=None):
    issue = Issue()
    # if code: issue.contracts.add(get_contract(project_number, code))
    issue.no_link = True
    return issue_form(request, project_number, issue, "oppretter", "opprett")

def issue_edit(request, project_number, issue_id, project_slug=None):
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
            
            return redirect(request, issue.get_absolute_url())
    else:
        form = IssueForm(instance=issue)
        formset = ImageFormset(queryset=image_qs)
    
    breadcrumb = issue
    return render_project_response(request, 'issue/form.html', project_number, locals())

def issue_delete(request, project_number, project_slug=None):
    if request.POST.has_key("issue_id"):
        issue = get_object_or_404(Issue, id=request.POST["issue_id"])
        issue.delete()
        
        #TODO: Load flash error message
        
        return redirect(request, issue.project.get_absolute_url())
    else:
        raise Http404()
