# main/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Course, Application, User, ContactMessage
from .forms import CustomUserCreationForm, ApplicationForm, ContactForm, UserProfileForm


def home(request):
    """Главная страница"""
    # Показываем последние 6 активных курсов
    featured_courses = Course.objects.filter(is_active=True)[:6]
    # Статистика
    total_courses = Course.objects.filter(is_active=True).count()
    total_applications = Application.objects.count()

    context = {
        'featured_courses': featured_courses,
        'total_courses': total_courses,
        'total_applications': total_applications,
    }
    return render(request, 'index.html', context)


def about(request):
    """Страница о нас"""
    return render(request, 'about.html')


def courses(request):
    """Страница со всеми курсами"""
    courses_list = Course.objects.filter(is_active=True)

    # Пагинация
    paginator = Paginator(courses_list, 9)  # 9 курсов на странице
    page_number = request.GET.get('page')
    courses_page = paginator.get_page(page_number)

    return render(request, 'courses.html', {'courses': courses_page})


def course_detail(request, course_id):
    """Детальная страница курса"""
    course = get_object_or_404(Course, id=course_id, is_active=True)

    # Проверяем, есть ли уже заявка от этого пользователя на этот курс
    user_application = None
    if request.user.is_authenticated:
        user_application = Application.objects.filter(
            user=request.user,
            course=course
        ).first()

    context = {
        'course': course,
        'user_application': user_application,
    }
    return render(request, 'course_detail.html', context)


@login_required
def apply_for_course(request, course_id):
    """Подача заявки на курс"""
    course = get_object_or_404(Course, id=course_id, is_active=True)

    # Проверяем, нет ли уже заявки от этого пользователя
    existing_application = Application.objects.filter(
        user=request.user,
        course=course
    ).first()

    if existing_application:
        messages.warning(request, 'Вы уже подали заявку на этот курс!')
        return redirect('course_detail', course_id=course.id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.')
            return redirect('profile')
    else:
        form = ApplicationForm(initial={'course': course})

    context = {
        'form': form,
        'course': course,
    }
    return render(request, 'apply_for_course.html', context)


def contact(request):
    """Страница контактов"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно! Добро пожаловать!')
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    """Профиль пользователя"""
    # Получаем заявки пользователя
    user_applications = Application.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'user_applications': user_applications,
    }
    return render(request, 'registration/profile.html', context)


@login_required
def edit_profile(request):
    """Редактирование профиля"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'registration/edit_profile.html', {'form': form})


@login_required
def application_detail(request, application_id):
    """Детали заявки"""
    application = get_object_or_404(Application, id=application_id, user=request.user)
    return render(request, 'application_detail.html', {'application': application})


@login_required
def cancel_application(request, application_id):
    """Отмена заявки"""
    application = get_object_or_404(Application, id=application_id, user=request.user)

    if application.status == 'new':
        application.status = 'cancelled'
        application.save()
        messages.success(request, 'Заявка успешно отменена.')
    else:
        messages.error(request, 'Нельзя отменить заявку с текущим статусом.')

    return redirect('profile')