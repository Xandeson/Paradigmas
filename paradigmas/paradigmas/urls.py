"""
URL configuration for paradigmas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import  views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    # Cursos
    path('cursos/', views.course_list, name='course_list'),
    path('cursos/novo/', views.course_create, name='course_create'),
    path('cursos/<int:pk>/editar/', views.course_edit, name='course_edit'),
    path('cursos/<int:pk>/excluir/', views.course_delete, name='course_delete'),
    
    # Alunos
    path('alunos/', views.student_list, name='student_list'),
    path('alunos/novo/', views.student_create, name='student_create'),
    path('alunos/<int:pk>/editar/', views.student_edit, name='student_edit'),
    path('alunos/<int:pk>/excluir/', views.student_delete, name='student_delete'),
]
