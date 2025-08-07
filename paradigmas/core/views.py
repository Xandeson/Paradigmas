from django.shortcuts import render
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, TemplateView
)
from .models import Course
from .forms import CourseForm
from .mixins import TitleMixin, BreadcrumbMixin, FormMessageMixin, ModelInfoMixin


class DashboardView(TitleMixin, BreadcrumbMixin, TemplateView):
    """Dashboard principal com estatísticas"""
    template_name = 'core/dashboard.html'
    title = "Dashboard"
    subtitle = "Visão geral do sistema acadêmico"
    breadcrumbs = [
        {'name': 'Dashboard', 'url': None, 'active': True}
    ]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        courses = Course.objects.all()
        
        # Import Student from people app
        try:
            from people.models import Student
            students = Student.objects.all()
        except ImportError:
            students = []
        
        # Estatísticas
        context.update({
            'total_courses': courses.count(),
            'total_students': students.count() if students else 0,
            'active_students': students.filter(status='active').count() if students else 0,
            'graduated_students': students.filter(status='graduated').count() if students else 0,
            'popular_courses': courses.annotate(
                student_count=Count('students')
            ).order_by('-student_count')[:5],
            'recent_students': students.order_by('-created_at')[:5] if students else [],
        })
        
        return context


# Course Views
class CourseListView(TitleMixin, BreadcrumbMixin, ModelInfoMixin, ListView):
    """Lista todos os cursos"""
    model = Course
    template_name = 'core/course_list.html'
    context_object_name = 'courses'
    paginate_by = 12
    title = "Cursos"
    subtitle = "Gerencie os cursos disponíveis"
    breadcrumbs = [
        {'name': 'Dashboard', 'url': 'dashboard', 'active': False},
        {'name': 'Cursos', 'url': None, 'active': True}
    ]


class CourseCreateView(TitleMixin, BreadcrumbMixin, FormMessageMixin, SuccessMessageMixin, CreateView):
    """Criar novo curso"""
    model = Course
    form_class = CourseForm
    template_name = 'core/course_form.html'
    success_url = reverse_lazy('course_list')
    title = "Novo Curso"
    subtitle = "Preencha os dados do novo curso"
    success_message_create = "Curso criado com sucesso!"
    breadcrumbs = [
        {'name': 'Dashboard', 'url': 'dashboard', 'active': False},
        {'name': 'Cursos', 'url': 'course_list', 'active': False},
        {'name': 'Novo Curso', 'url': None, 'active': True}
    ]
    
    def get_success_message(self, cleaned_data):
        return super().get_success_message('create')
    
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)


class CourseUpdateView(TitleMixin, BreadcrumbMixin, FormMessageMixin, SuccessMessageMixin, UpdateView):
    """Editar curso existente"""
    model = Course
    form_class = CourseForm
    template_name = 'core/course_form.html'
    success_url = reverse_lazy('course_list')
    title = "Editar Curso"
    subtitle = "Atualize as informações do curso"
    success_message_update = "Curso atualizado com sucesso!"
    breadcrumbs = [
        {'name': 'Dashboard', 'url': 'dashboard', 'active': False},
        {'name': 'Cursos', 'url': 'course_list', 'active': False},
        {'name': 'Editar Curso', 'url': None, 'active': True}
    ]
    
    def get_success_message(self, cleaned_data):
        return super().get_success_message('update')
    
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.updated_by = self.request.user
        return super().form_valid(form)


class CourseDeleteView(TitleMixin, BreadcrumbMixin, FormMessageMixin, SuccessMessageMixin, DeleteView):
    """Deletar curso"""
    model = Course
    template_name = 'core/course_confirm_delete.html'
    success_url = reverse_lazy('course_list')
    title = "Excluir Curso"
    subtitle = "Confirme a exclusão do curso"
    success_message_delete = "Curso excluído com sucesso!"
    breadcrumbs = [
        {'name': 'Dashboard', 'url': 'dashboard', 'active': False},
        {'name': 'Cursos', 'url': 'course_list', 'active': False},
        {'name': 'Excluir Curso', 'url': None, 'active': True}
    ]
    
    def get_success_message(self, cleaned_data):
        return super().get_success_message('delete')