from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from . import models


class MovieForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'image_url', 'year', 'genre',
                  'directors_list', 'actors_list',
                  'review', 'dates', 'grade',)
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
            'review',
            'dates',
            'grade',
            Submit('add', 'Add')
        )


class TVShowForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'image_url', 'genre',
                  'genre_family', 'creators_list',)
        model = models.TVShow

    def __init__(self, *args, **kwargs):
        super(TVShowForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'image_url',
            'genre',
            'genre_family',
            'creators_list',
            Submit('add', 'Add')
        )


class TVShowSeasonForm(forms.ModelForm):
    class Meta:
        model = models.TVShowSeason
        fields = ('number', 'name', 'image_url', 'year', 'actors_list',
                  'review', 'dates', 'grade')

    def __init__(self, *args, **kwargs):
        super(TVShowSeasonForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'number',
            'name',
            'image_url',
            'year',
            'actors_list',
            'review',
            'dates',
            'grade',
            Submit('add', 'Add')
        )
