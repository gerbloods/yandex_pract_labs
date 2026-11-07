from django.shortcuts import render
from django.http import HttpResponse
from .models import Homework
from django.shortcuts import render, redirect
from .forms import HomeworkForm
from .forms import (
    HomeworkStepOneForm,
    HomeworkStepTwoForm,
    HomeworkStepThreeForm
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView

class HomeworkPermissionMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        print("МИКСИН РАБОТАЕТ")
        print("Пользователь:", request.user)
        print("Авторизован:", request.user.is_authenticated)

        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        if request.user.has_perm('hometask.view_homework'):
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied

class HomeworkListView(HomeworkPermissionMixin, ListView):
    model = Homework
    template_name = 'taskDetails.html'
    context_object_name = 'homeworks'

    # 7.4 Неоптимизированный вариант с n+1 запросами (Подтянет 14 запросов)
    # def get_queryset(self):
    #     return Homework.objects.all()
    
    # 7.4 Оптимизация n+1 запросов (сократит количество запросов до 4)
    def get_queryset(self):
        return (
            Homework.objects
            .select_related('subject')
            .prefetch_related('tags')
        )

# 4 задание

# def index(request):
#     homeworks = Homework.objects.all()

#     return render(
#         request,
#         'taskDetails.html',
#         {'homeworks': homeworks}
#     )

def index(request):
    homeworks = (
        Homework.objects
        .select_related('subject')
        .prefetch_related('tags')
    )

    return render(
        request,
        'taskDetails.html',
        {'homeworks': homeworks}
    )


# 7.1 Функция отправки формы на сервер и сохранения данных в базу данных

def create_homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = HomeworkForm()

    return render(
        request,
        'homework_form.html',
        {'form': form}
    )

# 7.2 функция для обработки wizard-формы

def homework_wizard(request, step):
    wizard_data = request.session.get('homework_wizard', {})
    
    if step == 1:
        form = HomeworkStepOneForm(request.POST or None)

        if request.method == 'POST' and form.is_valid():
            wizard_data['subject'] = form.cleaned_data['subject'].id

            request.session['homework_wizard'] = wizard_data

            return redirect('homework_wizard', step=2)

    elif step == 2:
        form = HomeworkStepTwoForm(request.POST or None)

        if request.method == 'POST' and form.is_valid():
            wizard_data.update({
                'title': form.cleaned_data['title'],
                'description': form.cleaned_data['description'],
                'assigned_date': form.cleaned_data['assigned_date'].isoformat(),
                'due_date': form.cleaned_data['due_date'].isoformat(),
            })

            request.session['homework_wizard'] = wizard_data

            return redirect('homework_wizard', step=3)

    elif step == 3:
        form = HomeworkStepThreeForm(request.POST or None)

        if request.method == 'POST' and form.is_valid():
            homework = Homework.objects.create(
                subject_id=wizard_data['subject'],
                title=wizard_data['title'],
                description=wizard_data['description'],
                assigned_date=wizard_data['assigned_date'],
                due_date=wizard_data['due_date'],
            )

            homework.tags.set(form.cleaned_data['tags'])

            del request.session['homework_wizard']

            return redirect('index')

    else:
        return redirect('homework_wizard', step=1)

    return render(request, 'homework_wizard.html', {
        'form': form,
        'step': step
    })