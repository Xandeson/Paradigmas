from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Student
from .forms import StudentForm
from core.mixins import TitleMixin, BreadcrumbMixin, FormMessageMixin, ModelInfoMixin


class StudentListView(TitleMixin, BreadcrumbMixin, ModelInfoMixin, ListView):
    """Lista todos os alunos"""
    model = Student
    template_name = 'people/student_list.html'
    context_object_name = 'students'
    paginate_by = 20
    title = "Alunos"
    subtitle = "Gerencie os alunos cadastrados"
    breadcrumbs = [
        {'name': 'Dashboard', 'url': 'dashboard', 'active': False},
        {'name': 'Alunos', 'url': None, 'active': True}
    ]
    
    def get_queryset(self):
        return Student.objects.select_related('course').all()


class StudentCreateView(TitleMixin, BreadcrumbMixin, FormMessageMixin, SuccessMessageMixin, CreateView):
    """Criar novo aluno"""
    model = Student
    form_class = StudentForm
    template_name = 'people/student_form.html'
    success_url = reverse_lazy('people:student_list')
    title = "Novo Aluno"
    subtitle = "Preencha os dados do novo aluno"
    success_message_create = "Aluno cadastrado com sucesso!"
    breadcrumbs = [
        {'name': 'Dashboard', 'url': 'dashboard', 'active': False},
        {'name': 'Alunos', 'url': 'people:student_list', 'active': False},
        {'name': 'Novo Aluno', 'url': None, 'active': True}
    ]
    
    def get_success_message(self, cleaned_data):
        return super().get_success_message('create')
    
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)


class StudentUpdateView(TitleMixin, BreadcrumbMixin, FormMessageMixin, SuccessMessageMixin, UpdateView):
    """Editar aluno existente"""
    model = Student
    form_class = StudentForm
    template_name = 'people/student_form.html'
    success_url = reverse_lazy('people:student_list')
    title = "Editar Aluno"
    subtitle = "Atualize as informações do aluno"
    success_message_update = "Aluno atualizado com sucesso!"
    breadcrumbs = [
        {'name': 'Dashboard', 'url': 'dashboard', 'active': False},
        {'name': 'Alunos', 'url': 'people:student_list', 'active': False},
        {'name': 'Editar Aluno', 'url': None, 'active': True}
    ]
    
    def get_success_message(self, cleaned_data):
        return super().get_success_message('update')
    
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.updated_by = self.request.user
        return super().form_valid(form)


class StudentDeleteView(TitleMixin, BreadcrumbMixin, FormMessageMixin, SuccessMessageMixin, DeleteView):
    """Deletar aluno"""
    model = Student
    template_name = 'people/student_confirm_delete.html'
    success_url = reverse_lazy('people:student_list')
    title = "Excluir Aluno"
    subtitle = "Confirme a exclusão do aluno"
    success_message_delete = "Aluno excluído com sucesso!"
    breadcrumbs = [
        {'name': 'Dashboard', 'url': 'dashboard', 'active': False},
        {'name': 'Alunos', 'url': 'people:student_list', 'active': False},
        {'name': 'Excluir Aluno', 'url': None, 'active': True}
    ]
    
    def get_success_message(self, cleaned_data):
        return super().get_success_message('delete')