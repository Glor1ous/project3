from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Application, ContactMessage


class CustomUserCreationForm(UserCreationForm):
    """Кастомная форма регистрации пользователя"""
    full_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше ФИО'
        }),
        label='ФИО'
    )

    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 (xxx) xxx-xx-xx'
        }),
        label='Телефон'
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com'
        }),
        label='Email'
    )

    class Meta:
        model = User
        fields = ('username', 'full_name', 'phone', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Логин'
            })
        }
        labels = {
            'username': 'Логин',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class ApplicationForm(forms.ModelForm):
    """Форма для подачи заявки на обучение"""

    class Meta:
        model = Application
        fields = ['course', 'preferred_start_date', 'payment_method', 'notes']
        widgets = {
            'course': forms.Select(attrs={
                'class': 'form-select'
            }),
            'preferred_start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-select'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Дополнительная информация (необязательно)'
            })
        }
        labels = {
            'course': 'Выберите курс',
            'preferred_start_date': 'Желаемая дата начала',
            'payment_method': 'Способ оплаты',
            'notes': 'Примечания'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Показываем только активные курсы
        self.fields['course'].queryset = self.fields['course'].queryset.filter(is_active=True)


class ContactForm(forms.ModelForm):
    """Форма обратной связи"""

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваше имя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (xxx) xxx-xx-xx'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Введите ваше сообщение...'
            })
        }
        labels = {
            'name': 'Имя',
            'email': 'Email',
            'phone': 'Телефон',
            'message': 'Сообщение'
        }


class UserProfileForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя"""

    class Meta:
        model = User
        fields = ['full_name', 'phone', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'full_name': 'ФИО',
            'phone': 'Телефон',
            'email': 'Email'
        }