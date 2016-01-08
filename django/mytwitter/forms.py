from django import forms
from .models import Tweet, TweetPic

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

from .fields import MultiImageField

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'picture']

    picture = MultiImageField(min_num=0, max_num=4, max_file_size=1024*1024*5, required=False)

    def __init__(self, *args, **kwargs):
        super(TweetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Tweet'))
        self.helper.form_method = 'post'
        self.helper.form_action = 'tweet'
        self.helper.layout = Layout(
            Field('text', rows="6")
            )

class TweetAdminForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['user', 'username', 'screenname', 'text']
