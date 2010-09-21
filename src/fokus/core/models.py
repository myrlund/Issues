from django.db import models
from django.contrib.contenttypes import generic

from django.contrib.auth.models import User as DjangoUser
from datetime import timedelta
from fokus.update.helpers import UpdateRenderer

class User(DjangoUser):
    class Meta:
        proxy = True
    
    def __unicode__(self):
        return self.full_name()
    
    def full_name(self):
        if self.first_name and self.last_name:
            return u"%s %s" % (self.first_name, self.last_name)
        else:
            return self.username.title()
    
    @property
    def notification_interval(self):
        return timedelta(hours=self.get_profile().deadline_notification_interval)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    # Custom fields
    deadline_notification_interval = models.PositiveIntegerField('intervall for notifisering om frister', default=24,
                                                                 help_text='Oppgis i timer.')

class ChangeManager(models.Manager):
    def get_query_set(self):
        return super(ChangeManager, self).get_query_set()
    
    def order_by(self, *args):
        if args and args[0] == "status_date":
            pass
        print "Sorterer etter statusdato."
        return super(ChangeManager, self).order_by(*args)

class BaseModel(models.Model):
    pub_date = models.DateTimeField('publisert', editable=False, auto_now_add=True)
    mod_date = models.DateTimeField('sist modifisert', editable=False, auto_now=True)
#    deleted = models.BooleanField('slettet', default=False)

#    def delete(self):
#        self.deleted = True
#        self.save()
    
    def save(self, *args, **kwargs):
        super(BaseModel, self).save(*args, **kwargs)
        try:
            self._index.index(self)
            print "Indexed %s." % self
        except:
            pass
    
    class Meta:
        abstract = True
    
    def modelname(self, plural=False):
        if plural:
            return self._meta.verbose_name_plural
        else:
            return self._meta.verbose_name
    
    @property
    def _project(self):
        raise NotImplementedError, "Each indexable model must implement project accessor."
    
    @property
    def _index(self):
        return self._project._index
    
    def get_url(self, action='view'):
        raise NotImplementedError('get_url not implemented for model.')
    
    def get_absolute_url(self):
        return self.get_url('view')
    
    def get_edit_url(self):
        return self.get_url('edit')



class UpdatableModel(BaseModel):
    # Generic relation to updates
    updates = generic.GenericRelation('update.Update', verbose_name='oppdateringer')
    
    def get_update_count(self):
        """ Gets self-inclusive update count """
        return self.get_child_count() + 1
    
    def get_child_count(self):
        """ Gets number of child updates """
        count = self.updates.count()
        count += sum([update.get_child_count() for update in self.updates.all()])
        return count
    
    class Meta:
        abstract = True
    
    def render_updates(self, current_level=1):
        return UpdateRenderer(self, self.updates.all(), current_level).render()

class AttachableModel(UpdatableModel):
    # Generic relation to attachments
    images = generic.GenericRelation('attachment.ImageResource',
                                     verbose_name='bilder',
                                     content_type_field='parent_ct',
                                     object_id_field="parent_fk")
    
    resources = generic.GenericRelation('attachment.URLResource',
                                        verbose_name='ressurser',
                                        content_type_field='parent_ct',
                                        object_id_field="parent_fk")
    
    class Meta:
        abstract = True
    
    @property
    def attachments(self):
        a = list(self.images.all())
        a += list(self.resources.all())
        return a
    
    def all_images(self):
        images = self.images.all()
        for update in self.updates.all():
            images |= update.all_images()
        return images
    