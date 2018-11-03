from django import forms
from django.conf import settings

class SelectDatabaseForm(forms.Form):
    database = forms.ChoiceField(label='Database: ', 
                                 choices=settings.AVAILABLE_DATABASES)
    
    