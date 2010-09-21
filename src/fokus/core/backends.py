from django.contrib.auth.backends import ModelBackend

from fokus.issue.models import User

class CustomBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist: #@UndefinedVariable
            return None

class AutomaticBackend:
    
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist: #@UndefinedVariable
            user = User(username=username, password=password)
            user.is_staff = True
            user.save()
        return user
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist: #@UndefinedVariable
            return None
    
