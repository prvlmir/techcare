from django.db import models
from django.contrib.auth.models import User

# --- МОДЕЛЬ ОБЛАДНАННЯ (Assets) ---
class Asset(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва обладнання")
    image = models.ImageField(upload_to='assets/', null=True, blank=True, verbose_name="Фото")
    inventory_number = models.CharField(max_length=50, unique=True, verbose_name="Інвентарний номер")
    specs = models.TextField(verbose_name="Характеристики", blank=True)
    location = models.CharField(max_length=100, verbose_name="Розташування")

    def __str__(self):
        return f"{self.name} ({self.inventory_number})"

    class Meta:
        verbose_name = "Актив"
        verbose_name_plural = "Активи"

# --- МОДЕЛЬ ЗАЯВКИ (Tickets) ---   

class Ticket(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Низька (Можу почекати)'),
        ('Medium', 'Середня'),
        ('High', 'Висока (Терміново)'),
    ]
    
    STATUS_CHOICES = [
        ('Open', 'Нова'),
        ('In Progress', 'В роботі'),
        ('Closed', 'Закрито'),
    ]

    title = models.CharField(max_length=200, verbose_name="Тема")
    description = models.TextField(verbose_name="Опис")
    
    # НОВІ ПОЛЯ
    equipment = models.CharField(max_length=100, blank=True, null=True, verbose_name="Обладнання") 
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Low', verbose_name="Терміновість")
    
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_tickets',
        verbose_name="Виконавець"
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст коментаря")
    is_internal = models.BooleanField(default=False, verbose_name="Тільки для фахівців")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.ticket}"
    
    
class InventoryItem(models.Model):
    STATUS_CHOICES = [
        ('Вжитку', 'Вжитку'),
        ('На складі', 'На складі'),
        ('Списано', 'Списано'),
        ('В ремонті', 'В ремонті'),
    ]

    type = models.CharField(max_length=100, verbose_name="Тип (напр. Ноутбук)")
    model = models.CharField(max_length=100, verbose_name="Модель")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Вжитку', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} {self.model} (#{self.id})"

    class Meta:
        verbose_name = "Обладнання"
        verbose_name_plural = "Інвентаризація"