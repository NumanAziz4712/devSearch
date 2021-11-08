from django import forms
from django.forms import ModelForm, widgets
from .models import Project, Review

class projectForm(ModelForm):

    class Meta: 

        model = Project
        fields = ['title', 'description', 'featured_image','demo_link', 'source_link', 'tags']

        widgets ={
            'tags': forms.CheckboxSelectMultiple(),
        }
    
    # adding class to our input 

    def __init__(self, *args, **kwargs):
        super(projectForm, self).__init__(*args, **kwargs)
        
        for label, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

        # self.fields['title'].widget.attrs.update({'class':'input'})
# reviews
class ReviewForm(ModelForm):

    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote',
        }
    
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        
        for label, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})