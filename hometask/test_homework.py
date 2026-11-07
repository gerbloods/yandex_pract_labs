from django.test import TestCase
from .models import Homework, Subject
from .forms import HomeworkForm
from datetime import timedelta
from django.utils import timezone

class HomeworkFormTest(TestCase):

    def setUp(self):
        self.subject = Subject.objects.create(
            name='Математика'
        )

        self.valid_data = {
            'subject': self.subject.id,
            'title': 'Решить задачи',
            'description': 'Задания из учебника',
            'assigned_date': '2026-11-06',
            'due_date': '2026-11-10',
        }

    # Проверка корректных данных
    def test_valid_form(self):
        form = HomeworkForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    # Дата сдачи раньше даты выдачи
    def test_due_date_before_assigned_date(self):
        data = self.valid_data.copy()
        data['due_date'] = '2026-11-05'

        form = HomeworkForm(data=data)

        self.assertFalse(form.is_valid())

    # Даты совпадают
    def test_equal_dates(self):
        data = self.valid_data.copy()
        data['due_date'] = data['assigned_date']

        form = HomeworkForm(data=data)

        self.assertTrue(form.is_valid())

    # Не указано название
    def test_empty_title(self):
        data = self.valid_data.copy()
        data['title'] = ''

        form = HomeworkForm(data=data)

        self.assertFalse(form.is_valid())

    # Не указана дата выдачи
    def test_empty_assigned_date(self):
        data = self.valid_data.copy()
        data['assigned_date'] = ''

        form = HomeworkForm(data=data)

        self.assertFalse(form.is_valid())

    # Необязательные поля пустые
    def test_optional_fields_empty(self):
        data = self.valid_data.copy()
        data['description'] = ''

        form = HomeworkForm(data=data)

        self.assertTrue(form.is_valid())


# 8.1 TDD тестирование модели Homework
class HomeworkOverdueTest(TestCase):

    def setUp(self):
        self.subject = Subject.objects.create(
            name='Математика'
        )

    def create_homework(self, due_date, is_completed=False):
        return Homework.objects.create(
            subject=self.subject,
            title='Решить задачи',
            assigned_date=timezone.localdate() - timedelta(days=7),
            due_date=due_date,
            is_completed=is_completed
        )

    # Срок прошёл, задание не выполнено
    def test_homework_is_overdue(self):
        homework = self.create_homework(
            timezone.localdate() - timedelta(days=1)
        )

        self.assertTrue(homework.is_overdue)

    # Срок ещё не наступил
    def test_homework_is_not_overdue(self):
        homework = self.create_homework(
            timezone.localdate() + timedelta(days=1)
        )

        self.assertFalse(homework.is_overdue)

    # Выполненное задание не считается просроченным
    def test_completed_homework_is_not_overdue(self):
        homework = self.create_homework(
            timezone.localdate() - timedelta(days=1),
            is_completed=True
        )

        self.assertFalse(homework.is_overdue)

    # Срок сдачи сегодня — задание ещё не просрочено
    def test_homework_due_today_is_not_overdue(self):
        homework = self.create_homework(
            timezone.localdate()
        )

        self.assertFalse(homework.is_overdue)