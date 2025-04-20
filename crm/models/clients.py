"""
Модель Client представляет активного клиента в системе.

Связывает лида (потенциального клиента) с заключенным договором.
"""

from .leads import Lead
from django.db import models
from typing import ClassVar

class Client(models.Model):
    """
    Модель активного клиента.

    Атрибуты:
        lead (OneToOneField): Связанный объект лида (потенциального клиента)
        contract (ForeignKey): Заключенный договор с клиентом
        created_at (DateTime): Дата создания записи
        updated_at (DateTime): Дата последнего обновления
    """

    lead: models.OneToOneField = models.OneToOneField(Lead, on_delete=models.PROTECT)
    contract: models.ForeignKey = models.ForeignKey("Contract", on_delete=models.PROTECT)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Строковое представление клиента."""
        return f"Client {self.lead.full_name}"

    # pylint: disable=too-few-public-methods
    class Meta:
        """Мета-класс для дополнительных настроек модели."""

        verbose_name: ClassVar[str] = "Active Client"
        verbose_name_plural: ClassVar[str] = "Active Clients"
