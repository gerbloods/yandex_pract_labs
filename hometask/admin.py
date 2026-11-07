from django.contrib import admin
from .models import Subject, Tag, Homework


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")
    ordering = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)



# 5 задание

@admin.action(description="Отметить как выполненные")
def mark_completed(modeladmin, request, queryset):
    count = queryset.update(is_completed=True)
    modeladmin.message_user(
        request,
        f"Отмечено как выполненные: {count}."
    )

@admin.action(description="Отметить как невыполненные")
def mark_incomplete(modeladmin, request, queryset):
    count = queryset.update(is_completed=False)
    modeladmin.message_user(
        request,
        f"Отмечено как невыполненные: {count}."
    )


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "subject",
        "assigned_date",
        "due_date",
        "is_completed",
    )
    list_filter = ("subject", "is_completed", "assigned_date", "due_date")
    search_fields = ("title", "description", "subject__name")
    filter_horizontal = ("tags",)
    date_hierarchy = "due_date"
    list_editable = ("is_completed",)
    ordering = ("due_date",)
    list_per_page = 20

    actions = [mark_completed, mark_incomplete]
