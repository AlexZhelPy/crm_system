"""Views для работы с потенциальными клиентами (лидами)."""

from crm.forms import ClientForm, LeadForm
from crm.models.contracts import Contract
from crm.models.leads import Lead
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from services.logging_utils import log_error, log_success, log_warning
from typing import Any, Dict, Type

class LeadListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка потенциальных клиентов (лидов).

    Доступно только для авторизованных пользователей.
    """

    model: Type[Lead] = Lead
    template_name: str = "crm/lead_list.html"
    context_object_name: str = "leads"
    queryset = Lead.objects.select_related("campaign")  # Оптимизация: уменьшаем количество запросов к БД

    def get_queryset(self) -> QuerySet[Lead]:
        """Возвращает queryset лидов с обработкой возможных ошибок."""
        try:
            return super().get_queryset()
        except Exception as e:
            log_error(f"Ошибка при загрузке списка лидов пользователем {self.request.user}: {str(e)}")
            messages.error(self.request, "Произошла ошибка при загрузке списка потенциальных клиентов.")
            return Lead.objects.none()


class LeadDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для детального просмотра информации о потенциальном клиенте (лиде).

    Доступно только для авторизованных пользователей.
    """

    model: Type[Lead] = Lead
    template_name: str = "crm/lead_detail.html"
    context_object_name: str = "lead"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Обрабатывает GET-запрос с логированием и обработкой ошибок."""
        try:
            response = super().get(request, *args, **kwargs)
            log_success(f"Пользователь {request.user} просмотрел лида {self.object}")
            return response
        except Exception as e:
            log_error(f"Ошибка при просмотре лида пользователем {request.user}: {str(e)}")
            messages.error(request, "Произошла ошибка при загрузке данных потенциального клиента.")
            return HttpResponseRedirect(reverse("lead_list"))


class LeadCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания нового лида.

    Доступно только для операторов и администраторов.
    """

    model: Type[Lead] = Lead
    form_class: Type[LeadForm] = LeadForm
    template_name: str = "crm/lead_form.html"
    success_url = reverse_lazy("lead_list")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Проверяет права пользователя перед обработкой запроса."""
        if not (request.user.is_operator or request.user.is_admin):
            log_warning(f"Пользователь {request.user} попытался создать лид без прав")
            messages.error(request, "У вас недостаточно прав для создания потенциальных клиентов.")
            return HttpResponseRedirect(reverse("lead_list"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Обрабатывает валидную форму с логированием успешного создания."""
        response = super().form_valid(form)
        log_success(f"Пользователь {self.request.user} создал новый лид: {self.object}")
        messages.success(self.request, "Потенциальный клиент успешно создан!")
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        """Обрабатывает невалидную форму с логированием ошибок."""
        log_warning(f"Пользователь {self.request.user} не смог создать лид: {form.errors}")
        messages.error(self.request, "Исправьте ошибки в форме.")
        return super().form_invalid(form)


class LeadUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования лида.

    Доступно только для операторов и администраторов.
    """

    model: Type[Lead] = Lead
    form_class: Type[LeadForm] = LeadForm
    template_name: str = "crm/lead_form.html"
    success_url = reverse_lazy("lead_list")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Проверяет права пользователя перед обработкой запроса."""
        if not (request.user.is_operator or request.user.is_admin):
            log_warning(f"Пользователь {request.user} попытался редактировать лид без прав")
            messages.error(request, "У вас недостаточно прав для редактирования потенциальных клиентов.")
            return HttpResponseRedirect(reverse("lead_list"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Обрабатывает валидную форму с логированием успешного обновления."""
        response = super().form_valid(form)
        log_success(f"Пользователь {self.request.user} обновил лида {self.object}")
        messages.success(self.request, "Данные потенциального клиента успешно обновлены!")
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        """Обрабатывает невалидную форму с логированием ошибок."""
        log_warning(f"Пользователь {self.request.user} не смог обновить лида {self.object}: {form.errors}")
        messages.error(self.request, "Исправьте ошибки в форме.")
        return super().form_invalid(form)


class LeadDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления лида.

    Доступно только для операторов и администраторов.
    """

    model: Type[Lead] = Lead
    template_name: str = "crm/lead_confirm_delete.html"
    success_url: str = reverse_lazy("lead_list")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Проверяет права пользователя перед обработкой запроса."""
        if not (request.user.is_operator or request.user.is_admin):
            log_warning(f"Пользователь {request.user} попытался удалить лид без прав")
            messages.error(request, "У вас недостаточно прав для удаления потенциальных клиентов.")
            return HttpResponseRedirect(reverse("lead_list"))
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Обрабатывает удаление лида с логированием."""
        try:
            lead = self.get_object()
            lead_str = str(lead)
            response = super().delete(request, *args, **kwargs)
            log_success(f"Пользователь {request.user} удалил лида {lead_str}")
            messages.success(request, "Потенциальный клиент успешно удален!")
            return response
        except Exception as e:
            log_error(f"Ошибка при удалении лида пользователем {request.user}: {str(e)}")
            messages.error(request, "Произошла ошибка при удалении потенциального клиента.")
            return HttpResponseRedirect(reverse("lead_list"))


class LeadConvertView(LoginRequiredMixin, DetailView):
    """
    Представление для конвертации лида в активного клиента.

    Доступно только для менеджеров и администраторов.
    """

    model: Type[Lead] = Lead
    template_name: str = "crm/lead_convert.html"
    context_object_name: str = "lead"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Проверяет права пользователя перед обработкой запроса."""
        if not (request.user.is_manager or request.user.is_admin):
            log_warning(f"Пользователь {request.user} попытался конвертировать лид без прав")
            messages.error(request, "У вас недостаточно прав для конвертации потенциальных клиентов.")
            return HttpResponseRedirect(reverse("lead_list"))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Добавляет в контекст список договоров и форму для создания клиента."""
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["contracts"] = Contract.objects.all()
        context["form"] = ClientForm(initial={"lead": self.object})
        return context

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Обрабатывает конвертацию лида в клиента."""
        lead = self.get_object()
        form = ClientForm(request.POST)

        try:
            if form.is_valid():
                client = form.save(commit=False)
                client.lead = lead
                client.save()

                lead.is_converted = True
                lead.save()

                log_success(f"Пользователь {request.user} конвертировал лида {lead} в клиента {client}")
                messages.success(request, "Потенциальный клиент успешно конвертирован в активного клиента!")
                return redirect("client_list")

            log_warning(f"Пользователь {request.user} не смог конвертировать лида {lead}: {form.errors}")
            messages.error(request, "Ошибка при конвертации. Проверьте данные формы.")
            return self.render_to_response(self.get_context_data(form=form))

        except Exception as e:
            log_error(f"Ошибка при конвертации лида пользователем {request.user}: {str(e)}")
            messages.error(request, "Произошла ошибка при конвертации потенциального клиента.")
            return HttpResponseRedirect(reverse("lead_detail", kwargs={"pk": lead.pk}))
