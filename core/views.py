from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Ticket, InventoryItem
from .forms import CustomUserCreationForm, TicketForm, CommentForm, RegistrationForm

# ==========================================
# АВТОРИЗАЦІЯ ТА РЕЄСТРАЦІЯ
# ==========================================

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # 1. Створюємо об'єкт користувача, але ПОКИ НЕ зберігаємо в БД (commit=False)
            user = form.save(commit=False)
            
            # 2. Записуємо Email у поле Username (хитрість)
            user.username = user.email 
            
            # 3. Тепер зберігаємо остаточно
            user.save()
            
            # 4. Вхід (з твоїм фіксом бекенда)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            return redirect('dashboard_user')
    else:
        form = RegistrationForm()
    
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect_user_based_on_role(request.user)

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect_user_based_on_role(user)
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def redirect_user_based_on_role(user):
    if user.is_staff:
        return redirect('dashboard_staff')
    else:
        return redirect('dashboard_user')


# ==========================================
# DASHBOARDS (КАБІНЕТИ)
# ==========================================

@login_required
def dashboard_user(request):
    # Отримуємо всі заявки поточного користувача
    tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')
    
    # Рахуємо статистику
    total_count = tickets.count()
    # Припускаємо, що активні це 'Open', а закриті 'Closed' (перевір свої value у models.py)
    active_count = tickets.filter(status='Open').count() 
    closed_count = tickets.filter(status='Closed').count()
    
    context = {
        'tickets': tickets,
        'total_count': total_count,
        'active_count': active_count,
        'closed_count': closed_count
    }
    return render(request, 'core/dashboard_user.html', context)


@login_required
def dashboard_staff(request):
    if not request.user.is_staff:
        return redirect('dashboard_user')
    
    # 1. Отримуємо параметр 'tab' з URL (за замовчуванням 'all')
    current_tab = request.GET.get('tab', 'all')
    
    # Базовий запит (всі заявки)
    tickets = Ticket.objects.all().order_by('-created_at')

    # 2. Фільтруємо залежно від вкладки
    if current_tab == 'active':
        # Показуємо тільки "Нова" та "В роботі"
        tickets = tickets.exclude(status='Closed')
    elif current_tab == 'my':
        tickets = tickets.filter(assigned_to=request.user)
    elif current_tab == 'inventory':
        inventory_items = InventoryItem.objects.all().order_by('id')
    
    # 3. Рахуємо статистику (вона однакова для всіх вкладок)
    total_count = Ticket.objects.count()
    new_count = Ticket.objects.filter(status='Open').count()
    critical_count = Ticket.objects.filter(priority='High').count()
    inventory_items = InventoryItem.objects.all()
    
    # Рахуємо кількість активних для бейджика в меню
    active_count_total = Ticket.objects.exclude(status='Closed').count()

    context = {
        'tickets': tickets,         # Цей список змінюється динамічно!
        'current_tab': current_tab, # Передаємо поточну вкладку, щоб підсвітити кнопку
        'total_count': total_count,
        'new_count': new_count,
        'critical_count': critical_count,
        'active_count_total': active_count_total,
        'inventory': inventory_items,
    }
    
    return render(request, 'core/dashboard_staff.html', context)
# ==========================================
# РОБОТА З ТІКЕТАМИ
# ==========================================

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            # ВИПРАВЛЕНО: customer -> created_by
            ticket.created_by = request.user 
            ticket.save()
            return redirect('dashboard_user')
    else:
        form = TicketForm()
    
    return render(request, 'core/create_ticket.html', {'form': form})


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    
    # Перевірка доступу
    if request.user != ticket.created_by and not request.user.is_staff:
        return redirect('dashboard_user')

    # Обробка форми (Коментар або Зміна статусу)
    if request.method == 'POST':
        # 1. Якщо натиснули "Забронювати заявку"
        if 'assign_me' in request.POST and request.user.is_staff:
            ticket.assigned_to = request.user
            ticket.status = 'In Progress' # Автоматично переводимо в "В роботі"
            ticket.save()
            return redirect('ticket_detail', pk=pk)
        
        # 2. Якщо змінили статус/пріоритет (сайдбар)
        if 'update_status' in request.POST and request.user.is_staff:
            ticket.status = request.POST.get('status')
            ticket.priority = request.POST.get('priority')
            ticket.save()
            return redirect('ticket_detail', pk=pk)

        # 3. Якщо додали коментар
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            return redirect('ticket_detail', pk=pk)
    
    else:
        comment_form = CommentForm()

    comments = ticket.comments.all().order_by('created_at')

    return render(request, 'core/ticket_detail.html', {
        'ticket': ticket,
        'comments': comments,
        'comment_form': comment_form
    })