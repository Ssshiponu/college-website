from django.contrib import admin
from .models import Department, Faculty, Notice, Program, Event, Gallery, Faq

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department_head', 'established')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'code', 'department_head')

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'department', 'email', 'join_date')
    list_filter = ('designation', 'department', 'is_featured')
    search_fields = ('name', 'email', 'bio')

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'publish_date', 'is_important')
    list_filter = ('category', 'is_important', 'publish_date')
    search_fields = ('title', 'content')
    date_hierarchy = 'publish_date'

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'department', 'duration')
    list_filter = ('level', 'department')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'is_featured')
    list_filter = ('is_featured', 'date')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'upload_date')
    list_filter = ('category', 'upload_date')
    search_fields = ('title', 'description')

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'ans', 'page')
