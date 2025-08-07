from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'registration', 'course', 'semester', 'status']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do aluno'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
            'registration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 2024001001'
            }),
            'course': forms.Select(attrs={
                'class': 'form-control'
            }),
            'semester': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[(i, f'{i}º semestre') for i in range(1, 13)]),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }