from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Спробуємо знайти користувача за email
            # (Ми використовуємо змінну username, бо Django передає ввід саме так,
            # навіть якщо там пошта)
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        except UserModel.MultipleObjectsReturned:
            # Якщо раптом є кілька людей з однією поштою - не пускаємо нікого
            # (або можна взяти першого: user = UserModel.objects.filter(email=username).first())
            return None

        # Перевіряємо пароль
        if user.check_password(password):
            return user
        return None