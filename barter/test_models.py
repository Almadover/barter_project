import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, Ad, ExchangeProposal

@pytest.mark.django_db
def test_create_ad():
    user = User.objects.create_user(username='testuser', password='testpass')
    cat = Category.objects.create(name="Электроника")
    ad = Ad.objects.create(
        user=user,
        title="Продам ноутбук",
        description="Состояние отличное",
        category=cat,
        condition='new'
    )
    assert ad.title == "Продам ноутбук"
    assert ad.user.username == "testuser"
    assert ad.category.name == "Электроника"
    assert ad.condition == "new"

@pytest.mark.django_db
def test_create_category():
    cat = Category.objects.create(name="Игрушки")
    assert cat.name == "Игрушки"

@pytest.mark.django_db
def test_ad_str():
    user = User.objects.create_user(username='user2', password='secret')
    cat = Category.objects.create(name="Книги")
    ad = Ad.objects.create(
        user=user,
        title="Продам книгу",
        description="Как новая",
        category=cat,
        condition="used"
    )
    assert "Продам книгу" in str(ad)

@pytest.mark.django_db
def test_user_multiple_ads():
    user = User.objects.create_user(username='user3', password='pass123')
    cat = Category.objects.create(name="Мебель")
    ad1 = Ad.objects.create(
        user=user,
        title="Стол",
        description="Деревянный",
        category=cat,
        condition="used"
    )
    ad2 = Ad.objects.create(
        user=user,
        title="Стул",
        description="Пластиковый",
        category=cat,
        condition="new"
    )
    assert Ad.objects.filter(user=user).count() == 2

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, Ad

@pytest.mark.django_db
def test_ad_str():
    user = User.objects.create_user(username='user2', password='secret')
    cat = Category.objects.create(name="Книги")
    ad = Ad.objects.create(
        user=user,
        title="Продам книгу",
        description="Как новая",
        category=cat,
        condition="used"
    )
    assert "Продам книгу" in str(ad)

@pytest.mark.django_db
def test_user_multiple_ads():
    user = User.objects.create_user(username='user3', password='pass123')
    cat = Category.objects.create(name="Мебель")
    ad1 = Ad.objects.create(
        user=user,
        title="Стол",
        description="Деревянный",
        category=cat,
        condition="used"
    )
    ad2 = Ad.objects.create(
        user=user,
        title="Стул",
        description="Пластиковый",
        category=cat,
        condition="new"
    )
    assert Ad.objects.filter(user=user).count() == 2

@pytest.mark.django_db
def test_register_view_get(client):
    url = reverse('register')  # предполагается, что в urls.py name='register'
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context

@pytest.mark.django_db
def test_register_view_post_success(client):
    url = reverse('register')
    data = {
        'username': 'testuser',
        'password1': 'supertestpass123',
        'password2': 'supertestpass123',
    }
    response = client.post(url, data)
    # После успешной регистрации должен быть редирект
    assert response.status_code == 302
    assert response.url == reverse('login')
    # Проверим, что пользователь создан
    user_exists = User.objects.filter(username='testuser').exists()
    assert user_exists
    
@pytest.mark.django_db
def test_register_view_post_password_mismatch(client):
    url = reverse('register')
    data = {
        'username': 'testuser2',
        'password1': 'supertestpass123',
        'password2': 'anotherpass456',  # пароли не совпадают
    }
    response = client.post(url, data)
    # Не должно быть редиректа, страница должна отобразиться снова с ошибкой
    assert response.status_code == 200
    # Проверим, что пользователь НЕ создан
    user_exists = User.objects.filter(username='testuser2').exists()
    assert not user_exists
    # Можно проверить, что форма содержит ошибку пароля
    assert "password2" in response.context["form"].errors

@pytest.mark.django_db
def test_can_propose_exchange(client):
    user1 = User.objects.create_user(username='user1', password='pass')
    user2 = User.objects.create_user(username='user2', password='pass')
    ad1 = Ad.objects.create(user=user1, title='Моё объявление')
    ad2 = Ad.objects.create(user=user2, title='Чужое объявление')
    client.login(username='user1', password='pass')
    url = reverse('propose_exchange', args=[ad2.pk])
    response = client.post(url, {'ad_sender': ad1.pk, 'comment': 'Тест'})
    assert response.status_code == 302
    assert ExchangeProposal.objects.filter(ad_sender=ad1, ad_receiver=ad2).exists()


