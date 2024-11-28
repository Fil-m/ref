# accounts/views.py
from .forms import RegisterForm, AdForm
from .models import Ad
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, AuthenticationForm, UserCreationForm
from .forms import RegisterForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)  # Створюємо об'єкт, але ще не зберігаємо його
            ad.owner = request.user  # Призначаємо власника оголошення поточному користувачу
            ad.save()  # Тепер зберігаємо об'єкт з прив'язкою до користувача
            return redirect('home')  # Перенаправляємо на головну сторінку після успішного збереження
    else:
        form = AdForm()

    return render(request, 'create_ad.html', {'form': form})

@login_required
def profile(request):
    # Логіка для оновлення профілю користувача
    return render(request, 'accounts/profile.html')

@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.owner = request.user
            ad.save()
            return redirect('ads_list')
    else:
        form = AdForm()
    return render(request, 'accounts/ad_form.html', {'form': form})

@login_required
def edit_ad(request, id):
    ad = get_object_or_404(Ad, id=id, owner=request.user)
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ads_list')
    else:
        form = AdForm(instance=ad)
    return render(request, 'accounts/ad_form.html', {'form': form})

@login_required
def delete_ad(request, id):
    ad = get_object_or_404(Ad, id=id, owner=request.user)
    if request.method == 'POST':
        ad.delete()
        return redirect('ads_list')
    return render(request, 'accounts/delete_ad.html', {'ad': ad})



@login_required
def my_ads(request):
    ads = Ad.objects.filter(owner=request.user)
    return render(request, 'accounts/my_ads.html', {'ads': ads})


@login_required
def home(request):
    search_query = request.GET.get('search', '')
    filter_query = request.GET.get('filter', '')
    page_number = request.GET.get('page', 1)

    ads_list = Ad.objects.all()

    # Застосування пошуку, якщо є
    if search_query:
        ads_list = ads_list.filter(title__icontains=search_query)

    # Застосування фільтрів, якщо є
    if filter_query:
        ads_list = ads_list.filter(some_field=filter_query)  # Замініть some_field на відповідне поле

    # Упорядкування перед пагінацією
    ads_list = ads_list.order_by('-created_at')  # Замініть на потрібне поле

    paginator = Paginator(ads_list, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'filter_query': filter_query,
    }
    return render(request, 'accounts/home.html', context)

def register_or_login(request):
    if request.method == 'POST':
        if 'register' in request.POST:  # Якщо користувач надіслав форму реєстрації
            register_form = RegisterForm(request.POST)
            login_form = AuthenticationForm()
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect('home')
        elif 'login' in request.POST:  # Якщо користувач надіслав форму входу
            login_form = AuthenticationForm(request, data=request.POST)
            register_form = RegisterForm()
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
    else:
        register_form = RegisterForm()
        login_form = AuthenticationForm()

    return render(request, 'accounts/register.html', {'register_form': register_form, 'login_form': login_form})


