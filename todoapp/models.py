from django.contrib.auth.models import User
from django.db import models


class Todo(models.Model):
    description = models.TextField(blank=False, verbose_name='Описание задачи')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_complete = models.BooleanField(default=False, verbose_name='Выполнение')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='todos')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
