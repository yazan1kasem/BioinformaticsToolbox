from django import forms
from .models import SequenceSubmission

class SequenceSubmissionForm(forms.ModelForm):
    class Meta:
        model = SequenceSubmission
        fields = ['text_input', 'file_upload']
        labels = {
            'text_input': 'Texteingabe',
            'file_upload': 'Datei-Upload',
        }
        widgets = {
            'text_input': forms.Textarea(attrs={'placeholder': 'Geben Sie Ihren Text hier ein...', 'rows': 4, 'cols': 50}),
            'file_upload': forms.ClearableFileInput(attrs={'accept': 'application/pdf,image/*'}),  # Limitiert auf PDFs und Bilder
        }