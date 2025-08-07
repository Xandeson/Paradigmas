from django.urls import path
from .views import (
    DashboardView, CourseListView, CourseCreateView, CourseUpdateView, CourseDeleteView
)

urlpatterns = [
    # Dashboard
    path('', DashboardView.as_view(), name='dashboard'),
    
    # Cursos
    path('cursos/', CourseListView.as_view(), name='course_list'),
    path('cursos/novo/', CourseCreateView.as_view(), name='course_create'),
    path('cursos/<int:pk>/editar/', CourseUpdateView.as_view(), name='course_edit'),
    path('cursos/<int:pk>/excluir/', CourseDeleteView.as_view(), name='course_delete'),
]