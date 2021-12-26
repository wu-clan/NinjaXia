from django.contrib import admin

# Register your models here.
from backend.models.project import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    项目管理
    """
    list_display = (
        'name',
        'description',
        'created_time',
        'modified_time'
    )
