from pprint import pprint
import requests
from geopy.distance import lonlat, distance

from django import forms
from django.db.models import F, Sum
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views

from foodcartapp.models import Product, Restaurant, Order, OrderElements, RestaurantMenuItem
from geo_places.models import Address


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


def fetch_coordinations(address):
    print(' ОБРАЩЕНИЕ К ЯНДЕКС АПИ ')
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": 'c2fb9276-ddef-49b6-84ee-79c40be0a81a',
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_distance_to_rest(rest_address, client_address):
    all_address = Address.objects.all()

    client_coordinations = [(addr.lat, addr.lon) for addr in all_address if addr.name == client_address]
    if not client_coordinations:
        client_coordinations = fetch_coordinations(client_address)
        Address.objects.create(
            name=client_address,
            lon=client_coordinations[0],
            lat=client_coordinations[1],
        )
    else:
        client_coordinations = client_coordinations[0]

    rest_coordinations = [(addr.lat, addr.lon) for addr in all_address if addr.name == rest_address]
    if not rest_coordinations:
        rest_coordinations = fetch_coordinations(rest_address)
        Address.objects.create(
            name=rest_address,
            lon=rest_coordinations[0],
            lat=rest_coordinations[1],
        )
    else:
        rest_coordinations = rest_coordinations[0]

    """Подсчитываем расстояние"""
    distance_to_rest = round(distance(lonlat(*client_coordinations), lonlat(*rest_coordinations)).km, 2)
    return distance_to_rest


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    order_items = Order.objects.prefetch_related('order_elements').annotate(
        coast=Sum(F('order_elements__quantity') * F('order_elements__product__price')))

    all_restaurants_menu = RestaurantMenuItem.objects.all()
    all_orders = OrderElements.objects.all()

    products_by_order = {}
    for order in all_orders:
        if order.order.id in products_by_order.keys():
            products_by_order[order.order.id].append(order.product)
        else:
            products_by_order[order.order.id] = [order.product]

    rest_by_products = {}
    for restaurant in all_restaurants_menu:
        if restaurant.restaurant in rest_by_products.keys():
            rest_by_products[restaurant.restaurant].append(restaurant.product)
        else:
            rest_by_products[restaurant.restaurant] = [restaurant.product]

    rest_can_cook_by_order = {}
    for order_id, i in products_by_order.items():
        order_address = Order.objects.filter(id=order_id)[0].address
        for rest, j in rest_by_products.items():
            rest_address = rest.address
            distance_to_rest = get_distance_to_rest(rest_address, order_address)

            if set(i).issubset(j):
                if order_id in rest_can_cook_by_order.keys():
                    rest_can_cook_by_order[order_id].append(f'{rest.name} - {distance_to_rest} км')
                else:
                    rest_can_cook_by_order[order_id] = [f'{rest.name} - {distance_to_rest} км']

    return render(request, template_name='order_items.html', context={
        'order_items': order_items,
        'rest_can_cook_by_order': rest_can_cook_by_order,
    })
