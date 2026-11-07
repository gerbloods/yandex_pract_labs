from django import forms
from .models import Homework, Subject, Tag

# 7.1 Создать комплексную форму с несколькими связанными моделями

class HomeworkForm(forms.ModelForm):

    class Meta:
        model = Homework

        fields = [
            'subject',
            'title',
            'description',
            'assigned_date',
            'due_date',
            'tags',
        ]

        labels = {
            'subject': 'Предмет',
            'title': 'Название задания',
            'description': 'Описание',
            'assigned_date': 'Дата выдачи',
            'due_date': 'Срок сдачи',
            'tags': 'Теги',
        }

        widgets = {
            'assigned_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'due_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'description': forms.Textarea(
                attrs={'rows': 4}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        assigned_date = cleaned_data.get('assigned_date')
        due_date = cleaned_data.get('due_date')

        if assigned_date and due_date:
            if due_date < assigned_date:
                raise forms.ValidationError(
                    'Срок сдачи не может быть раньше даты выдачи.'
                )

        return cleaned_data



# 7.2 Создание wizard-формы

class HomeworkStepOneForm(forms.Form):
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        label='Предмет'
    )

class HomeworkStepTwoForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        label='Название задания'
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
        label='Описание'
    )

    assigned_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата выдачи'
    )

    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Срок сдачи'
    )

class HomeworkStepThreeForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        label='Теги'
    )