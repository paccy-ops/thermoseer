import requests
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from demo.models import Temperature, ScannerTemperature
from thermoseer.forms import TemperatureForm, ScannerTemperatureForm

#
params = {
    'access_key': 'e4d95824172f03265fd3d151a9fa9629',
    'query': 'Baguio City'
}
#
api_result = requests.get('http://api.weatherstack.com/current', params)


def home(request):
    first_record = Temperature.objects.first()
    api_response = api_result.json()
    humidity = api_response['current']['humidity']
    temperature = api_response['current']['temperature']
    weather_icons = api_response['current']['weather_icons']
    wind_degree = api_response['current']['wind_degree']
    name = api_response['location']['name']
    country = api_response['location']['country']
    timezone_id = api_response['location']['timezone_id']
    weather_descriptions = api_response['current']['weather_descriptions']

    return render(request, "thermoser/home.html", {
        "first_record": first_record,
        "humidity": humidity,
        "temperature": temperature,
        "weather_icons": weather_icons[0],
        "wind_degree": wind_degree,
        "name": name,
        "country": country,
        "timezone_id": timezone_id,
        "weather_descriptions": weather_descriptions[0]
    })


def temperature_list(request):
    search_str = request.GET.get("searchText")
    object_list = Temperature.objects.all()
    if search_str is not None:
        object_list = Temperature.objects.filter(
            Q(temp__icontains=search_str) |
            Q(scanner__name__icontains=search_str) |
            Q(scanner__scanner_id__icontains=search_str) |
            Q(status__icontains=search_str))

    paginator = Paginator(object_list, 4)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        temperatures = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        temperatures = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        temperatures = paginator.page(paginator.num_pages)
    return render(request,
                  'thermoser/temperature/list.html',
                  {'page': page,
                   'temperatures': temperatures})


@login_required
def temperature_users_details(request):
    temperature = Temperature.objects.last()
    scanner = ScannerTemperature.objects.first()
    user_scanners = ScannerTemperature.objects.all()[:6]
    latest_test = scanner.scanners.first()
    temperatures = Temperature.objects.filter(scanner_id=scanner.scanner_id)[:3]
    return render(request, 'thermoser/temperature/detail.html',
                  {'temperature': temperature, 'temperatures': temperatures, 'scanner': scanner,
                   'user_scanners': user_scanners,
                   'latest_test': latest_test})


@login_required
def user_scanner_detail(request, temp_pk):
    scanner = get_object_or_404(ScannerTemperature, scanner_id=temp_pk, user=request.user)
    user_scanners = ScannerTemperature.objects.all()[:5]
    latest_test = scanner.scanners.first()
    temperatures = scanner.scanners.all()
    paginator = Paginator(temperatures, 3)
    page = request.GET.get('page')
    try:
        temperatures = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        temperatures = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        temperatures = paginator.page(paginator.num_pages)
    return render(request, 'thermoser/temperature/detail.html',
                  {'scanner': scanner, 'latest_test': latest_test, 'temperatures': temperatures,
                   'user_scanners': user_scanners})


@login_required
def temperature_detail(request, temp_pk):
    temperature = get_object_or_404(ScannerTemperature, pk=temp_pk, user=request.user)
    scanner = get_object_or_404(ScannerTemperature, pk=temp_pk)
    scanner_ids = Temperature.objects.filter(scanner_id=temperature.scanner_id)
    temperatures = Temperature.objects.all()
    paginator = Paginator(scanner_ids, 3)
    page = request.GET.get('page')
    try:
        scanner_ids = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        scanner_ids = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        scanner_ids = paginator.page(paginator.num_pages)

    return render(request, 'thermoser/temperature/detail.html',
                  {'temperature': temperature, 'scanner': scanner, 'temperatures': temperatures,
                   'scanners': scanner_ids})


@login_required
def users_list(request):
    user = Temperature.objects.first()
    users = ScannerTemperature.objects.all()
    return render(request, 'thermoser/temperature/detail.html',
                  {'user': user, 'users': users})


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'thermoser/user/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('thermoseer:home')
            except IntegrityError:
                return render(request, 'thermoser/user/signupuser.html', {'form': UserCreationForm(),
                                                                          'error': 'That username has already been '
                                                                                   'taken.'
                                                                                   'Please choose a new username'})
        else:
            return render(request, 'thermoser/user/signupuser.html',
                          {'form': UserCreationForm(), 'error': 'Passwords did not match'})


#
#
def loginuser(request):
    if request.method == 'GET':
        return render(request, 'thermoser/user/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'thermoser//user/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('thermoseer:temperature_list')


#
#
@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('thermoseer:home')


#
#
#
@login_required
def create_temperature(request):
    if request.method == 'GET':
        return render(request, 'thermoser/temperature/temperature-dashboard.html', {'form': TemperatureForm()})
    else:
        try:
            form = TemperatureForm(request.POST)
            temp = form.save(commit=False)

            temp.user = request.user
            scanner = ScannerTemperature.objects.get(scanner_id=temp.scanner_id)

            if float(temp.temp) >= float(37.5):
                temp.status = "HIGH"
            else:
                temp.status = 'NORMAL'

            if not scanner.active:
                scanner.active = True
                scanner.save()

            temp.save()
            return redirect('thermoseer:temperature_list')
        except ValueError:
            return render(request, 'thermoser/temperature/temperature-dashboard.html',
                          {'form': TemperatureForm(), 'error': 'Bad data passed in. Try again.'})


@login_required
def addId(request):
    if request.method == 'GET':
        return render(request, 'thermoser/temperature/add-id.html', {'form': ScannerTemperatureForm()})
    else:
        try:
            form = ScannerTemperatureForm(request.POST)
            temp = form.save(commit=False)
            temp.user = request.user
            temp.save()
            return redirect('thermoseer:temperature_users_details')
        except ValueError:
            return render(request, 'thermoser/temperature/add-id.html',
                          {'form': ScannerTemperatureForm(), 'error': 'Bad data passed in. Try again.'})
