import pytest
from .models import Subject
from .forms import HomeworkForm

# Тестирование формы HomeworkForm с помощью библиотеки pytest
# Корректные данные принимаются.
# Обязательные поля не могут быть пустыми.
# Срок сдачи не может быть раньше даты выдачи.
# Некорректный формат даты отклоняется.
# Слишком длинное название отклоняется.
# Несуществующий предмет отклоняется.
# Необязательное описание можно оставить пустым.
# Теги проверяются на принадлежность существующим объектам.


# Фикстура: создаёт предмет в тестовой базе данных
@pytest.fixture
def subject(db):
    return Subject.objects.create(
        name='Математика'
    )


# Фикстура: подготавливает корректные данные для формы
@pytest.fixture
def valid_data(subject):
    return {
        'subject': subject.id,
        'title': 'Решить задачи',
        'description': 'Задания из учебника',
        'assigned_date': '2026-11-06',
        'due_date': '2026-11-10',
    }


# 1. Проверка корректных данных
def test_valid_homework_form(valid_data):
    form = HomeworkForm(data=valid_data)

    assert form.is_valid()


# 2. Проверка обязательных полей
@pytest.mark.parametrize(
    'field,value',
    [
        ('title', ''),
        ('assigned_date', ''),
        ('subject', ''),
    ]
)
def test_required_fields(field, value, valid_data):
    data = valid_data.copy()
    data[field] = value

    form = HomeworkForm(data=data)

    assert not form.is_valid()
    assert field in form.errors


# 3. Проверка срока сдачи
def test_due_date_before_assigned_date(valid_data):
    data = valid_data.copy()
    data['due_date'] = '2026-11-05'

    form = HomeworkForm(data=data)

    assert not form.is_valid()
    assert '__all__' in form.errors


# 4. Проверка некорректного формата даты
def test_invalid_date_format(valid_data):
    data = valid_data.copy()
    data['assigned_date'] = 'не дата'

    form = HomeworkForm(data=data)

    assert not form.is_valid()
    assert 'assigned_date' in form.errors


# 5. Проверка максимальной длины названия
def test_title_too_long(valid_data):
    data = valid_data.copy()
    data['title'] = 'А' * 201

    form = HomeworkForm(data=data)

    assert not form.is_valid()
    assert 'title' in form.errors


# 6. Проверка несуществующего предмета
def test_invalid_subject(valid_data):
    data = valid_data.copy()
    data['subject'] = 99999

    form = HomeworkForm(data=data)

    assert not form.is_valid()
    assert 'subject' in form.errors


# 7. Проверка необязательного описания
def test_empty_description(valid_data):
    data = valid_data.copy()
    data['description'] = ''

    form = HomeworkForm(data=data)

    assert form.is_valid()