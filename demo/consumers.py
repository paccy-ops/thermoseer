from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin, RetrieveModelMixin
from djangochannelsrestframework.observer import model_observer

from .models import Temperature
from .serializers import TemperatureSerializer


class PostConsumer(ListModelMixin, GenericAsyncAPIConsumer):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer
    permissions = (permissions.AllowAny,)

    async def connect(self, **kwargs):
        await self.model_change.subscribe()
        await super().connect()

    @model_observer(Temperature)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serialize(self, instance, action, **kwargs):
        return dict(data=TemperatureSerializer(instance=instance).data, action=action.value)


class SingleConsumer(RetrieveModelMixin, GenericAsyncAPIConsumer):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer
    permission_classes = (permissions.AllowAny,)
    tp = Temperature.objects.all().order_by('-created')[0]

    def get_object(self, **kwargs) -> Temperature:
        return self.tp

    async def connect(self, **kwargs):
        await self.model_change.subscribe()
        await super().connect()

    @model_observer(Temperature)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serialize(self, instance, action, **kwargs):
        return dict(data=TemperatureSerializer(instance=instance).data, action=action.value)
