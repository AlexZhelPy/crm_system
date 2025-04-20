"""
Модуль models для работы с услугами.

Содержит модель Service для хранения информации об услугах компании.
"""

from django.db import models
from typing import ClassVar

class Service(models.Model):
    """
    Модель услуги.

    Атрибуты:
        name (str): Название услуги
        description (str): Описание
        price (Decimal): Цена
        created_at (DateTime): Дата создания
        updated_at (DateTime): Дата обновления
    """

    name: str = models.CharField(max_length=255)
    description: str = models.TextField()
    price: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Строковое представление услуги."""
        return str(self.name)

    class Meta:
        """Мета-класс для дополнительных настроек модели."""

        verbose_name: ClassVar[str] = "Service"
        verbose_name_plural: ClassVar[str] = "Services"
