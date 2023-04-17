from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from demo.models import ScannerTemperature
from django.utils import timezone
from .models import Temperature
from .serializers import TemperatureSerializer, PostTemperatureSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = TemperatureSerializer
    queryset = Temperature.objects.all()


class TemperatureViewSets(viewsets.ViewSet):
    @staticmethod
    def list(request):
        queryset = Temperature.objects.all()
        serializer = TemperatureSerializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def retrieve(request, pk=None):
        queryset = Temperature.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = TemperatureSerializer(user)
        return Response(serializer.data)


@api_view(['GET'])
def view(request):
    tp = Temperature.objects.all().order_by('-created')[0]
    serializer = TemperatureSerializer(tp, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def createTemperature(request):
    data = request.data
    if float(data['temp']) > 37.5:
        data['status'] = 'HIGH'
    else:
        data['status'] = 'NORMAL'
    temperature = Temperature.objects.create(
        scanner_id=data['scanner_id'],
        temp=data['temp'],
        status=data['status']
    )

    scanner = ScannerTemperature.objects.get(scanner_id=temperature.scanner_id)
    if not scanner.active:
        scanner.active = True
        scanner.save()
    scanner.updated = timezone.now()
    scanner.save()

    serializer = PostTemperatureSerializer(temperature, many=False)
    return Response(serializer.data)


def index(request):
    return render(request, "demo/index.html")


def detail(request):
    return render(request, "demo/detail.html")
