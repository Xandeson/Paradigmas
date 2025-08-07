from django.urls import path
from .views import (
    StudentListView, StudentCreateView, StudentUpdateView, StudentDeleteView
)

app_name = 'people'

urlpatterns = [
    # Alunos
    path('alunos/', StudentListView.as_view(), name='student_list'),
    path('alunos/novo/', StudentCreateView.as_view(), name='student_create'),
    path('alunos/<int:pk>/editar/', StudentUpdateView.as_view(), name='student_edit'),
    path('alunos/<int:pk>/excluir/', StudentDeleteView.as_view(), name='student_delete'),
]