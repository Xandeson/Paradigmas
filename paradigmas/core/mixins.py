from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.base import ContextMixin


class AuditMixin:
    """Mixin para adicionar informações de auditoria aos modelos"""
    
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            if hasattr(form.instance, 'created_by') and not form.instance.pk:
                form.instance.created_by = self.request.user
            if hasattr(form.instance, 'updated_by'):
                form.instance.updated_by = self.request.user
        return super().form_valid(form)


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """Mixin customizado para login obrigatório com mensagem personalizada"""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Você precisa estar logado para acessar esta página.')
            return redirect('admin:login')
        return super().dispatch(request, *args, **kwargs)


class PermissionMixin:
    """Mixin para verificação de permissões"""
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            messages.error(request, 'Você não tem permissão para realizar esta ação.')
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def has_permission(self):
        """Override este método nas views filhas"""
        return True


class TitleMixin(ContextMixin):
    """Mixin para adicionar título às páginas automaticamente"""
    title = None
    subtitle = None
    
    def get_title(self):
        """Retorna o título da página"""
        return self.title
    
    def get_subtitle(self):
        """Retorna o subtítulo da página"""
        return self.subtitle
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.get_title()
        context['page_subtitle'] = self.get_subtitle()
        return context


class BreadcrumbMixin(ContextMixin):
    """Mixin para adicionar breadcrumbs às páginas"""
    breadcrumbs = []
    
    def get_breadcrumbs(self):
        """Retorna a lista de breadcrumbs"""
        return self.breadcrumbs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breadcrumbs()
        return context


class FormMessageMixin:
    """Mixin para mensagens personalizadas em formulários"""
    success_message_create = "Item criado com sucesso!"
    success_message_update = "Item atualizado com sucesso!"
    success_message_delete = "Item excluído com sucesso!"
    
    def get_success_message(self, action='create'):
        """Retorna a mensagem de sucesso baseada na ação"""
        messages_map = {
            'create': self.success_message_create,
            'update': self.success_message_update,
            'delete': self.success_message_delete,
        }
        return messages_map.get(action, self.success_message_create)


class ModelInfoMixin(ContextMixin):
    """Mixin para adicionar informações do modelo ao contexto"""
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'model') and self.model:
            context['model_name'] = self.model._meta.verbose_name
            context['model_name_plural'] = self.model._meta.verbose_name_plural
        return context