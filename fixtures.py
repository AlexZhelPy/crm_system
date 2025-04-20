from django.contrib.auth import get_user_model
from crm.models.services import Service
from crm.models.campaigns import Campaign
from crm.models.leads import Lead
from crm.models.contracts import Contract
from crm.models.clients import Client

User = get_user_model()


def create_test_data():
    # Очищаем таблицы (более надежный способ)
    Client.objects.all().delete()
    Contract.objects.all().delete()
    Lead.objects.all().delete()
    Campaign.objects.all().delete()
    Service.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()  # Удаляем всех, кроме суперпользователя

    # Создаем пользователей, используя get_or_create
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}
    )
    if created:
        admin.set_password('admin123')
        admin.save()

    marketer, created = User.objects.get_or_create(
        username='marketer',
        defaults={'email': 'marketer@example.com'}
    )
    if created:
        marketer.set_password('marketer123')
        marketer.save()

    manager, created = User.objects.get_or_create(
        username='manager',
        defaults={'email': 'manager@example.com'}
    )
    if created:
        manager.set_password('manager123')
        manager.save()

    # Создаем услуги
    service1 = Service.objects.create(name="SEO продвижение", description="Полное SEO продвижение сайта", price=50000)
    service2 = Service.objects.create(name="Контекстная реклама", description="Настройка и ведение рекламы", price=30000)

    # Создаем кампании
    campaign1 = Campaign.objects.create(name="Летний набор", service=service1, channel="google", budget=100000)
    campaign2 = Campaign.objects.create(name="Новогодняя акция", service=service2, channel="yandex", budget=150000)

    # Создаем лидов
    lead1 = Lead.objects.create(full_name="Иван Иванов", phone="+79000000000", email="ivan@example.com", campaign=campaign1)
    lead2 = Lead.objects.create(full_name="Петр Петров", phone="+79167654321", email="petr@example.com", campaign=campaign2)

    # Создаем договоры
    contract1 = Contract.objects.create(name="Договор 1", service=service1, document="path/to/document1.pdf", start_date="2023-01-01", end_date="2023-12-31", amount=50000)
    contract2 = Contract.objects.create(name="Договор 2", service=service2, document="path/to/document2.pdf", start_date="2023-02-01", end_date="2023-11-30", amount=30000)

    print("Тестовые данные успешно созданы!")
