from django import forms
from . import models


class UserForm(forms.Form):
    username = forms.CharField(max_length=8, widget=forms.TextInput(attrs={'size': 15}))
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))


class ProjectForm(forms.Form):
    project_id = forms.CharField(max_length=4, required=False)
    start_date = forms.CharField(max_length=10)
    project_no = forms.CharField(max_length=15)
    project_name = forms.CharField(max_length=30)
    protype_code = forms.ModelChoiceField(models.ProjectType.objects.order_by('PROTYPE_CODE'),
                                          empty_label='', to_field_name='PROTYPE_CODE')
    language_code = forms.ModelChoiceField(models.Language.objects.order_by('LANGUAGE_CODE'),
                                           empty_label='', to_field_name='LANGUAGE_CODE')
    summary = forms.CharField(widget=forms.Textarea, max_length=255)
    status_code = forms.ModelChoiceField(models.Status.objects.order_by('STATUS_CODE'),
                                         empty_label='', to_field_name='STATUS_CODE')
    customer = forms.CharField(max_length=20, required=False)
    charge = forms.CharField(max_length=20, required=False)
    reviewer = forms.CharField(max_length=20, required=False)
    release_date = forms.CharField(required=False, max_length=10)
    remarks = forms.CharField(widget=forms.Textarea, required=False, max_length=255)


class UrlForm(forms.Form):
    now_url = forms.CharField(required=False)


class EmotionForm(forms.Form):
    input_text = forms.CharField(widget=forms.Textarea)
