from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Announcement(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    TYPE = (
        ('tanks', 'Танки'),
        ('heals', 'Хилы'),
        ('damage_dealers', 'Дамагеры'),
        ('merchants', 'Торговецы'),
        ('guildmasters', 'Гилдмастеры'),
        ('questgivers', 'Квестгиверы'),
        ('smiths', 'Кузнецы'),
        ('tanners', 'Кожевникы'),
        ('potions_masters', 'Зельевары'),
        ('spell_masters', 'Мастера заклинаний'),
    )
    categoryType = models.CharField(max_length=15, choices=TYPE, default='tanks')
    time_add = models.DateTimeField(auto_now_add=True)
    head = models.CharField(max_length=256)
    body = models.TextField()
    image = models.ImageField(upload_to='images', blank=True, null=True)
    file = models.FileField(upload_to='files', blank=True, null=True)

    def __str__(self):
        return f'{self.head}'

    def get_absolute_url(self):
        return reverse('announcement_detail', args=[str(self.id)])


class Response(models.Model):
    response_post = models.ForeignKey(Announcement, related_name='response', on_delete=models.CASCADE)
    response_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_add = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text}'

    def get_absolute_url(self):
        return reverse('response_detail', args=[str(self.id)])
