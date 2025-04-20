"""
Модуль models для работы с потенциальными клиентами (лидами).

Содержит модель Lead для хранения информации о потенциальных клиентах.
"""

from .campaigns import Campaign
from django.db import models
from typing import ClassVar

class Lead(models.Model):
    """
    Модель потенциального клиента (лида).

    Атрибуты:
        full_name (str): Полное имя
        phone (str): Телефон
        email (str): Email
        campaign (Campaign): Связанная кампания
        is_converted (bool): Флаг конвертации в клиента
        created_at (DateTime): Дата создания
        updated_at (DateTime): Дата обновления
    """

    full_name: str = models.CharField(max_length=255)
    phone: str = models.CharField(max_length=20)
    email: models.EmailField = models.EmailField()
    campaign: models.ForeignKey = models.ForeignKey(Campaign, on_delete=models.PROTECT)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    is_converted: bool = models.BooleanField(default=False)

    def __str__(self) -> str:
        """Строковое представление лида."""
        return f"Lead {self.full_name}"

    class Meta:
        """Мета-класс для дополнительных настроек модели."""

        verbose_name: ClassVar[str] = "Potential Client"
        verbose_name_plural: ClassVar[str] = "Potential Clients"
