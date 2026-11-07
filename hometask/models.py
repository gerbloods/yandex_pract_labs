from django.db import models
from django.utils import timezone
# Задание 1. Создание моделей для приложения "Домашние задания" с разными связями между ними.

class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название предмета")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название тега")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Homework(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="homeworks",
        verbose_name="Предмет"
    )
    title = models.CharField(max_length=200, verbose_name="Тема задания")
    description = models.TextField(blank=True, verbose_name="Описание задания")
    assigned_date = models.DateField(verbose_name="Дата выдачи")
    due_date = models.DateField(verbose_name="Срок сдачи")
    is_completed = models.BooleanField(default=False, verbose_name="Выполнено")
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="homeworks",
        verbose_name="Теги"
    )

    def __str__(self):
        return self.title
    
    @property
    def is_overdue(self):
        return (
            not self.is_completed
            and self.due_date < timezone.localdate()
        )

    class Meta:
        verbose_name = "Домашнее задание"
        verbose_name_plural = "Домашние задания"
