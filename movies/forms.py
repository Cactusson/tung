from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from . import models


class MovieForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'image_url', 'year', 'genre',
                  'directors_list', 'actors_list', 'dates',
                  'review', 'grade',)
        model = models.Movie

    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'image_url',
            'year',
            'genre',
            'directors_list',
            'actors_list',
            'dates',
            'review',
            'grade',
            Submit('add', 'Add')
        )
