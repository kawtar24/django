# forms.py
from django import forms
class FileUploadForm(forms.Form):
    file = forms.FileField(label='Sélectionnez un fichier')

class ChooseColumnsForm(forms.Form):
    x_column = forms.ChoiceField(label='Choose X Column', choices=[])
    y_column = forms.ChoiceField(label='Choose Y Column', choices=[])

   