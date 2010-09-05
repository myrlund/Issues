from django.forms.models import ModelForm

from fokus.update.models import Update
from django.forms.widgets import HiddenInput
from django.forms.fields import BooleanField

class UpdateForm(ModelForm):
    notify = BooleanField(initial=False, required=False)
    
    class Meta:
        model = Update
        
        widgets = {
            'content_type': HiddenInput(),
            'object_id': HiddenInput(),
        }
    
    def save(self, *args, **kwargs):
        notify = self.cleaned_data.pop('notify')
        update = super(UpdateForm, self).save(*args, **kwargs)
        update.notify = notify
        return update
        