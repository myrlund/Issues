from django import forms
from django.contrib.auth import forms as f

class LoginForm(f.AuthenticationForm):
    pass
    #username = forms.CharField(label="Brukernavn")
    #password = forms.CharField(label="Passord", widget=forms.PasswordInput)
    #remember = forms.BooleanField(label="Husk meg", required=False)

class ProfileForm(forms.Form):
    user = None
    
    username = forms.CharField(label="Brukernavn")
    email = forms.CharField(label="E-post")
    first_name = forms.CharField(label="Fornavn", required=False)
    last_name = forms.CharField(label="Etternavn", required=False)
    
    notification_interval = forms.IntegerField(label="Notifikasjonsintervall (i timer)", required=False)
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("instance")
        if not args:
            super(ProfileForm, self).__init__(self.data(), **kwargs)
        else:
            super(ProfileForm, self).__init__(*args, **kwargs)
    
    def data(self):
        return {
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'notification_interval': self.user.get_profile().deadline_notification_interval,
        }
    
    def save(self):
        self.user.username = self.cleaned_data['username']
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.user.email = self.cleaned_data['email']
        
        try:
            i = int(self.cleaned_data['notification_interval'])
            if i > 0:
                self.user.get_profile().deadline_notification_interval = i
        except ValueError:
            print "en feil! %s" % self.cleaned_data['notification_interval']
            pass
        
        self.user.save()
        self.user.get_profile().save()
        return self.user

class PasswordChangeForm(f.PasswordChangeForm):
    """ In case of later wanting to use own logic """
    pass
