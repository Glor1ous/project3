# Задание демонстрационного экзамена
## Шпаргалка по Django

### Базовые команды

* **Создание проекта:**
```bash
django-admin startproject myproject
cd myproject
python manage.py startapp myapp
```

* **Миграции:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### Модели

* **Создание модели:**
```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### Формы

* **Базовая форма:**
```python
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
```

### Views

* **Function-based view:**
```python
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
```

* **Class-based view:**
```python
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'
```

### URL

* **urls.py:**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]
```

### Шаблоны

* **Базовый шаблон:**
```html
{% extends 'base.html' %}

{% block content %}
    <h1>{{ title }}</h1>
    {{ content }}
{% endblock %}
```

### Админ-панель

* **Регистрация модели:**
```python
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
```

### Настройки

* **Основные настройки:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
]
```

### Команды для работы

* **Запуск сервера:**
```bash
python manage.py runserver
```

* **Создание суперпользователя:**
```bash
python manage.py createsuperuser
```

* **Работа с shell:**
```bash
python manage.py shell
```

### Полезные команды

* **Просмотр SQL:**
```bash
python manage.py sqlmigrate appname migration_name
```

* **Проверка миграции:**
```bash
python manage.py showmigrations
```

* **Сброс базы данных:**
```bash
python manage.py flush
```#   p r o j e c t  
 #   p r o j e c t 2  
 