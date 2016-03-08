from django import forms
from .models import Whiteboard

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field


class WhiteboardForm(forms.ModelForm):

    class Meta:
        model = Whiteboard
        fields = ['account', 'date', 'text', 'image']

    def __init__(self, *args, **kwargs):
        super(WhiteboardForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Upload'))
        self.helper.form_method = 'post'
        self.helper.form_action = 'whiteboard'
        self.helper.layout = Layout(
            Field('account'),
            Field('date', placeholder='mm/dd/yyyy'),
            Field('text', rows="6")
            )
