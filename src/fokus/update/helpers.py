from django.conf import settings
from django.template.context import Context
from django.template import loader

class UpdateRenderer:
    def __init__(self, parent, updates, level):
        self.parent = parent
        self.updates = updates
        self.level = level
    
    def render(self):
        if self.level <= settings.UPDATE_RECURSION_LIMIT:
            c = Context({'parent': self.parent, 'updates': self.updates})
            template = loader.get_template('issues/update/list.html')
            return template.render(c)
        else:
            raise ValueError, "Maximum recursion depth of %d reached." % settings.UPDATE_RECURSION_LIMIT
