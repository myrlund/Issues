from django.db import models

from datetime import datetime

class BaseModel(models.Model):
    pub_date = models.DateTimeField('publisert')
    mod_date = models.DateTimeField('sist modifisert')
    
    def save(self, **kwargs):
        if not self.pk:
            self.pub_date = datetime.now()
        self.mod_date = datetime.now()
        super(BaseModel, self).save(**kwargs)
    
    class Meta:
        abstract = True
