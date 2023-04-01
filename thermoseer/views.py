from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import TemperatureForm
from demo.models import Temperature


def home(request):
    first_record = Temperature.objects.first()
    return render(request, "thermoser/home.html", {"first_record": first_record})


def scanned_record(request):
    first_record = Temperature.objects.first()
    return JsonResponse({'data': first_record})


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


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('thermoseer:home')


# Create your views here.
def temperature_list(request):
    object_list = Temperature.objects.all()
    paginator = Paginator(object_list, 3)  # 3 posts in each page
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
def create_temperature(request):
    if request.method == 'GET':
        return render(request, 'thermoser/temperature/createtemperature.html', {'form': TemperatureForm()})
    else:
        try:
            form = TemperatureForm(request.POST)
            temp = form.save(commit=False)
            temp.user = request.user
            temp.save()
            return redirect('thermoseer:temperature_list')
        except ValueError:
            return render(request, 'thermoser/temperature/createtemperature.html',
                          {'form': TemperatureForm(), 'error': 'Bad data passed in. Try again.'})


@login_required
def temperature_detail(request, temp_pk):
    temperature = get_object_or_404(Temperature, pk=temp_pk, user=request.user)
    return render(request, 'thermoser/temperature/detail.html', {'temperature': temperature})
