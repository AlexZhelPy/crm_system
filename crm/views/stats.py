"""Views для работы со статистикой."""

from django.views.generic import TemplateView
from django.db.models import Count, Sum, F, Prefetch
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from typing import Dict, Any

from crm.models.campaigns import Campaign
from crm.models.leads import Lead
from crm.models.clients import Client
from services.logging_utils import log_success, log_warning, log_error


class CampaignStatsView(LoginRequiredMixin, TemplateView):
    """
    Представление для отображения статистики по маркетинговым кампаниям.
    Показывает количество лидов, конвертированных клиентов и ROI для каждой кампании.
    Доступно только для авторизованных пользователей.
    """
    template_name = 'crm/campaign_stats.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Формирует контекст данных для отображения статистики кампаний.
        Включает оптимизированные запросы к базе данных и обработку ошибок.

        Возвращает:
            dict: Контекст данных с информацией о кампаниях и их статистике
        """
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        user = self.request.user

        try:
            # Оптимизированные запросы с использованием select_related и prefetch_related
            campaigns = Campaign.objects.select_related('service').prefetch_related(
                Prefetch(
                    'lead_set',
                    queryset=Lead.objects.select_related('campaign').prefetch_related(
                        Prefetch(
                            'client',
                            queryset=Client.objects.select_related('contract', 'lead')
                        )
                    ),
                    to_attr='prefetched_leads'
                )
            ).annotate(
                lead_count=Count('lead'),
                client_count=Count('lead__client'),
                roi=Sum(F('lead__client__contract__amount') - F('budget'))
            ).order_by('-created_at')  # Сортировка по дате создания вместо start_date

            # Расчет коэффициента конверсии с проверкой деления на ноль
            for campaign in campaigns:
                campaign.conversion_rate = (
                            campaign.client_count * 100.0 / campaign.lead_count) if campaign.lead_count > 0 else 0
                campaign.conversion_rate = round(campaign.conversion_rate, 1)  # Округляем до 1 знака после запятой

            context['campaigns'] = campaigns

            # Дополнительная агрегация для общей статистики
            total_stats = {
                'total_leads': sum(c.lead_count for c in campaigns),
                'total_clients': sum(c.client_count for c in campaigns),
                'total_roi': sum(c.roi for c in campaigns if c.roi is not None),
                'avg_conversion': (sum(c.conversion_rate for c in campaigns) / len(campaigns)) if campaigns else 0
            }
            context.update(total_stats)

            log_success(f"Пользователь {user} успешно загрузил статистику кампаний")
            return context

        except Exception as e:
            log_error(f"Ошибка при расчете статистики кампаний пользователем {user}: {str(e)}")
            messages.error(self.request, 'Произошла ошибка при загрузке статистики кампаний.')
            return context
