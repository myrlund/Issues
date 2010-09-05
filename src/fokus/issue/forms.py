
from django.forms import ModelForm
from django.forms.fields import DateTimeField, BooleanField
from django.forms.widgets import TextInput
from django.forms.models import ModelMultipleChoiceField, modelformset_factory

from fokus.issue.models import Issue, IssueSubscription

class RelatedIssueField(ModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        qs = Issue.objects.all()
        if kwargs.has_key("instance"):
            qs = qs.exclude(pk=kwargs["instance"].pk)
        super(RelatedIssueField, self).__init__(*args, **kwargs)

class CloseForm(ModelForm):
    closed = BooleanField(required=False)
    
    class Meta:
        model = Issue
        fields = ('closed',)
    
    @staticmethod
    def formset():
        return modelformset_factory(Issue, CloseForm, extra=0)

class IssueForm(ModelForm):
    deadline = DateTimeField(widget=TextInput(attrs={'class': 'date'}), required=False)
    
    class Meta:
        model = Issue
    
    def __init__(self, *args, **kwargs):
        super(IssueForm, self).__init__(*args, **kwargs)
        self.load_related_choices()
    
    def load_related_choices(self):
        r = self._meta.model.objects.filter(project=self.instance.project)
        if self.instance.pk:
            r = r.exclude(pk=self.instance.pk)
        
        w = self.fields['related'].widget
        
        choices = []
        for choice in r:
            choices.append((choice.id, unicode(choice)))
        w.choices = choices
    
    def update_subscribers(self, subscribers):
        # Remove existing responsabilities not in new set
        for existing in self.instance.subscribers.all():
            if existing not in subscribers:
                IssueSubscription.objects.get(user=existing, issue=self.instance).delete()
        
        # Add new responsabilities
        for subscriber in subscribers:
            if subscriber not in self.instance.subscribers.all():
                IssueSubscription.objects.create(user=subscriber, issue=self.instance)
    
    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        self.instance = super(IssueForm, self).save(*args, **kwargs)
        self.instance.save()
        subscribers = self.cleaned_data['subscribers']
        self.update_subscribers(subscribers)
        return self.instance
    