from django import forms

from fokus.attachment.models import ImageResource, URLResource

#models = (ImageResource, URLResource,)
#content_types = [(model, ContentType.objects.get(model=model.__name__.lower())) for model in models]
#choices = [(ct.id, model._meta.verbose_name) for (model, ct) in content_types]

#class BaseAttachmentFormset(forms.BaseInlineFormSet):
#    def clean(self):
#        return

class ImageResourceForm(forms.ModelForm):
    description = forms.CharField(required=False, label="Valgfri beskrivelse")
    
    class Meta:
        model = ImageResource

