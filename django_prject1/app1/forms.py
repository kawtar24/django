# forms.py
from django import forms
class FileUploadForm(forms.Form):
    file = forms.FileField(label='Sélectionnez un fichier')

class ChooseColumnsForm(forms.Form):
    col_name1 = forms.ChoiceField( choices=(), required=True)
    col_name2 = forms.ChoiceField( choices=(), required=True)

    def __init__(self, *args, **kwargs):
        column_choices = kwargs.pop('column_choices', None)

        super(ChooseColumnsForm, self).__init__(*args, **kwargs)

        if column_choices:
            self.fields['col_name1'].choices = column_choices
            self.fields['col_name2'].choices = column_choices


   