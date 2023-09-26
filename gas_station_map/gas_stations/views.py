from datetime import datetime

from django.shortcuts import render, redirect

# Create your views here.

from .models import GasStation, FuelType, Column, BankCard, Profile, Payment
import folium

from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, BankCardForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return redirect('gas_stations_map')

@login_required
def gas_stations_map(request):

    # Получение списка заправок из базы данных
    gas_stations = GasStation.objects.all()

    lat = request.META.get('HTTP_X_REAL_IP') # получение широты и долготы пользователя
    lng = request.META.get('HTTP_X_REAL_IP')
    if lat and lng:
        m = folium.Map(location=[lat, lng], zoom_start=8, width='100%', height='100%') # инициализация карты и установка местоположения пользователя
        folium.Marker([lat, lng]).add_to(m) # добавление маркера на карту с местоположением пользователя
    else:
        m = folium.Map(location=[54.297570, 48.326542], zoom_start=15)
    # Добавление маркеров на карту
    for gas_station in gas_stations:
        columns = Column.objects.filter(id_GasStation=gas_station.id).order_by('fuel')
        fuel_types = []
        for column in columns:
            fuel_types.append(column)
        popup_html = f'''<div style="font-size: 20px;">{gas_station.name}<br/>{gas_station.address}<br/><br/>Заправиться:</div>'''
        for fuel_type in fuel_types:
            if str(fuel_type.fuel) not in popup_html:
                popup_html += f'<a href="fuel-selection/?gas_station_id={gas_station.id}&fuel_type={fuel_type.fuel_id}" class="btn btn-primary" style="color:white;">{fuel_type.fuel}</a>'
        folium.Marker(
            location=[gas_station.latitude, gas_station.longitude],
            icon=folium.Icon(icon='gas', prefix='fa', color='blue'),
            popup=popup_html
        ).add_to(m)

    # Конвертация карты в HTML и возврат страницы
    m = m._repr_html_()
    context = {'map': m,
               }
    return render(request, 'gas_stations/gas_stations_map.html', context)


def fuel_selection(request):
    gas_station_id = request.GET.get('gas_station_id')
    fuel_id = request.GET.get('fuel_type')
    gas_station = GasStation.objects.get(id=gas_station_id)
    fuel_type = FuelType.objects.get(id=fuel_id)

    columns = Column.objects.filter(id_GasStation=gas_station_id, fuel=fuel_id).order_by('number')
    columns = [column for column in columns]
    context = {
        'fuel_id': fuel_id,
        'fuel_type': fuel_type,
        'gas_station': gas_station,
        'columns': columns
    }
    return render(request, 'gas_stations/fuel_selection.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('gas_stations_map')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('gas_stations_map')
        else:
            messages.info(request, 'Неверное имя пользователя или пароль')
    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def payment(request):
    user_profile = request.user.profile
    cards = BankCard.objects.filter(profile=user_profile)
    gas_station_id = request.GET.get('column_id')
    fuel_id = request.GET.get('fuel_id')
    if request.method == 'POST':
        form = BankCardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.profile = user_profile
            card.save()
            return redirect('payment')
    else:
        form = BankCardForm()

    context = {
        'fuel_id': fuel_id,
        'gas_station': gas_station_id,
        'cards': cards,
        'form': form
    }

    return render(request, 'payment.html', context)


def payment_confirm(request):
    # Получаем данные из формы оплаты
    if request.method == 'POST':
        profile_name = request.user.profile
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        gas_station_id = request.POST.get('station_id')
        fuel_id = request.POST.get('fuel_id')

        fuel = FuelType.objects.get(id=fuel_id)
        gas_station = Column.objects.get(id=gas_station_id)

        # Сохраняем данные в БД
        Payment.objects.create(profile=profile_name, gas_station=gas_station.id_GasStation, fuel_type=fuel, date=date)

        # Отображаем сообщение об успешной оплате
        return render(request, 'payment_success.html')

    return redirect('payment')

def payment_view(request):
    profile = request.user.profile
    payments = Payment.objects.filter(profile=profile)
    context = {
        'payments': payments,
    }
    return render(request, 'payment_view.html', context)
