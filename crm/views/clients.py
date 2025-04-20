"""Views для работы с клиентами."""

from crm.forms import ClientForm
from crm.models.clients import Client
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, UpdateView
from services.logging_utils import log_error, log_success, log_warning
from typing import Any, Type

class ClientListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка клиентов.

    Доступно только для авторизованных пользователей.
    """

    model: Type[Client] = Client
    template_name: str = "crm/client_list.html"
    context_object_name: str = "clients"
    queryset: QuerySet[Client] = Client.objects.select_related("lead")

    def get_queryset(self) -> QuerySet[Client]:
        """Возвращает queryset клиентов с обработкой возможных ошибок."""
        try:
            return super().get_queryset()
        except Exception as e:
            log_error(f"Ошибка при загрузке списка клиентов пользователем {self.request.user}: {str(e)}")
            messages.error(self.request, "Произошла ошибка при загрузке списка клиентов.")
            return Client.objects.none()


class ClientDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для детального просмотра информации о клиенте.

    Доступно только для авторизованных пользователей.
    """

    model: Type[Client] = Client
    template_name: str = "crm/client_detail.html"
    context_object_name: str = "client"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Обрабатывает GET-запрос с логированием и обработкой ошибок."""
        try:
            response = super().get(request, *args, **kwargs)
            client = self.object
            # Используем строковое представление клиента или конкретные поля
            log_success(f"Пользователь {request.user} просмотрел клиента {client}")
            return response
        except Exception as e:
            log_error(f"Ошибка при просмотре клиента пользователем {request.user}: {str(e)}")
            messages.error(request, "Произошла ошибка при загрузке данных клиента.")
            return HttpResponseRedirect(reverse("client_list"))


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования данных клиента.

    Доступно только для менеджеров и администраторов.
    """

    model: Type[Client] = Client
    form_class: Type[ClientForm] = ClientForm
    template_name: str = "crm/client_form.html"
    context_object_name: str = "client"
    success_url: str = reverse_lazy("client_list")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Проверяет права пользователя перед обработкой запроса."""
        if not (request.user.is_manager or request.user.is_admin):
            log_warning(f"Пользователь {request.user} попытался редактировать клиента без прав")
            messages.error(request, "У вас недостаточно прав для редактирования клиентов.")
            return HttpResponseRedirect(reverse("client_list"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Обрабатывает валидную форму с логированием успешного обновления."""
        response = super().form_valid(form)
        client = self.object
        log_success(f"Пользователь {self.request.user} обновил данные клиента {client}")
        messages.success(self.request, "Данные клиента успешно обновлены!")
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        """Обрабатывает невалидную форму с логированием ошибок."""
        log_warning(f"Пользователь {self.request.user} не смог обновить данные клиента: {form.errors}")
        messages.error(self.request, "Исправьте ошибки в форме.")
        return super().form_invalid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления клиента.

    Доступно только для менеджеров и администраторов.
    При удалении клиента связанный лид помечается как неконвертированный.
    """

    model: Type[Client] = Client
    template_name: str = "crm/client_confirm_delete.html"
    success_url: str = reverse_lazy("client_list")
    context_object_name: str = "client"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Проверяет права пользователя перед обработкой запроса."""
        if not (request.user.is_manager or request.user.is_admin):
            log_warning(f"Пользователь {request.user} попытался удалить клиента без прав")
            messages.error(request, "У вас недостаточно прав для удаления клиентов.")
            return HttpResponseRedirect(reverse("client_list"))
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Обрабатывает удаление клиента с обновлением связанного лида и логированием."""
        try:
            client = self.get_object()
            lead = client.lead

            response = super().delete(request, *args, **kwargs)

            # Обновляем статус лида
            if lead:
                lead.is_converted = False
                lead.save()
                log_success(f"Пользователь {request.user} удалил клиента {client} и сбросил статус лида")
                messages.success(request, "Клиент успешно удален! Статус лида сброшен.")
            else:
                log_success(f"Пользователь {request.user} удалил клиента {client} (без связанного лида)")
                messages.success(request, "Клиент успешно удален!")

            return response
        except Exception as e:
            log_error(f"Ошибка при удалении клиента пользователем {request.user}: {str(e)}")
            messages.error(request, "Произошла ошибка при удалении клиента.")
            return HttpResponseRedirect(reverse("client_list"))
