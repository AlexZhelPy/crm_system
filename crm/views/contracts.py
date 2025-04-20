"""Views для работы с договорами."""

from crm.forms import ContractForm
from crm.models.contracts import Contract
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from services.logging_utils import log_error, log_success, log_warning
from typing import Any, Type

class ContractListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка договоров.

    Доступно только для авторизованных пользователей.
    """

    model: Type[Contract] = Contract
    template_name: str = "crm/contract_list.html"
    context_object_name: str = "contracts"

    def get_queryset(self) -> QuerySet[Contract]:
        """Возвращает оптимизированный queryset договоров с обработкой ошибок."""
        try:
            # Используем только существующие связи (service)
            return Contract.objects.select_related("service")
        except Exception as e:
            log_error(f"Ошибка при загрузке списка договоров пользователем {self.request.user}: {str(e)}")
            messages.error(self.request, "Произошла ошибка при загрузке списка договоров.")
            return Contract.objects.none()


class ContractDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для детального просмотра договора.

    Доступно только для авторизованных пользователей.
    """

    model: Type[Contract] = Contract
    template_name: str = "crm/contract_detail.html"
    context_object_name: str = "contract"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Обрабатывает GET-запрос с логированием и обработкой ошибок."""
        try:
            response = super().get(request, *args, **kwargs)
            log_success(f"Пользователь {request.user} просмотрел договор {self.object}")
            return response
        except Exception as e:
            log_error(f"Ошибка при просмотре договора пользователем {request.user}: {str(e)}")
            messages.error(request, "Произошла ошибка при загрузке данных договора.")
            return HttpResponseRedirect(reverse("contract_list"))


class ContractCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания нового договора.

    Доступно только для менеджеров и администраторов.
    """

    model: Type[Contract] = Contract
    form_class: Type[ContractForm] = ContractForm
    template_name: str = "crm/contract_form.html"
    success_url: str = reverse_lazy("contract_list")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Проверяет права пользователя перед обработкой запроса."""
        if not (request.user.is_manager or request.user.is_admin):
            log_warning(f"Пользователь {request.user} попытался создать договор без прав")
            messages.error(request, "У вас недостаточно прав для создания договоров.")
            return HttpResponseRedirect(reverse("contract_list"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Обрабатывает валидную форму с логированием успешного создания."""
        contract = form.save(commit=False)
        contract.manager = self.request.user
        contract.save()
        form.save_m2m()  # Сохраняем связи many-to-many

        log_success(f"Пользователь {self.request.user} создал договор {contract}")
        messages.success(self.request, "Договор успешно создан!")
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        """Обрабатывает невалидную форму с логированием ошибок."""
        log_warning(f"Пользователь {self.request.user} не смог создать договор: {form.errors}")
        messages.error(self.request, "Исправьте ошибки в форме.")
        return super().form_invalid(form)


class ContractUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования договора.

    Доступно только для менеджеров и администраторов.
    """

    model: Type[Contract] = Contract
    form_class: Type[ContractForm] = ContractForm
    template_name: str = "crm/contract_form.html"
    success_url: str = reverse_lazy("contract_list")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Проверяет права пользователя перед обработкой запроса."""
        if not (request.user.is_manager or request.user.is_admin):
            log_warning(f"Пользователь {request.user} попытался редактировать договор без прав")
            messages.error(request, "У вас недостаточно прав для редактирования договоров.")
            return HttpResponseRedirect(reverse("contract_list"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Обрабатывает валидную форму с логированием успешного обновления."""
        response = super().form_valid(form)
        log_success(f"Пользователь {self.request.user} обновил договор {self.object}")
        messages.success(self.request, "Договор успешно обновлен!")
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        """Обрабатывает невалидную форму с логированием ошибок."""
        log_warning(f"Пользователь {self.request.user} не смог обновить договор {self.object}: {form.errors}")
        messages.error(self.request, "Исправьте ошибки в форме.")
        return super().form_invalid(form)


class ContractDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления договора.

    Доступно только для менеджеров и администраторов.
    """

    model: Type[Contract] = Contract
    template_name: str = "crm/contract_confirm_delete.html"
    success_url: str = reverse_lazy("contract_list")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Проверяет права пользователя перед обработкой запроса."""
        if not (request.user.is_manager or request.user.is_admin):
            log_warning(f"Пользователь {request.user} попытался удалить договор без прав")
            messages.error(request, "У вас недостаточно прав для удаления договоров.")
            return HttpResponseRedirect(reverse("contract_list"))
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Обрабатывает удаление договора с логированием."""
        try:
            contract = self.get_object()
            contract_str = str(contract)
            response = super().delete(request, *args, **kwargs)
            log_success(f"Пользователь {request.user} удалил договор {contract_str}")
            messages.success(request, "Договор успешно удален!")
            return response
        except Exception as e:
            log_error(f"Ошибка при удалении договора пользователем {request.user}: {str(e)}")
            messages.error(request, "Произошла ошибка при удалении договора.")
            return HttpResponseRedirect(reverse("contract_list"))
