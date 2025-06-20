# main/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Course, Application, ContactMessage


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Администрирование пользователей"""
    list_display = ('username', 'full_name', 'email', 'phone', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'full_name', 'email', 'phone')
    ordering = ('-date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('full_name', 'phone')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {'fields': ('full_name', 'phone', 'email')}),
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Администрирование курсов"""
    # Исправлено: используем 'title' вместо 'name', так как в модели поле называется 'title'
    list_display = ('title', 'category', 'price', 'duration', 'is_active', 'created_at')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('title', 'description', 'short_description')
    list_editable = ('is_active', 'price')
    ordering = ('-created_at',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'short_description', 'description', 'category')
        }),
        ('Параметры курса', {
            'fields': ('duration', 'price')
        }),
        ('Дополнительно', {
            'fields': ('image', 'is_active')
        }),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Администрирование заявок"""
    list_display = ('user', 'course', 'preferred_start_date', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at', 'course')
    search_fields = ('user__username', 'user__full_name', 'user__email', 'course__title')
    list_editable = ('status',)
    ordering = ('-created_at',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'course', 'preferred_start_date', 'payment_method')
        }),
        ('Статус и примечания', {
            'fields': ('status', 'notes')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        """Оптимизируем запросы"""
        return super().get_queryset(request).select_related('user', 'course')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Администрирование контактных сообщений"""
    list_display = ('name', 'email', 'phone', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('is_read',)
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')


# Настройка заголовков админки
admin.site.site_header = "Администрирование учебных курсов"
admin.site.site_title = "Учебные курсы"
admin.site.index_title = "Панель управления"