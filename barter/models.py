from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Категория")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Ad(models.Model):
    CONDITION_CHOICES = (
        ('new', 'Новый'),
        ('used', 'Б/У'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Категория")
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, verbose_name="Состояние")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    image = models.ImageField(upload_to='ads/', blank=True, null=True)  

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class AdImage(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='ads_images/')

    def __str__(self):
        return f"Image for {self.ad.title}"

class ExchangeProposal(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('declined', 'Отклонена'),
    )
    ad_sender = models.ForeignKey(
        Ad,
        related_name="sent_proposals",
        on_delete=models.CASCADE,
        verbose_name="Объявление отправителя"
    )
    ad_receiver = models.ForeignKey(
        Ad,
        related_name="received_proposals",
        on_delete=models.CASCADE,
        verbose_name="Объявление получателя"
    )
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата предложения")

    class Meta:
        verbose_name = "Заявка на обмен"
        verbose_name_plural = "Заявки на обмен"

    def __str__(self):
        return f"Обмен: {self.ad_sender.title} -> {self.ad_receiver.title} [{self.status}]"