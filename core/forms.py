from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ticket, Comment

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(label="Ім'я та прізвище", max_length=100, required=False)
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        # Додаємо username, бо Django вимагає його для створення юзера
        fields = ('username', 'email', 'full_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['full_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'equipment', 'priority', 'description']
        widgets = {
            'priority': forms.Select(attrs={'class': 'form-select-custom'}),
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'is_internal']
        
class RegistrationForm(UserCreationForm):
    # Робимо пошту обов'язковою (за замовчуванням у Django вона необов'язкова)
    email = forms.EmailField(required=True, label="Електронна пошта")

    class Meta:
        model = User
        # Вказуємо тільки ті поля, які має бачити людина
        fields = ['email', 'first_name', 'last_name'] 
        # Поля 'username' тут більше немає!
        
    

