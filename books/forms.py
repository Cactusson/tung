from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from . import models


class BookForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'image_url', 'year', 'genre',
                  'authors_list', 'review', 'dates', 'grade',)
        model = models.Book

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'image_url',
            'year',
            'genre',
            'authors_list',
            'review',
            'dates',
            'grade',
            Submit('add', 'Add')
        )
