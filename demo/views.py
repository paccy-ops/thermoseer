from django.shortcuts import render
# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import Temperature
from .serializers import TemperatureSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = TemperatureSerializer
    queryset = Temperature.objects.all()


class TemperatureViewSets(viewsets.ViewSet):
    """s
    A simple ViewSet for listing or retrieving users.
    """

    def list(self, request):
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
    user = request.user
    data = request.data
    product = Temperature.objects.create(
        user=user,
        scanner_id=data['scanner_id'],
        temp=data['temp'],
        dept=data['dept'],
        name=data['name'],

    )

    serializer = TemperatureSerializer(product, many=False)
    return Response(serializer.data)


# class VirkInfoViewList(ListCreateAPIView):
#     """ List all VatAccountInfo, or create a new VatAccountInfo. """
#     serializer_class = TemperatureSerializer
#     # permission_classes = (IsAuthenticated,)
#     queryset = Temperature.objects.all()
#
#     def perform_create(self, serializer, **kwargs):
#         return serializer.save()
#
#     def get_queryset(self):
#         data = self.queryset.order_by('-created')[0]
#         return data


# def data_la(APIView):
#
#     return Response(serializer.data)


def index(request):
    return render(request, "demo/index.html")


def detail(request):
    return render(request, "demo/detail.html")
