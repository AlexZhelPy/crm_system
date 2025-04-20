"""Модуль моделей для приложения accounts.

Содержит модели пользователей системы и связанные с ними настройки.
"""


from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    """Модель пользователя системы с расширенными возможностями.

    Наследует стандартную модель пользователя Django и добавляет:
    - Ролевую систему
    - Кастомные permissions
    - Методы проверки ролей
    """

    class Role(models.TextChoices):
        """Роли пользователей в системе."""

        ADMIN = "ADMIN", "Administrator"
        OPERATOR = "OPERATOR", "Operator"
        MARKETER = "MARKETER", "Marketer"
        MANAGER = "MANAGER", "Manager"

    role: str = models.CharField(max_length=10, choices=Role.choices, default=Role.OPERATOR)

    groups: models.ManyToManyField = models.ManyToManyField(
        Group,
        related_name="accounts_user_set",
        blank=True,
        help_text="Группы, к которым принадлежит пользователь. Пользователь получает все права своих групп.",
        verbose_name="groups",
    )
    user_permissions: models.ManyToManyField = models.ManyToManyField(
        Permission,
        related_name="accounts_user_set",
        blank=True,
        help_text="Конкретные права для этого пользователя.",
        verbose_name="user permissions",
    )

    @property
    def is_admin(self) -> bool:
        """Проверяет, является ли пользователь администратором."""
        return self.role == self.Role.ADMIN

    @property
    def is_operator(self) -> bool:
        """Проверяет, является ли пользователь оператором."""
        return self.role == self.Role.OPERATOR

    @property
    def is_marketer(self) -> bool:
        """Проверяет, является ли пользователь маркетологом."""
        return self.role == self.Role.MARKETER

    @property
    def is_manager(self) -> bool:
        """Проверяет, является ли пользователь менеджером."""
        return self.role == self.Role.MANAGER

    class Meta:
        """Мета-класс для настройки модели User."""

        verbose_name: str = "Пользователь"
        verbose_name_plural: str = "Пользователи"

    def __str__(self) -> str:
        """Строковое представление пользователя."""
        return str(self.username)
