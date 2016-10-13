from django import forms
from django.utils.translation import ugettext_lazy as _

from graph.helpers import get_title


class SearchBaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(SearchBaseForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = _(get_title(field))


class SearchForm(SearchBaseForm):
    text = forms.CharField(required=False)
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    # TODO validate end_date >= start_date
