from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'has_experience',
            'course',
            'cv1',
            'cv2',
            'cv3',
            'cv4',
            'certificate1',
            'certificate2',
            'certificate3',
            'certificate4',
            'message',
        ]

        widgets = {
            'course': forms.TextInput(attrs={'hidden': True}),
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = (field.widget.attrs.get('class') or '') + ' regular-input'
