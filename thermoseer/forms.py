from django.forms import ModelForm

from demo.models import Temperature, ScannerTemperature


class TemperatureForm(ModelForm):
    class Meta:
        model = Temperature
        fields = ('scanner', "temp")


class ScannerTemperatureForm(ModelForm):
    class Meta:
        model = ScannerTemperature
        fields = ('scanner_id', "name", "dept")
