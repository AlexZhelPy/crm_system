"""Views для работы с услугами."""

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import reverse
from django.forms import BaseModelForm
from django.db.models import QuerySet

from typing import Any, Type

from crm.models.services import Service
from crm.forms import ServiceForm
from services.logging_utils import log_success, log_warning, log_error


class ServiceListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка услуг.
    Доступно только для авторизованных пользователей.
    """
    model: Type[Service] = Service
    template_name: str = 'crm/service_list.html'
    context_object_name: str = 'services'
    paginate_by = 20  # Оптимизация: добавляем пагинацию для больших списков

    def get_queryset(self) -> QuerySet[Service]:
        """
        Возвращает оптимизированный queryset услуг с обработкой ошибок.
        """
        try:
            return Service.objects.all().order_by('name')
        except Exception as e:
            log_error(f"Ошибка при загрузке списка услуг пользователем {self.request.user}: {str(e)}")
            messages.error(self.request, 'Произошла ошибка при загрузке списка услуг.')
            return Service.objects.none()


class ServiceDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для детального просмотра услуги.
    Доступно только для авторизованных пользователей.
    """
    model: Type[Service] = Service
    template_name: str = 'crm/service_detail.html'
    context_object_name: str = 'service'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Обрабатывает GET-запрос с логированием и обработкой ошибок.
        """
        try:
            response = super().get(request, *args, **kwargs)
            log_success(f"Пользователь {request.user} просмотрел услугу {self.object.name}")
            return response
        except Exception as e:
            log_error(f"Ошибка при просмотре услуги пользователем {request.user}: {str(e)}")
            messages.error(request, 'Произошла ошибка при загрузке данных услуги.')
            return HttpResponseRedirect(reverse('service_list'))


class ServiceCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания новой услуги.
    Доступно только для маркетологов и администраторов.
    """
    model: Type[Service] = Service
    form_class: Type[ServiceForm] = ServiceForm
    template_name: str = 'crm/service_form.html'
    success_url: str = reverse_lazy('service_list')

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Проверяет права пользователя перед обработкой запроса.
        """
        if not (request.user.is_marketer or request.user.is_admin):
            log_warning(f"Пользователь {request.user} попытался создать услугу без прав")
            messages.error(request, 'У вас недостаточно прав для создания услуг.')
            return HttpResponseRedirect(reverse('service_list'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """
        Обрабатывает валидную форму с логированием успешного создания.
        """
        response = super().form_valid(form)
        log_success(f"Пользователь {self.request.user} создал новую услугу: {self.object.name}")
        messages.success(self.request, 'Услуга успешно создана!')
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        """
        Обрабатывает невалидную форму с логированием ошибок.
        """
        log_warning(f"Пользователь {self.request.user} не смог создать услугу: {form.errors}")
        messages.error(self.request, 'Исправьте ошибки в форме.')
        return super().form_invalid(form)


class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования услуги.
    Доступно только для маркетологов и администраторов.
    """
    model: Type[Service] = Service
    form_class: Type[ServiceForm] = ServiceForm
    template_name: str = 'crm/service_form.html'
    success_url: str = reverse_lazy('service_list')

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Проверяет права пользователя перед обработкой запроса.
        """
        if not (request.user.is_marketer or request.user.is_admin):
            log_warning(f"Пользователь {request.user} попытался редактировать услугу без прав")
            messages.error(request, 'У вас недостаточно прав для редактирования услуг.')
            return HttpResponseRedirect(reverse('service_list'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """
        Обрабатывает валидную форму с логированием успешного обновления.
        """
        response = super().form_valid(form)
        log_success(f"Пользователь {self.request.user} обновил услугу {self.object.name}")
        messages.success(self.request, 'Услуга успешно обновлена!')
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        """
        Обрабатывает невалидную форму с логированием ошибок.
        """
        log_warning(f"Пользователь {self.request.user} не смог обновить услугу {self.object.name}: {form.errors}")
        messages.error(self.request, 'Исправьте ошибки в форме.')
        return super().form_invalid(form)


class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления услуги.
    Доступно только для маркетологов и администраторов.
    """
    model: Type[Service] = Service
    template_name: str = 'crm/service_confirm_delete.html'
    success_url: str = reverse_lazy('service_list')

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Проверяет права пользователя перед обработкой запроса.
        """
        if not (request.user.is_marketer or request.user.is_admin):
            log_warning(f"Пользователь {request.user} попытался удалить услугу без прав")
            messages.error(request, 'У вас недостаточно прав для удаления услуг.')
            return HttpResponseRedirect(reverse('service_list'))
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Обрабатывает удаление услуги с логированием.
        """
        try:
            service = self.get_object()
            service_name = service.name
            response = super().delete(request, *args, **kwargs)
            log_success(f"Пользователь {request.user} удалил услугу {service_name}")
            messages.success(request, 'Услуга успешно удалена!')
            return response
        except Exception as e:
            log_error(f"Ошибка при удалении услуги пользователем {request.user}: {str(e)}")
            messages.error(request, 'Произошла ошибка при удалении услуги.')
            return HttpResponseRedirect(reverse('service_detail', kwargs={'pk': self.get_object().pk}))