@pytest.mark.django_db
def test_decline_exchange_proposal(client):
    user1 = User.objects.create_user(username='user1', password='pass')
    user2 = User.objects.create_user(username='user2', password='pass')
    ad1 = Ad.objects.create(user=user1, title='Объявление 1')
    ad2 = Ad.objects.create(user=user2, title='Объявление 2')
    proposal = ExchangeProposal.objects.create(ad_sender=ad1, ad_receiver=ad2, status='pending')
    client.login(username='user2', password='pass')
    url = reverse('decline_exchange_proposal', args=[proposal.pk])
    response = client.get(url)
    proposal.refresh_from_db()
    assert response.status_code == 302
    assert proposal.status == 'declined'

@pytest.mark.django_db
def test_decline_exchange_proposal_unauthorized(client):
    user1 = User.objects.create_user(username='user1', password='pass')
    user2 = User.objects.create_user(username='user2', password='pass')
    ad1 = Ad.objects.create(user=user1, title='Объявление 1')
    ad2 = Ad.objects.create(user=user2, title='Объявление 2')
    proposal = ExchangeProposal.objects.create(ad_sender=ad1, ad_receiver=ad2, status='pending')
    url = reverse('decline_exchange_proposal', args=[proposal.pk])
    response = client.get(url)
    # Ожидаем редирект на страницу логина (по умолчанию /accounts/login/?next=...)
    assert response.status_code == 302
    assert '/login' in response.url


@pytest.mark.django_db
def test_accept_exchange_proposal(client):
    user1 = User.objects.create_user(username='user1', password='pass')
    user2 = User.objects.create_user(username='user2', password='pass')
    ad1 = Ad.objects.create(user=user1, title='Объявление 1')
    ad2 = Ad.objects.create(user=user2, title='Объявление 2')
    proposal = ExchangeProposal.objects.create(ad_sender=ad1, ad_receiver=ad2, status='pending')
    client.login(username='user2', password='pass')
    url = reverse('accept_exchange_proposal', args=[proposal.pk])
    response = client.get(url)
    proposal.refresh_from_db()
    assert response.status_code == 302
    assert proposal.status == 'accepted'

@pytest.mark.django_db
def test_ad_delete(client, django_user_model):
    # Создаём пользователя и объявление
    user = django_user_model.objects.create_user(username='test_user', password='pass')
    ad = Ad.objects.create(title='Test Ad', user=user)
    # Логинимся
    client.login(username='test_user', password='pass')
    # Формируем url для удаления
    url = reverse('ad_delete', args=[ad.pk])
    # Отправляем POST-запрос на удаление
    response = client.post(url)
    # Проверяем редирект
    assert response.status_code == 302
    # Проверяем, что объявление удалено
    assert not Ad.objects.filter(pk=ad.pk).exists()




@pytest.mark.django_db
def test_ad_edit_success(client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='pass')
    category = Category.objects.create(name='Одежда')
    ad = Ad.objects.create(
        title='Old Title',
        user=user,
        description='Описание',
        category=category,
        condition='new',
    )
    client.login(username='testuser', password='pass')
    url = reverse('ad_edit', args=[ad.pk])
    data = {
        'title': 'New Title',
        'description': 'Новое описание',
        'category': category.id,
        'condition': 'used',
    }
    response = client.post(url, data)
    ad.refresh_from_db()
    assert ad.title == 'New Title'
    assert ad.description == 'Новое описание'
    assert ad.condition == 'used'
    assert response.status_code == 302

@pytest.mark.django_db
def test_ad_edit_notowner(client, django_user_model):
    owner = django_user_model.objects.create_user(username='owner', password='pass')
    other = django_user_model.objects.create_user(username='other', password='pass')
    ad = Ad.objects.create(title='Test', user=owner)
    client.login(username='other', password='pass')
    url = reverse('ad_edit', args=[ad.pk])
    response = client.post(url, {'title': 'Hacked'})
    ad.refresh_from_db()
    assert ad.title == 'Test'  # не изменился
    assert response.status_code == 302  # редирект на 'my_ads'