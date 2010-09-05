from django import template
from django.template import Node, Variable
from django.forms.models import modelformset_factory

from fokus.attachment.models import ImageResource
from fokus.attachment.forms import ImageResourceForm
from fokus.core.templatetags.tools import split_token

register = template.Library()

class AttachmentFormsetNode(Node):
    def __init__(self, prefix, var_name):
        self.prefix = Variable(prefix)
        self.var_name = var_name
    
    def render(self, context):
        prefix = self.prefix.resolve(context)
        
        ImageFormset = modelformset_factory(ImageResource, form=ImageResourceForm, extra=1, can_delete=True)
        formset = ImageFormset(prefix=prefix, queryset=ImageResource.objects.none())
        
        context[self.var_name] = formset
        return '' 

@register.tag
def attachment_formset(parser, token):
    prefix, var_name = split_token(token) 
    return AttachmentFormsetNode(prefix, var_name)
