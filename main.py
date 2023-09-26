def gas_stations_map(request):
    # Создание карты
    #m = folium.Map(location=[54.297570, 48.326542], zoom_start=12)

    # populate_gas_stations(request)

    # Получение списка заправок из базы данных
    gas_stations = GasStation.objects.all()

    lat = request.META.get('HTTP_X_REAL_IP') # получение широты и долготы пользователя
    lng = request.META.get('HTTP_X_REAL_IP')
    if lat and lng:
        m = folium.Map(location=[lat, lng], zoom_start=13) # инициализация карты и установка местоположения пользователя
        folium.Marker([lat, lng]).add_to(map) # добавление маркера на карту с местоположением пользователя
    else:
        m = folium.Map(location=[54.297570, 48.326542], zoom_start=12)
    # Добавление маркеров на карту
    for gas_station in gas_stations:
        folium.Marker(
            location=[gas_station.latitude, gas_station.longitude],
            icon=folium.Icon(icon='gas', prefix='fa', color='blue'),
            popup='''
                    <form>
                        <label for="fuel_type">Выберите тип топлива:</label>
                        <select id="fuel_type" name="fuel_type">
                            <option value="a92">A92</option>
                            <option value="a95">A95</option>
                            <option value="diesel">Дизельное топливо</option>
                        </select>
                        <br><br>
                        <input type="submit" value="Отправить">
                    </form>
                    '''
        ).add_to(m)

    form = FuelPurchaseForm(request.POST or None)
    if form.is_valid():
        fuel_type = form.cleaned_data['fuel_type']
        amount = form.cleaned_data['amount']
        payment_method = form.cleaned_data['payment_method']
        # сохраните данные в базу данных или отправьте их на обработку
        return render(request, 'purchase_confirmation.html', {
            'fuel_type': fuel_type,
            'amount': amount,
            'payment_method': payment_method,
        })


    # Конвертация карты в HTML и возврат страницы
    m = m._repr_html_()
    context = {'map': m,
               'form': form,
               }
    return render(request, 'gas_stations/gas_stations_map.html', context)