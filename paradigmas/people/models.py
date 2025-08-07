from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel, Course


class Student(BaseModel):
    STATUS_CHOICES = [
        ('active', _('Ativo')),
        ('inactive', _('Inativo')),
        ('graduated', _('Formado')),
    ]

    name = models.CharField(max_length=200, verbose_name=_("Nome Completo"))
    email = models.EmailField(unique=True, verbose_name=_("E-mail"))
    registration = models.CharField(max_length=20, unique=True, verbose_name=_("Matrícula"))
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='students',
        verbose_name=_("Curso")
    )
    semester = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name=_("Semestre Atual")
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='active',
        verbose_name=_("Status")
    )
    enrollment_date = models.DateField(auto_now_add=True, verbose_name=_("Data de Matrícula"))

    class Meta:
        verbose_name = _("Aluno")
        verbose_name_plural = _("Alunos")
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