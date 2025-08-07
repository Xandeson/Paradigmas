from django import forms
from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description', 'duration', 'coordinator']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Engenharia de Software'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: ENG001'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva o curso, objetivos e área de atuação...'
            }),
            'duration': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[(i, f'{i} semestre{"s" if i > 1 else ""}') for i in range(1, 13)]),
            'coordinator': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do coordenador'
            }),
        }