"""
Модуль models для работы с договорами.
Содержит модель Contract для хранения информации о договорах с клиентами.
"""

from django.db import models
from .services import Service
from typing import ClassVar


class Contract(models.Model):
    """
    Модель договора с клиентом.

    Атрибуты:
        name (str): Название договора
        service (Service): Связанная услуга
        document (File): Файл договора
        start_date (Date): Дата начала действия
        end_date (Date): Дата окончания
        amount (Decimal): Сумма договора
        created_at (DateTime): Дата создания
        updated_at (DateTime): Дата обновления
    """

    name: str = models.CharField(max_length=255)
    service: models.ForeignKey = models.ForeignKey(Service, on_delete=models.PROTECT)
    document: models.FileField = models.FileField(upload_to='contracts/')
    start_date: models.DateField = models.DateField()
    end_date: models.DateField = models.DateField()
    amount: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Строковое представление договора."""
        return str(self.name)

    class Meta:
        """Мета-класс для дополнительных настроек модели."""
        verbose_name: ClassVar[str] = 'Contract'
        verbose_name_plural: ClassVar[str] = 'Contracts'
