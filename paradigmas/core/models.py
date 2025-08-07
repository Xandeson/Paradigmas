import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models

# Create your models here.
User = get_user_model()


def get_sentinel_user():
    return get_user_model().objects.get_or_create(email="deleted")[0]


class UUIDModel(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True


class CreationTimestampedModel(models.Model):
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        editable=False,
    )
    created_by = models.ForeignKey(
        User,
        verbose_name=_("Created by"),
        on_delete=models.SET(get_sentinel_user),
        null=True,
        related_name="created_%(app_label)s_%(class)s_set",
    )

    class Meta:
        abstract = True


class UpdateTimestampedModel(models.Model):
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True, editable=False)
    updated_by = models.ForeignKey(
        User,
        verbose_name=_("Updated by"),
        on_delete=models.SET(get_sentinel_user),
        null=True,
        related_name="updated_%(app_label)s_%(class)s_set",
    )

    class Meta:
        abstract = True


class TimestampedModel(CreationTimestampedModel, UpdateTimestampedModel):
    class Meta:
        abstract = True


class BaseModel(UUIDModel, TimestampedModel):
    class Meta:
        abstract = True


class Course(BaseModel):
    name = models.CharField(max_length=200, verbose_name=_("Nome do Curso"))
    code = models.CharField(max_length=20, unique=True, verbose_name=_("Código"))
    description = models.TextField(verbose_name=_("Descrição"))
    duration = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name=_("Duração (semestres)")
    )
    coordinator = models.CharField(max_length=200, verbose_name=_("Coordenador"))

    class Meta:
        verbose_name = _("Curso")
        verbose_name_plural = _("Cursos")
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_student_count(self):
        return self.students.count()
    
    get_student_count.short_description = _("Número de Alunos")