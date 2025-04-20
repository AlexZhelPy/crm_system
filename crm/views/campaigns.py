"""Views для работы с маркетинговыми кампаниями."""

from crm.forms import CampaignForm
from crm.models.campaigns import Campaign
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from services.logging_utils import log_error, log_success, log_warning
from typing import Any, Type

class CampaignListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка маркетинговых кампаний.

    Доступно только для авторизованных пользователей.
    """

    model: Type[Campaign] = Campaign
    template_name: str = "crm/campaign_list.html"
    context_object_name: str = "campaigns"
    queryset: QuerySet[Campaign] = Campaign.objects.all()

    def get_queryset(self) -> QuerySet[Campaign]:
        """Возвращает queryset кампаний с обработкой возможных ошибок."""
        try:
            return super().get_queryset()
        except Exception as e:
            log_error(f"Ошибка при получении списка кампаний пользователем {self.request.user}: {str(e)}")
            messages.error(self.request, "Произошла ошибка при загрузке списка кампаний.")
            return Campaign.objects.none()


class CampaignDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для детального просмотра информации о кампании.

    Доступно только для авторизованных пользователей.
    """

    model: Type[Campaign] = Campaign
    template_name: str = "crm/campaign_detail.html"
    context_object_name: str = "campaign"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Обрабатывает GET-запрос с логированием и обработкой ошибок."""
        try:
            response = super().get(request, *args, **kwargs)
            log_success(f"Пользователь {request.user} просмотрел кампанию {self.object.name}")
            return response
        except Exception as e:
            log_error(f"Ошибка при просмотре кампании пользователем {request.user}: {str(e)}")
            messages.error(request, "Произошла ошибка при загрузке данных кампании.")
            return HttpResponseRedirect(reverse("campaign_list"))


class CampaignCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания новой кампании.

    Доступно только для маркетеров и администраторов.
    """

    model: Type[Campaign] = Campaign
    form_class: Type[CampaignForm] = CampaignForm
    template_name: str = "crm/campaign_form.html"
    success_url: str = reverse_lazy("campaign_list")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Проверяет права пользователя перед обработкой запроса."""
        if not (request.user.is_marketer or request.user.is_admin):
            log_warning(f"Пользователь {request.user} попытался создать кампанию без прав")
            messages.error(request, "У вас недостаточно прав для создания кампаний.")
            return HttpResponseRedirect(reverse("campaign_list"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Обрабатывает валидную форму с логированием успешного создания."""
        response = super().form_valid(form)
        log_success(f"Пользователь {self.request.user} создал кампанию: {self.object.name}")
        messages.success(self.request, "Кампания успешно создана!")
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        """Обрабатывает невалидную форму с логированием ошибок."""
        log_warning(f"Пользователь {self.request.user} не смог создать кампанию: {form.errors}")
        messages.error(self.request, "Исправьте ошибки в форме.")
        return super().form_invalid(form)


class CampaignUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования существующей кампании.

    Доступно только для маркетеров и администраторов.
    """

    model: Type[Campaign] = Campaign
    form_class: Type[CampaignForm] = CampaignForm
    template_name: str = "crm/campaign_form.html"
    success_url: str = reverse_lazy("campaign_list")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Проверяет права пользователя перед обработкой запроса."""
        if not (request.user.is_marketer or request.user.is_admin):
            log_warning(f"Пользователь {request.user} попытался редактировать кампанию без прав")
            messages.error(request, "У вас недостаточно прав для редактирования кампаний.")
            return HttpResponseRedirect(reverse("campaign_list"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Обрабатывает валидную форму с логированием успешного обновления."""
        response = super().form_valid(form)
        log_success(f"Пользователь {self.request.user} обновил кампанию: {self.object.name}")
        messages.success(self.request, "Кампания успешно обновлена!")
        return response

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        """Обрабатывает невалидную форму с логированием ошибок."""
        log_warning(
            f"Пользователь {self.request.user} не смог обновить кампанию {self.get_object().name}: {form.errors}"
        )
        messages.error(self.request, "Исправьте ошибки в форме.")
        return super().form_invalid(form)


class CampaignDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления кампании.

    Доступно только для маркетеров и администраторов.
    """

    model: Type[Campaign] = Campaign
    template_name: str = "crm/campaign_confirm_delete.html"
    success_url: str = reverse_lazy("campaign_list")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Проверяет права пользователя перед обработкой запроса."""
        if not (request.user.is_marketer or request.user.is_admin):
            log_warning(f"Пользователь {request.user} попытался удалить кампанию без прав")
            messages.error(request, "У вас недостаточно прав для удаления кампаний.")
            return HttpResponseRedirect(reverse("campaign_list"))
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Обрабатывает удаление кампании с логированием."""
        try:
            campaign = self.get_object()
            campaign_name = campaign.name
            response = super().delete(request, *args, **kwargs)
            log_success(f"Пользователь {request.user} удалил кампанию: {campaign_name}")
            messages.success(request, "Кампания успешно удалена!")
            return response
        except Exception as e:
            log_error(f"Ошибка при удалении кампании пользователем {request.user}: {str(e)}")
            messages.error(request, "Произошла ошибка при удалении кампании.")
            return HttpResponseRedirect(reverse("campaign_list"))
