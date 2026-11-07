
# Консольные команды

## Лабораторная работа №7. Django Templates

### 1. Создание Django-проекта

```powershell
python -m django startproject check
```

### 2. Запуск сервера разработки

```powershell
python manage.py runserver
```

### 3. Запуск сервера на определённом порту

```powershell
python manage.py runserver 8000
```

### 4. Остановка сервера

```text
Ctrl + C
```

### 5. Проверка конфигурации проекта

```powershell
python manage.py check
```

---

## Лабораторная работа №8. Тестирование Django

### 1. Переход в каталог проекта

```powershell
cd E:\yandex_pract_labs\8lecture\homework
```

### 2. Активация виртуального окружения

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Установка зависимостей

```powershell
python -m pip install -r requirements.txt
```

### 4. Запуск тестов Django через pytest

```powershell
python -m pytest hometask -v
```

### 5. Запуск тестов с параллельным выполнением

```powershell
python -m pytest hometask -v -n 2
```

### 6. Автоматическое определение количества процессов

```powershell
python -m pytest hometask -v -n auto
```

### 7. Запуск тестов с анализом покрытия кода

```powershell
python -m pytest hometask --cov=hometask --cov-report=term-missing
```

### 8. Создание HTML-отчёта о покрытии

```powershell
python -m pytest hometask --cov=hometask --cov-report=html
```

Отчёт будет находиться в каталоге `htmlcov`.
Для просмотра открыть файл `htmlcov/index.html`.

### 9. Запуск стандартного тестового механизма Django

```powershell
python manage.py test hometask
```

### 10. Проверка установленных библиотек

```powershell
python -m pip list
```

### 11. Установка pytest и дополнительных инструментов

```powershell
python -m pip install pytest pytest-django pytest-xdist pytest-cov
```

---

## Git и GitHub

### 1. Проверка версии Git

```powershell
git --version
```

### 2. Проверка состояния репозитория

```powershell
git status
```

### 3. Добавление изменений

```powershell
git add .
```

### 4. Создание коммита

```powershell
git commit -m "Update project"
```

### 5. Отправка изменений на GitHub

```powershell
git push
```

### 6. Получение изменений из GitHub

```powershell
git pull
```

### 7. Просмотр истории коммитов

```powershell
git log --oneline
```

---

## GitHub Actions

Автоматический запуск тестов выполняется после отправки изменений в GitHub (`git push`).

Workflow находится в файле:

```text
.github/workflows/tests.yml
```

Команда запуска тестов в GitHub Actions:

```bash
pytest hometask -v -n 2
```

Результаты выполнения можно посмотреть во вкладке **Actions** репозитория GitHub.
