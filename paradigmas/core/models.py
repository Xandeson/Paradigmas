from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Course(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome do Curso")
    code = models.CharField(max_length=20, unique=True, verbose_name="Código")
    description = models.TextField(verbose_name="Descrição")
    duration = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name="Duração (semestres)"
    )
    coordinator = models.CharField(max_length=200, verbose_name="Coordenador")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_student_count(self):
        return self.students.count()


class Student(models.Model):
    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('inactive', 'Inativo'),
        ('graduated', 'Formado'),
    ]

    name = models.CharField(max_length=200, verbose_name="Nome Completo")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    registration = models.CharField(max_length=20, unique=True, verbose_name="Matrícula")
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='students',
        verbose_name="Curso"
    )
    semester = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name="Semestre Atual"
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='active',
        verbose_name="Status"
    )
    enrollment_date = models.DateField(auto_now_add=True, verbose_name="Data de Matrícula")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.registration})"

    def get_status_display_class(self):
        status_classes = {
            'active': 'success',
            'inactive': 'danger',
            'graduated': 'primary',
        }
        return status_classes.get(self.status, 'secondary')
# Create your models here.
