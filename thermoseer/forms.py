from django.forms import ModelForm

from demo.models import Temperature


class TemperatureForm(ModelForm):
    class Meta:
        model = Temperature
        fields = ('scanner_id', "name", "temp")
