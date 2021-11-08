from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import Message, Profiles, Skills

class CustomUserCreationForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['first_name', 'email','username', 'password1', 'password2']

        labels = {
            'first_name':'Full Name',
        }

    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for label, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

# profile form 

class ProfileForm(ModelForm):
    class Meta:
        model = Profiles
        fields = ['name', 'email', 'username', 'location', 'location','short_intro', 'bio', 'profile_image', 'social_github', 'social_twitter','social_linkedin', 'social_youtube', 'social_website']
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for label, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


# skills 
class SkillsForm(ModelForm):

    class Meta:
        model = Skills
        fields = ['name', 'description']
    
    def __init__(self, *args, **kwargs):
        super(SkillsForm, self).__init__(*args, **kwargs)

        for label, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

# messages 
class MessageForm(ModelForm):

    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']
    
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for label, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})