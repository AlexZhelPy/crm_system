"""
Модель Campaign представляет маркетинговую кампанию в системе.
Содержит информацию о названии, связанной услуге, канале продвижения и бюджете.
"""

from django.db import models
from .services import Service
from typing import ClassVar

class Campaign(models.Model):
    """
        Модель маркетинговой кампании.

        Атрибуты:
            name (str): Название кампании
            service (Service): Связанная услуга
            channel (str): Канал продвижения
            budget (Decimal): Бюджет кампании
            created_at (DateTime): Дата создания
            updated_at (DateTime): Дата последнего обновления
    """

    name: str = models.CharField(max_length=255)
    service: models.ForeignKey = models.ForeignKey(Service, on_delete=models.PROTECT)
    channel: str = models.CharField(max_length=100)
    budget: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Строковое представление кампании."""
        return str(self.name)

    # pylint: disable=too-few-public-methods
    class Meta:
        """Мета-класс для дополнительных настроек модели."""
        verbose_name: ClassVar[str] = 'Campaign'
        verbose_name_plural: ClassVar[str] = 'Campaigns'
