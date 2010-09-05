import re

from django.template import TemplateSyntaxError, Node, Variable
from django import template

from fokus.update.models import Update
from fokus.update.forms import UpdateForm
from fokus.core.templatetags.tools import split_token

register = template.Library()

class UpdateFormNode(Node):
    def __init__(self, parent, var_name):
        self.parent = Variable(parent)
        self.var_name = var_name
    
    def render(self, context):
        update = Update(parent=self.parent.resolve(context))
        form = UpdateForm(instance=update)
        
        context[self.var_name] = form
        return '' 

@register.tag
def update_form(parser, token):
    parent, var_name = split_token(token)
    return UpdateFormNode(parent, var_name)
