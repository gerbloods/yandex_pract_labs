from django.urls import path
from . import views
from .views import HomeworkListView

urlpatterns = [
    # path('', views.index, name='index'),
    path('', HomeworkListView.as_view(), name='index'),
    path('create/', views.create_homework, name='create_homework'),
    path('wizard/<int:step>/', views.homework_wizard, name='homework_wizard'),
]